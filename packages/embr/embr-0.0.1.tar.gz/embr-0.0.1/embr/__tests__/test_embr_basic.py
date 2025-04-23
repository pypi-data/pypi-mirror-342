from embr.embr import Embr, Spark
from embr.roles import user, gpt


def test_role_annotation():
    """Tests that the @ operator correctly creates a Spark object with the proper role and content."""
    entry = user @ "hello"

    assert type(entry) is Spark
    assert entry.role == "user" and entry.content == "hello"


def test_append_operator():
    """Tests that the << operator correctly appends content to the Embr instance."""
    embr = Embr()
    embr << "hello"
    assert embr.last.content == "hello"


def test_append_operator_without_parentheses():
    """Tests appending a Spark object using << operator without requiring parentheses."""
    embr = Embr()
    embr << user @ "hello"
    assert embr.last.content == "hello" and embr.last.role == "user"


def test_carry_into_gpt():
    """Tests forwarding content to GPT using >> operator and | pipe operator."""
    embr = Embr()
    embr << "hello"
    response = embr >> gpt
    assert response.content == "[gpt] response to: hello"


def test_pipe_returns_chat():
    embr = Embr()
    result = embr << "hello" | gpt
    assert type(result) is Embr
    assert result.last.content == "[gpt] response to: hello"


def test_rake():
    """Tests the rake operation that removes empty messages from the conversation."""
    embr = Embr([Spark("user", ""), Spark("user", "hello")])
    embr.rake()
    assert len(embr) == 1 and embr[0].content == "hello"


def test_chained_expression():
    """Tests a chain of operations including appending, raking, and GPT processing."""
    embr = Embr()
    embr << user @ "hello" << None
    assert len(embr) == 2 and embr.last.content is None
    embr.rake()
    assert len(embr) == 1

    response = embr >> gpt
    embr << response
    assert len(embr) == 2 and embr.last.content == "[gpt] response to: hello"


def test_string_pipe_syntax():
    """Tests the pipe operator for adding string content directly to Embr instance."""
    embr = Embr()
    embr = "hello" | embr
    assert embr.last.content == "hello" and embr.last.role == "user"


def test_last_property():
    """Tests the last property accessor for retrieving the most recent message."""
    embr = Embr()
    assert embr.last is None
    embr << "hello"
    assert embr.last.content == "hello"


def test_auto_strip_noop():
    """Tests automatic stripping of empty messages and None values during append."""
    embr = Embr()
    for val in ["", None, "hello"]:
        if val:
            embr << val
    assert len(embr) == 1 and embr.last.content == "hello"


def test_meta_class_init_single_message():
    """Tests initialization of Embr with a single message using class-level << operator."""
    embr = Embr << "hello"
    assert len(embr) == 1 and embr.last.content == "hello"


def test_meta_class_init_multiple_messages():
    """Tests initialization of Embr with multiple messages using class-level << operator."""
    embr = Embr << ("", "hello", None)
    assert len(embr) == 1 and embr.last.content == "hello"


def test_inplace_single_message():
    """Tests in-place append of a single message to an Embr instance."""
    embr = Embr()
    embr << "hey"
    assert len(embr) == 1 and embr.last.content == "hey"


def test_inplace_multiple_messages():
    """Tests in-place append of multiple messages to an Embr instance."""
    embr = Embr()
    for msg in ("uhm", "does this work", None, ""):
        if msg:
            embr << msg

    assert len(embr) == 2
    assert embr[-2].content == "uhm"
    assert embr.last.content == "does this work"
