from mixer import tokenize_text


def test_tokenizer():
    assert tokenize_text("hello, world") == ["hello", ",", "world"]
