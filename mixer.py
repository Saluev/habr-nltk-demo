import argparse
from collections import defaultdict
from dataclasses import dataclass
import random
import subprocess
import sys
from typing import List, MutableMapping, Set

import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer


Tag = str


@dataclass
class TaggedToken:
    text: str
    tag: Tag


def tokenize_text(text: str) -> List[str]:
    return nltk.word_tokenize(text)


def tag_tokens(tokens: List[str]) -> List[TaggedToken]:
    return [
        TaggedToken(text=token, tag=tag)
        for token, tag in nltk.pos_tag(tokens)
    ]


def tokenize_and_tag_text(text: str) -> List[TaggedToken]:
    output = subprocess.run("cmd/tree-tagger-russian",
                            cwd="treetagger",
                            input=text.encode("utf-8"),
                            capture_output=True).stdout.decode("utf-8")
    result = []
    for line in output.strip().split("\n"):
        text, tag, _ = line.split("\t")
        result.append(TaggedToken(text=text, tag=tag))
    return result


def calc_private_nouns_set(tokens: List[TaggedToken]) -> Set[str]:
    result = set()
    for prev_token, token in zip([TaggedToken(".", ".")] + tokens, tokens):
        if prev_token.text != "." and token.text[0].islower():
            result.add(token.text.lower())
    return result


DONT_MIX_WORDS = {
    "a", "an", "the",
    "am", "is", "are", "been", "was", "were",
    "have", "had",
}
DONT_MIX_MARKER = "DONT_MIX"
DONT_MIX_TAGS = {DONT_MIX_MARKER, "-"}


def shuffle_tokens(tokens: List[TaggedToken]) -> List[TaggedToken]:
    tokens = [
        token if token.text not in DONT_MIX_WORDS else TaggedToken(text=token.text, tag=DONT_MIX_MARKER)
        for token in tokens
    ]
    tokens_by_tag: MutableMapping[Tag, List[TaggedToken]] = defaultdict(list)
    index_to_tag: MutableMapping[int, Tag] = {}
    index_to_subindex: MutableMapping[int, int] = {}
    for idx, token in enumerate(tokens):
        index_to_tag[idx] = token.tag
        index_to_subindex[idx] = len(tokens_by_tag[token.tag])
        tokens_by_tag[token.tag].append(token)
    for tag, curr_tokens in tokens_by_tag.items():
        if tag not in DONT_MIX_TAGS:
            random.shuffle(curr_tokens)
    return [
        tokens_by_tag[index_to_tag[idx]][index_to_subindex[idx]]
        for idx in range(len(tokens))
    ]


def detokenize_tokens(tokens: List[TaggedToken], private_nouns: Set[str]) -> str:
    cased_tokens = []
    for prev_token, token in zip([TaggedToken(".", ".")] + tokens, tokens):
        if prev_token.text == ".":
            cased_tokens.append(token.text[0].upper() + token.text[1:])
        elif token.text.lower() in private_nouns:
            cased_tokens.append(token.text[0].lower() + token.text[1:])
        else:
            cased_tokens.append(token.text)
    result = TreebankWordDetokenizer().detokenize(cased_tokens)
    result = result.replace(" .", ".")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shuffle words in text.")
    parser.add_argument("--tagger", type=str, default="nltk", choices=["nltk", "treetagger"])
    args = parser.parse_args()

    input_text = "".join(sys.stdin)
    if args.tagger == "nltk":
        tokens = tokenize_text(input_text)
        tagged_tokens = tag_tokens(tokens)
    elif args.tagger == "treetagger":
        tagged_tokens = tokenize_and_tag_text(input_text)
    private_nouns = calc_private_nouns_set(tagged_tokens)
    sys.stderr.write(f"Tagged tokens:\n{tagged_tokens!r}")
    shuffled_tokens = shuffle_tokens(tagged_tokens)
    result_text = detokenize_tokens(shuffled_tokens, private_nouns)
    print(result_text)
