import re
from typing import Union, Type

from embr.embr import Spark


def save_jsonl(arr, filename="collection.jsonl", overwrite=True):
    import json
    from pathlib import Path

    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "w" if overwrite else "a+") as f:
        for item in arr:
            f.write(json.dumps(item) + "\n")


class Ror:
    """Proxy Object for using the or notation. Also
    supports being called directly, which supports
    more complex arguments.

    **Note**: execution goes from left to right.
    """

    def __init__(self, fn):
        self.fn = fn

    def __ror__(self, arg):
        return self.fn(arg)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


class At:
    """Proxy Object for using the @ notation. Also
    supports being called direction, which supports
    more complex arguments."""

    def __init__(self, fn):
        self.fn = fn

    def __matmul__(self, arg):
        return self.fn(arg)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


def remove_comments(input_string):
    full_text = ""
    for line in input_string.split("\n"):
        if line.strip().startswith("//"):
            continue
        if line.strip().startswith("#"):
            continue
        if line.strip().startswith("......"):
            continue
        if line.strip().startswith("..."):
            continue
        full_text += line + "\n"

    return full_text


def replace_substring(test_str, s1, s2):
    # Replacing all occurrences of substring s1 with s2
    test_str = re.sub(s1, s2, test_str)
    return test_str


def to_json(input_string):
    import json5

    # chatGPT sometimes forgets about a comma at the end of the line
    input_string = replace_substring(input_string, '"\n', '",\n')
    input_string = replace_substring(input_string, '"\)\n', '",\n')
    input_string = replace_substring(input_string, ".',\n", '.",\n')
    input_string = replace_substring(input_string, "”", '"')
    # it also sometimes adds comments and other stuff that is not JSON
    input_string = remove_comments(input_string)

    # Find the indices of the curly braces
    start_bracket = input_string.find("{")
    end_bracket = input_string.rfind("}")

    if end_bracket == -1:
        input_string += "}"
        end_bracket = input_string.rfind("}")

    # Extract the JSON part from the string
    json_part = input_string[start_bracket : end_bracket + 1]
    # Convert the extracted JSON to a Python dictionary
    data = json5.loads(json_part)
    return data


def to_jsonl(input_string):
    import json5

    input_string = replace_substring(input_string, "\.\n(\s*)\}", '."\n\g<1>}')
    input_string = replace_substring(input_string, '"\n', '",\n')
    input_string = replace_substring(input_string, "”", '"')
    input_string = remove_comments(input_string)

    # Find the indices of the curly braces
    start_bracket = input_string.find("[")
    end_bracket = input_string.rfind("]")

    if end_bracket == -1:
        input_string += "]"
        end_bracket = input_string.rfind("]")

    # Extract the JSON part from the string
    json_part = input_string[start_bracket : end_bracket + 1]

    # Convert the extracted JSON to a Python dictionary
    # json_part = json_part[:610].replace("\n", r"\n") + '"}]'
    # print(json_part)
    data = json5.loads(json_part)
    return data


class Text(str):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    def indent(self, n=4):
        lines = self.text.splitlines()
        return Text("\n".join(" " * n + line for line in lines))


def jsonl(*keys, dtype: Type[Text] = Text):
    """Return proxy object to convert the response
    text into an JSON, its values specified by keys,
    or a single value given just one key.
    """

    def destructure(response: Union[str, Text, Spark]) -> Union[dict, list, dtype]:
        if isinstance(response, Text):
            response = response.text

        if isinstance(response, Spark):
            response = response.content

        data = to_jsonl(response)

        return data

    return Ror(destructure)


def json(*keys, dtype: Type[Text] = Text):
    """Return proxy object to convert the response
    text into an JSON, its values specified by keys,
    or a single value given just one key.
    """

    def destructure(response: Union[str, Text, Spark]) -> Union[dict, list, dtype]:
        if isinstance(response, Text):
            response = response.text

        if isinstance(response, Spark):
            response = response.content

        if isinstance(response, Spark):
            response = response.content

        data = to_json(response)

        if len(keys) > 1:
            results = []
            for k in keys:
                value = data.get(k, None)
                if isinstance(value, str):
                    value = dtype(value)

                results.append(value)

            return results

        elif len(keys) == 1:
            value = data.get(keys[0], None)
            if isinstance(value, str):
                value = dtype(value)
            return value

        else:
            return data

    return Ror(destructure)
