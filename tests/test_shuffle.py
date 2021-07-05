from mixer import shuffle_tokens, TaggedToken


def test_shuffle():
    tokens = [
        TaggedToken("every", "TAG_1"),
        TaggedToken("hunter", "TAG_2"),
        TaggedToken("wants", "TAG_3"),
        TaggedToken("to", "TAG_4"),
        TaggedToken("know", "TAG_5"),
    ]
    assert shuffle_tokens(tokens) == tokens

    tokens = [TaggedToken(str(i), "TAG_1") for i in range(100)] + \
             [TaggedToken(str(i), "TAG_2") for i in range(100)]
    shuffled_tokens = shuffle_tokens(tokens)
    assert tokens != shuffled_tokens
    assert sorted(tokens[:100], key=repr) + sorted(tokens[100:], key=repr) == \
           sorted(shuffled_tokens[:100], key=repr) + sorted(shuffled_tokens[100:], key=repr)
