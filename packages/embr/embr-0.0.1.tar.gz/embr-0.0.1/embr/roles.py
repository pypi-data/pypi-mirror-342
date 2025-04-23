from dataclasses import asdict
from typing import Optional, Callable, Union

from embr.embr import Spark, T, S, Embr
from embr.reducers import chain_reducers
from embr.cache_utils.lru_cache import lru_cache


class Role:
    def __init__(self, name: str):
        self.name = name

    def __matmul__(self, content: str) -> "Spark":
        return Spark(self.name, content)


class CallableRole(Role):
    def __init__(self, name: str, func: Optional[Callable[[T], S]] = None):
        super().__init__(name)
        self.func = func

    def __call__(self, embr: Union[T, S]) -> S:
        """
        Make the role callable to process chats, or Sparks
        Handles both Embr and Spark objects
        """
        if self.func:
            # If we get a Spark directly, create a temporary Embr to hold it
            if isinstance(embr, Spark):
                # Create a temporary Embr with just this Spark
                temp_embr = Embr([embr])
                return self.func(temp_embr)
            elif isinstance(embr, Embr):
                return self.func(embr)
            else:
                raise TypeError(f"Cannot call {type(self)} with {type(embr)}")

        return Spark(self.name, f"Default response from {self.name}")

    def __or__(self, other):
        """Enable chaining reducers with the | operator"""
        if callable(other):
            return chain_reducers(self, other)
        raise TypeError(f"Cannot use | operator with {type(self)} and non-callable {type(other)}")


user = Role("user")
system = Role("system")
on_call = Role("on_call")
assistant = Role("assistant")


def gpt_function(embr: Embr) -> Spark:
    return Spark("assistant", f"[gpt] response to: {embr.last.content if embr.last else ''}")
    # message = call_gpt(messages=[asdict(s) for s in embr.sparks])
    # return Spark(**message)


def claude_function(embr: Embr) -> Spark:
    return Spark("assistant", f"[claude] response to: {embr.last.content if embr.last else ''}")


def other_ai_function(embr: Embr) -> Spark:
    return Spark("assistant", f"[other_ai] response to: {embr.last.content if embr.last else ''}")


gpt = CallableRole("assistant", gpt_function)
claude = CallableRole("assistant", claude_function)
other_ai = CallableRole("assistant", other_ai_function)


@lru_cache(cache_mode="mongodb")
def call_gpt(messages, model="gpt-4o"):
    from openai import OpenAI

    client = OpenAI()
    completion_gen = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    print("GPT-4o: \n")
    all_text = ""

    # role will be empty in later delta.
    role = None
    for completion in completion_gen:
        message = completion.choices[0].delta
        role = role or message.role
        text_delta = message.content
        if text_delta is None:
            break

        all_text += text_delta
        print(message.content, end="")

    return dict(role=role, content=all_text)


def fn(embr: Embr) -> Spark:
    return Spark(
        **call_gpt(
            messages=[asdict(s) for s in embr.sparks],
            model="gpt-4o",
            # _no_cache=True,
        ),
    )


# gpt4o = CallableRole("assistant", lambda embr: call_gpt(messages=[asdict(s) for s in embr.sparks], model="gpt-4o"))
gpt4o = CallableRole("assistant", fn)
