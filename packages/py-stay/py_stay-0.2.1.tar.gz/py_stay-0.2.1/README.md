# Stay

**S**imple **T**yped **A**rgparse, **Y**es

[![ruff-action](https://github.com/drkspace/stay/actions/workflows/ruff_action.yml/badge.svg?branch=main)](https://github.com/drkspace/stay/actions/workflows/ruff_action.yml)
[![Tests](https://github.com/drkspace/stay/actions/workflows/tests_action.yml/badge.svg)](https://github.com/drkspace/stay/actions/workflows/tests_action.yml)

Add typing to your argparse CLIs without having to modify your current parsers.

Example:

```python
from stay import Stayspace, StayParser

class ArgSpace(Stayspace):
    foo: int
    bar: str

parser = StayParser(namespace_cls=ArgSpace)

parser.add_argument("--foo", type=int)
parser.add_argument("--bar", type=float)

args = parser.parse_args()

reveal_type(args.foo) # int
reveal_type(args.bar) # float
reveal_type(args.invalid) # Type Error
```

## Install

To install from PyPi:

```bash
pip install -U py-stay
```

To install the most recent dev version

```bash
git clone https://github.com/drkspace/stay
cd stay
pip install .
```

## Why not other typed argparse libraries?

There are two other typed argparse libraries, [tap](https://github.com/swansonk14/typed-argument-parser) and [typed-argparse](https://github.com/typed-argparse/typed-argparse).
Their main deficiencies are that they can not replicate all of argparse's features, like argument groups and mutually exclusive groups.
Stay, on the other hand, will always support 100% of argparse's features as the parsing class, ``StayParser``, is a subclass of ``argparse.ArgumentParser``.

However, Stay cannot generate a parser from a ``Namespace`` or other data structure.
If you require that functionality, please use [tap](https://github.com/swansonk14/typed-argument-parser) or [typed-argparse](https://github.com/typed-argparse/typed-argparse).
No Hard feelings.

## Examples

Here are some examples.
See [examples/](examples/) for the full set.

### Simple Example

```python
#!/usr/bin/env python
# ruff: noqa: T201
from stay import StayParser, Stayspace


class CLIInput(Stayspace):
    name: str
    age: int

def main() -> None:

    parser = StayParser(namespace_cls=CLIInput)

    parser.add_argument("--name", type=str)
    parser.add_argument("--age", type=int)

    args = parser.parse_args()

    print(f"Hello {args.name}. You are {args.age} years old")

if __name__ == "__main__":
    main()
```

### Mutually exclusive groups

Unfortunately, python's typing system is not robust enough to have a nice way to have multiple/an arbitrary number types as the ``namespace_cls`` input.
You have to fake it with combining your ``Stayspace``s into one class and using that as input to ``namespace_cls``.
You are still able to type the generic as the union of your types and then you can use a ``TypeIs`` or ``TypeGuard`` (depending on your python version) to pick out the type.

> [!IMPORTANT]
> If you use the below strategy of creating a subclass of 2 ``Stayspace``s, any methods or ``ClassVar``s you add to them might interfere with eachother.


```python
#!/usr/bin/env python
# ruff: noqa: T201

from typing_extensions import TypeIs

from stay import StayParser, Stayspace


class CLIInput1(Stayspace):
    foo: int

class CLIInput2(Stayspace):
    bar: str

class CLICombined(CLIInput1, CLIInput2):
    ...

def is_inp_1(inp: CLIInput1|CLIInput2) -> TypeIs[CLIInput1]:
    return "foo" in inp

def main() -> None:

    parser = StayParser[CLIInput1|CLIInput2](namespace_cls=CLICombined)

    meg = parser.add_mutually_exclusive_group(required=True)
    meg.add_argument("--foo", type=int)
    meg.add_argument("--bar", type=str)

    args = parser.parse_args()

    if is_inp_1(args):
        print(f"You inputted foo with a value of {args.foo}")
    else:
        print(f"You inputted bar with a value of {args.bar}")

if __name__ == "__main__":
    main()
```

### Subparser

Subparsers act just like (mutually exclusive) groups.
In order to match with how argparse behaves, the results of a subparser will be "flat".
You can use ``TypeIs``/``TypeGuard`` to narrow a ``Stayspace`` to the one for a specific subparser.
