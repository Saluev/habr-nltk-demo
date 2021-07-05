from dataclasses import dataclass
import sys
from typing import List


Tag = str


@dataclass
class TaggedToken:
    text: str
    tag: Tag


def tokenize_text(text: str) -> List[str]:
    ...


def tag_tokens(tokens: List[str]) -> List[TaggedToken]:
    ...


def shuffle_tokens(tokens: List[TaggedToken]) -> List[TaggedToken]:
    ...


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
