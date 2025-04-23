def test_context_cache():
    from embr.embr import Embr
    from embr.roles import user, gpt4o

    chat = Embr()

    chat << "hello"

    chat <<= "Note: return single numbers, do NOT text more than that."
    chat |= gpt4o

    chat << "let's compute 1 + 1 =?"
    chat |= gpt4o

    chat << user @ "what if we now add 3?"
    response = chat > gpt4o

    assert len(chat) == 6, "the last one shall now log."
    assert response.content == "5", "the result should accumulate all messages in the context."
