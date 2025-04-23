# embr.py
# ─────────────────────────────────────────────────────────────────────────────
# Embr DSL: Chat-like abstraction for natural language pipelines
# Inspired by UNIX shell syntax
#
# ─── Operator Table ───────────────────────────────────────────────────────────
# Operator | Purpose                            | Example usage
# ---------|-------------------------------------|------------------------------------
# `@`      | Assign role to message              | `user @ "message"`
# `<<`     | Append message to chat (in-place)   | `chat << "text"`
# `>>`     | Send chat to model, return response | `response = chat >> gpt`
# `>`      | Process chat with model             | `response = chat > gpt`
# `\|`     | Pipe chat into reducer, append if Spark | `chat | gpt`
# `\|=`    | Chain reducers into chat pipeline   | `chat |= gpt | claude`
#
# ─── Usage Examples ───────────────────────────────────────────────────────────
# chat = Embr()
# user @ "use the table analogy to understand autoregressive functions" > gpt >> chat
# chat = chat << "what about this?" | gpt
# chat << user @ "does this work?"
# chat |= gpt | claude | other_ai
# chat |= on_call @ gpt | on_call @ images
# task_chat > gpt >> global_chat  # Process and transfer without parentheses
# ─────────────────────────────────────────────────────────────────────────────

from dataclasses import dataclass, field, asdict
from typing import List, Callable, Optional, Union, TypeVar, Any, cast

default_role = "user"

# Define TypeVars for better type hinting
T = TypeVar("T", bound="Embr")  # TypeVar for Embr and its subclasses
S = TypeVar("S", bound="Spark")  # TypeVar for Spark and its subclasses
R = TypeVar("R", bound=Union["Embr", "Spark"])  # TypeVar for return types that can be either Embr or Spark
C = TypeVar("C")  # TypeVar for any type - used for flexible callable handling


@dataclass
class Spark:
    role: str
    content: Any
    # Removed source reference to avoid circular references

    def __post_init__(self):
        from textwrap import dedent

        if self.content:
            self.content = dedent(self.content).strip()

        # lines = self.content.split("\n")
        #
        # print("=============")
        # print(*lines, sep="\n")

    def __dict__(self):
        return asdict(self)

    def __gt__(self, other):
        """
        Enable Spark > Embr to append the spark to the chat
        Also support Spark > transformer to transform the Spark
        """
        if isinstance(other, Embr):
            # When Spark > Embr, append to the chat
            other << self
            return other
        elif callable(other):
            # When Spark > transformer, apply the transformation
            return other(self)
        raise TypeError(f"Cannot use > operator with types Spark and {type(other)}")

    def __rshift__(self, other):
        """
        Handle result >> chat pattern to transfer results to another chat
        Also support Spark >> transformer to transform the Spark
        """
        if isinstance(other, Embr):
            # Simply append this message to the target chat
            other << self
            return other
        elif callable(other):
            # When Spark >> transformer, apply the transformation
            return other(self)
        raise TypeError(f"Cannot use >> operator with Spark and {type(other)}")

    def __or__(self, transformer):
        """Enable Spark | transformer syntax"""
        if callable(transformer):
            return transformer(self)
        raise TypeError(f"Cannot use | operator with Spark and non-callable {type(transformer)}")


class EmbrMeta(type):
    def __matmul__(cls, arg):
        if isinstance(arg, str):
            return cls([Spark(role=default_role, content=arg)])

        return cls([arg])

    def __lshift__(cls, msgs):
        if not isinstance(msgs, tuple):
            msgs = (msgs,)
        cleaned = [
            Spark(default_role, msg) if isinstance(msg, str) else msg
            for msg in msgs
            if msg and (isinstance(msg, Spark) or (isinstance(msg, str) and msg))
        ]
        return cls(cleaned)


class Last:
    def __call__(self, e: "Embr"):
        return self.func(e.last)

    def __matmul__(self, fn: Callable[[Union["Embr", Spark]], T]):
        self.func = fn
        return self


last = Last()


@dataclass
class Embr(dict, metaclass=EmbrMeta):
    sparks: List[Spark] = field(default_factory=list)
    # reducers: List[Callable[["Embr"], Union["Embr", Spark]]] = field(default_factory=list)

    @property
    def md(self):
        """Returns the chat formatted in Markdown."""
        if not self.sparks:
            return ""

        markdown = ""
        for spark in self.sparks:
            markdown += f"**{spark.role}**: {spark.content}\n\n"

        return markdown.strip()

    def __dict__(self):
        """Returns the chat as a dictionary."""
        return [asdict(s) for s in self.sparks]

    def _clean_sparks(self, sparks):
        return [e for e in sparks if isinstance(e, Spark) and e.content]

    def __lshift__(self, other: Optional[Union[str, Spark]] = None):
        """
        Append a message to the chat. Handles various input types:
        - None: Returns a lambda for deferred execution
        - str: Creates a Spark with the default role
        - Spark: Appends directly

        Returns self for method chaining.
        """
        if other is None:
            # return lambda entry: self << entry
            spark = Spark(default_role, other)
        elif isinstance(other, Embr):
            for spark in other.sparks:
                self << spark
            return self
        elif isinstance(other, str):
            spark = Spark(default_role, other)
        elif isinstance(other, Spark):
            spark = other
        else:
            return self

        # Just add a copy of the Spark to our list
        clean_spark = Spark(spark.role, spark.content)
        self.sparks.append(clean_spark)

        return self

    def __rshift__(self, other: Union[Callable[["Embr"], R], "Embr"]) -> R:
        """
        Handle >> operator to either:
        1. Process with a model (like chat >> gpt)
        2. Transfer sparks to another chat (like chat1 >> chat2)
        """
        if isinstance(other, Embr):
            # Transfer all sparks to the other chat
            for spark in self.sparks:
                other << spark
            return cast(R, other)
        else:
            # Process with a model or function
            result = other(self)
            if isinstance(result, (Spark, Embr)) or result is None:
                return cast(R, result if result is not None else self)
            raise TypeError(f"Function returned unsupported type: {type(result)}")

    def __gt__(self, other: Callable[["Embr"], Spark]) -> Spark:
        """
        Handle > operator to process chat through model and return result
        Enables chat > gpt syntax
        """
        if callable(other) or hasattr(other, "__call__"):
            result = other(self)
            if isinstance(result, Spark):
                return result
            elif isinstance(result, Embr):
                return result
            raise TypeError(f"Function returned unsupported type: {type(result)}")

        raise TypeError(f"Right operand must be callable, got {type(other)}")

    def process(self, transformer: Callable[["Embr"], Spark]) -> Spark:
        """Process chat through a model, returning a result that can be transferred"""
        result = transformer(self)
        if isinstance(result, Spark):
            return result
        raise TypeError(f"Transformer must return Spark, got {type(result)}")

    def append_to(self, target: "Embr") -> "Embr":
        """Append contents of this chat to target chat"""
        for spark in self.sparks:
            target << spark
        return target

    def __or__(self, transformer: Callable[["Embr"], Union["Embr", Spark]]) -> "Embr":
        """
        Apply a transformer to this chat and return a new Embr instance.
        If the transformer returns a Spark, append it to a new copy.
        If the transformer returns an Embr, return it.
        """
        # Create a new Embr with the same sparks
        new_embr = Embr(self.sparks.copy())

        result = transformer(self)
        if isinstance(result, Spark):
            print(">>>> result is Spark", result)
            new_embr << result
            return new_embr
        elif isinstance(result, Embr):
            print(">>>> result is Embr", result)
            return result
        raise TypeError(f"Transformer must return Spark or Embr, got {type(result)}")

    def __ror__(self, other: str) -> "Embr":
        return self << other

    def __ior__(self, reducer: Union[Callable[["Embr"], Union["Embr", Spark]], "Embr"]) -> "Embr":
        if isinstance(reducer, Embr):
            # self.reducers.extend(reducer.reducers)
            self << reducer
        elif callable(reducer):
            result = reducer(self)
            self << result
            # self.reducers.append(reducer)
        else:
            raise TypeError("Reducer must be callable or Embr")
        return self

    # def apply_reducers(self) -> "Embr":
    #     for reducer in self.reducers:
    #         result = reducer(self)
    #         if isinstance(result, Spark):
    #             self << result
    #         elif isinstance(result, Embr):
    #             self.sparks.extend(result.sparks)
    #     return self

    def __getitem__(self, idx: int) -> Spark:
        return self.sparks[idx]

    def __len__(self) -> int:
        return len(self.sparks)

    @property
    def last(self):
        return self.sparks[-1] if self.sparks else None

    def rake(self):
        self.sparks = self._clean_sparks(self.sparks)
        return self
