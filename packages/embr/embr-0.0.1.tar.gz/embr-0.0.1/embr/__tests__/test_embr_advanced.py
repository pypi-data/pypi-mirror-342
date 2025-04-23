"""
Test suite for the Embr library demonstrating core functionality and usage patterns:

1. **Basic Chat Operations**:
   - Direct message creation and processing with GPT
   - Chaining multiple model responses (GPT, Claude)
   - Basic chat context management

2. **Advanced Message Handling**:
   - Chat transfer between contexts
   - Response processing and modification
   - Context merging and state management

3. **Control Flow Patterns**:
   - Direct message transfer
   - Response object manipulation
   - Multi-step conversation processing

4. **Integration Features**:
   - Multiple chat context handling
   - Response chaining across contexts
   - State verification and assertions

These tests validate the core functionality and demonstrate recommended usage patterns
for building complex conversational applications with the Embr library.
"""

import pytest  # noqa: F401
from embr.embr import Embr, Spark
from embr.roles import user, gpt, claude


def test_gpt():
    response = user @ "hello" > gpt
    print(response)

    response = user @ "hello" >> gpt >> claude
    print(response)


def test_general():
    chat = Embr()

    # These are now possible
    result = user @ "hello" > gpt  # Create a message and process it directly
    chat << user @ "hello" > gpt  # Create, process, and append the result
    response = user @ "hello" >> chat > gpt  # Create, process, and append the result

    # Modified to avoid recursion with simpler alternatives
    spark = user @ "hello"
    spark >> chat  # First add the message
    result = chat > gpt  # Then process
    result >> chat  # Then append the result

    chat = Embr()
    # Alternative approach using pipe
    a = user @ "hello" | gpt > chat  # Another variation
    print(a)

    # # More advanced composition
    result = user @ "hello" >> gpt >> claude  # Chain transformers


def test_chat_transfer_pattern():
    """
    Tests the pattern where the task chat is processed by gpt
    and then transferred to the global chat using chained operations.

    This pattern demonstrates the operator precedence and flow:

    ```
    ┌────────────┐    ┌─────┐    ┌─────────────┐    ┌────────────┐
    │ task_chat  │ >  │ gpt │ -> │ response    │ >> │ global_chat│
    └────────────┘    └─────┘    │ (Spark)     │    └────────────┘
                                 └─────────────┘
    ```
    """
    # Initialize chats
    task_chat = Embr()
    global_chat = Embr()

    # Add a message to the task chat
    task_chat << user @ "hello"

    # Process with gpt and transfer to global chat
    response = task_chat > gpt

    task_chat >> global_chat
    response >> global_chat

    # Verify results
    assert len(global_chat) == 2
    assert global_chat.last.role == "assistant"
    assert global_chat.last.content == "[gpt] response to: hello"


def test_flow_without_parentheses():
    """
    Tests alternative patterns to eliminate parentheses
    when transferring processed chat content.

    Shows different approaches for handling the flow:

    ```
    ┌────────────┐    ┌─────┐    ┌─────────────────┐    ┌────────────┐
    │ task_chat  │ >  │ gpt │ -> │ Intermediate    │ >  │ global_chat│
    └────────────┘    └─────┘    │ Object with     │    └────────────┘
                                 │ response stored │
                                 └─────────────────┘
    ```
    """
    # Initialize chats
    task_chat = Embr()
    global_chat = Embr()

    # Add a message to the task chat
    task_chat << user @ "hello world"

    # get a response and manually append
    response = task_chat > gpt
    global_chat << response  # Directly append the response

    # Verify results
    assert len(global_chat) == 1
    assert global_chat.last.role == "assistant"
    assert global_chat.last.content == "[gpt] response to: hello world"


def test_chat_context_management():
    """
    Tests managing separate conversational contexts
    and selectively merging them.

    Visual representation of the pattern:

    ```
    Global Chat                Task Chat
    ┌────────────┐            ┌────────────┐
    │ (empty)    │            │ (empty)    │
    └────────────┘            └────────────┘
                                   │
                                   ▼
                              ┌────────────┐
                              │ "Question" │
                              └────────────┘
                                   │
                                   ▼
    Task Chat > gpt = Spark   ┌────────────┐
                              │ > gpt      │
                              └────────────┘
                                   │
                                   ▼
    Task Chat << Spark        ┌────────────┐
                              │ "Question" │
                              │ "Answer"   │
                              └────────────┘
                                   │
                                   ▼
                              ┌────────────┐
    Task Chat >> Global Chat  │ >> Global  │
                              └────────────┘
                                   │
                                   ▼
                              ┌────────────┐
    Global Chat (updated)     │ "Question" │
                              │ "Answer"   │
                              └────────────┘
    ```
    """
    # Initialize chats
    task_chat = Embr()
    global_chat = Embr()

    # Add a message to the task chat
    task_chat << user @ "What's the weather?"

    # Process with gpt
    response = task_chat > gpt

    # Add a response to task chat
    task_chat << response

    # Make sure task chat has both question and answer
    assert len(task_chat) == 2
    assert task_chat[0].role == "user"
    assert task_chat[1].role == "assistant"

    # Transfer task chat to global chat
    task_chat >> global_chat

    # Verify results - global chat should have both messages
    assert len(global_chat) == 2
    assert global_chat[0].role == "user"
    assert global_chat[1].role == "assistant"


def test_direct_transfer_pattern():
    """Tests direct message transfer between the chats without processing."""
    task_chat = Embr()
    global_chat = Embr()

    # Add messages to task chat
    task_chat << user @ "Hello there"
    task_chat << gpt @ "Hi, how can I help?"

    # Transfer to global chat
    task_chat >> global_chat

    assert len(global_chat) == 2
    assert global_chat[0].role == "user"
    assert global_chat[0].content == "Hello there"
    assert global_chat[1].role == "assistant"
    assert global_chat[1].content == "Hi, how can I help?"


def test_response_object_methods():
    """Tests that the response objects from an LLM have the expected methods."""
    task_chat = Embr()
    task_chat << user @ "test message"

    response = task_chat > gpt

    # Response should be a Spark object
    assert isinstance(response, Spark)
    assert response.role == "assistant"
    assert response.content.startswith("[gpt] response to: ")

    # Should be able to modify content
    response.content = "Modified content"
    assert response.content == "Modified content"


def test_multiple_responses_chaining():
    """Tests chaining multiple responses through the different chats."""
    chat1 = Embr()
    chat2 = Embr()
    chat3 = Embr()

    # Start conversation in chat1
    chat1 << user @ "initial message"

    # Process chat1 and get a response
    response1 = chat1 > gpt

    # Transfer chat1 content and response to chat2
    chat1 >> chat2
    response1 >> chat2

    # Add another user message to chat2
    chat2 << user @ "follow-up question"

    # Process chat2 and get a response
    response2 = chat2 > gpt

    # Transfer chat2 content and response to chat3
    chat2 >> chat3
    response2 >> chat3

    # Verify chat3 has the complete conversation history
    assert len(chat3) == 4
    assert chat3[0].role == "user"
    assert chat3[0].content == "initial message"
    assert chat3[1].role == "assistant"
    assert chat3[1].content == "[gpt] response to: initial message"
    assert chat3[2].role == "user"
    assert chat3[2].content == "follow-up question"
    assert chat3[3].role == "assistant"
    assert chat3[3].content == "[gpt] response to: follow-up question"
