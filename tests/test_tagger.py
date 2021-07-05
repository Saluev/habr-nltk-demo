from mixer import tag_tokens, TaggedToken


def test_tagger():
    assert tag_tokens(["hello", ",", "world"]) == [
        TaggedToken("hello", "NN"),
        TaggedToken(",", ","),
        TaggedToken("world", "NN"),
    ]
