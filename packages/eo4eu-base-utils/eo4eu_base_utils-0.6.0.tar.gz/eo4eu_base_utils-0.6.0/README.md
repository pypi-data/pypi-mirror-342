# Base utilities for EO4EU

This package serves as a common base of utilities used in other `eo4eu-[...]-utils` packages. You may find it generally useful.

## General

- The `if_none` function helps with the writing of optional parameters. For example:

```py
def validate(input: str, accepted: list[str]|None = None):
    accepted = if_none(accepted, ["yes", "definitely", "absolutely"])
    if input not in accepted:
        raise ValueError(f"Input \"{input}\" not in {accepted}")
```


## Typing
The `eo4eu_base_utils.typing` submodule provides some of the types found in the standard library `typing` module. The difference is, for versions below 3.10, this module will pull them from `typing_extensions` instead.

## Unify
The `eo4eu_base_utils.unify` submodule provides functions for working with dictionaries. Namely:

- `overlay` combines two dictionaries recursively, preserving nested keys if possible. In the case of conflicts, `overlay` will prefer the second dictionary provided. Example:

```py
from pprint import pprint
from eo4eu_base_utils.unify import overlay

h0 = {
    "name": "bobby.png",
    "dataset": "hamster images",
    "date": None,
    "metadata": {
        "size": "3TB",
        "color": "brown",
    },
}
h1 = {
    "path": "/usr/hamsters/bobby.png",
    "date": "2025-14-01",
    "metadata": {
        "color": "brown and white, actually",
        "type": "chubby",
    },
}

pprint(overlay(h0, h1))
```
Output:
```py
{'dataset': 'hamster images',
 'date': '2025-14-01',
 'metadata': {'color': 'brown and white, actually',
              'size': '3TB',
              'type': 'chubby'},
 'name': 'bobby.png',
 'path': '/usr/hamsters/bobby.png'}
```

- `unify` is similar to `overlay`, but raises a `eo4eu_base_utils.unify.UnifyError` in the case of conflicts. This function has a more general notion of values being "compatible"; one or both of the dictionaries might have **types** as values, thus serving as more of a schema. An example:

```py
from pprint import pprint
from eo4eu_base_utils.unify import overlay

schema = {
    "service": "elasticsearch",
    "auth": {
        "username": str,
        "password": str,
    },
    "port": int,
}

good_data = {
    "service": "elasticsearch",
    "mood": "good",
    "auth": {
        "username": "buddy",
        "password": "pasword",
    },
    "port": 6868,
}

also_good_data = {  # doesn't matter if keys are missing
    "auth": {
        "username": "buddy",
    },
}

bad_data = {
    "auth": {
        "username": 007,  # not a string
    },
}

pprint(unify(schema, good_data))
pprint(unify(schema, also_good_data))
pprint(unify(schema, bad_data))  # this will raise an error
```

`unify` is commutative, therefore `unify(d0, d1) == unify(d1, d0)`.

## Result
The `Result` type is a hacky attempt to get something like rust's `Result` type, and have errors as values instead of exceptions. It has several constructors:

```py
def parse_num(num_str: str) -> Result[float]:
    try:
        return Result.ok(float(num_str))
    except Exception as e:
        return Result.err(str(e))
```

The above function may also be written as:

```py
def parse_num(num_str: str) -> Result[float]:
    return Result.wrap(float, num_str)
```

The `Result` type allows you to do a few neat things. For example, instead of this pattern:

```py
config = None
try:
    config = read_from_file(config_file)
except Exception as e:
    logger.error(f"Failed to read config: {e}")
```

You can do this:

```py
config = read_from_file(config_file)  # returns Result
if config.is_err():
    logger.error(f"Failed to read config: {config.fmt_err()}")
```

There is also `result.is_ok()` which is the opposite of `result.is_err()`. Also, things like:

```py
some_num = (Result.wrap(get_user_input)
                  .default("7")
                  .map_ok(lambda num_str: float(num_str))
                  .map_ok(lambda num: num if num > 0 else 0)
                  .unwrap())  # this raises an exception if the result is an error
```

Which would normally be written as:
```py
def get_some_num():
    user_input = "7"
    try:
        user_input = get_user_input()
    except Exception:
        pass

    num = float(user_input)
    if num < 0:
        num = 0
    return num
```

Possibly a bad example, but anyway...
