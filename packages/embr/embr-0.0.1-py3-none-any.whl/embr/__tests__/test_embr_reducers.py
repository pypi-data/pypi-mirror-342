"""
# Summary: Reducer Patterns

Embr supports reducer functions.

`Embr \| reducer (embr, others) -> Spark -> embr_2`

Also, chaining without existing chat:

```python
chat |= gpt | claude | other_ai
```

allows us to combine the returns from all of these, and have them all output when an event happens.

✅ The `|` operator is immutable — it returns a new `Embr` instance.
✅ When reducers are chained together (e.g., `gpt | claude | other_ai`), they are grouped into a single chained reducer function.
"""

import pytest  # noqa: F401
from embr.embr import Embr, Spark
from embr.reducers import chainable
from embr.roles import user, gpt, claude, other_ai


def test_reducer_chain_with_pipe():
    chat = Embr()
    chat << user @ "hello"

    @chainable
    def reducer_1(chat: Embr) -> Spark:
        return Spark("assistant", "[r1] response to: " + chat.last.content)

    @chainable
    def reducer_2(chat: Embr) -> Spark:
        return Spark("assistant", "[r2] response to: " + chat.last.content)

    chained = reducer_1 | reducer_2
    new_chat = chat | chained

    assert len(new_chat) == 3
    assert new_chat[-1].content.startswith("[r2]")
    assert new_chat[-2].content.startswith("[r1]")
    assert new_chat[0].role == "user"

    # the original chat should be unchanged.
    assert len(chat) == 1  # original chat unchanged


def test_reducer_chain_without_chat():
    chat = Embr()
    chat << user @ "test message"

    reducers = gpt | claude | other_ai

    updated = chat | reducers

    assert len(updated) == 4
    assert updated[-1].content.startswith("[other_ai]")
    assert updated[-2].content.startswith("[claude]")
    assert updated[0].role == "user"

    print(updated)

    assert len(chat) == 1  # original chat unchanged
