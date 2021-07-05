from collections import defaultdict
from dataclasses import dataclass
import random
import sys
from typing import List, MutableMapping, Tuple

import nltk


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


DONT_MIX_WORDS = {
    "a", "an", "the",
    "am", "is", "are", "been", "was", "were",
    "have", "had",
}
DONT_MIX_MARKER = "DONT_MIX"


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
        if tag != DONT_MIX_MARKER:
            random.shuffle(curr_tokens)
    return [
        tokens_by_tag[index_to_tag[idx]][index_to_subindex[idx]]
        for idx in range(len(tokens))
    ]


def detokenize_tokens(tokens: List[TaggedToken]) -> str:
    ...


if __name__ == "__main__":
    input_text = "".join(sys.stdin)
    tokens = tokenize_text(input_text)
    tagged_tokens = tag_tokens(tokens)
    sys.stderr.write(f"Tagged tokens:\n{tagged_tokens!r}")
    shuffled_tokens = shuffle_tokens(tagged_tokens)
    result_text = detokenize_tokens(shuffled_tokens)
    print(result_text)
