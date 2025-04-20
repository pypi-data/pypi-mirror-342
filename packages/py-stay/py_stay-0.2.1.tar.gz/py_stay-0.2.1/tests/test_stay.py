#!/usr/bin/env python

"""Tests for `stay` package."""

from shlex import split

import pytest

from stay import InvalidParentParserError, StayParser, Stayspace


class Space1(Stayspace):
    arg1: int
    arg2: bool
    arg3: str


class Space2(Space1):
    foo: float


class Space3(Stayspace):
    unrelated: str


@pytest.fixture
def base_parser() -> StayParser[Space1]:
    parser = StayParser(namespace_cls=Space1, add_help=False)

    parser.add_argument("--arg1", type=int)
    parser.add_argument("--arg2", type=bool)
    parser.add_argument("--arg3", type=str)

    return parser


def test_args(base_parser: StayParser[Space1]):
    args = base_parser.parse_args(split('--arg1 42 --arg2 true --arg3 "stay is awesome"'))

    assert args.arg1 == 42
    assert args.arg2
    assert args.arg3 == "stay is awesome"


def test_valid_parent_parsers(base_parser: StayParser[Space1]):
    parser = StayParser(namespace_cls=Space2, parents=[base_parser])

    parser.add_argument("--foo", type=float)

    args = parser.parse_args(split('--arg1 42 --arg2 true --arg3 "stay is awesome" --foo 3.14'))

    assert args.arg1 == 42
    assert args.arg2
    assert args.arg3 == "stay is awesome"
    assert args.foo == pytest.approx(3.14)


def test_invalid_parent(base_parser: StayParser[Space1]):
    with pytest.raises(InvalidParentParserError):
        StayParser(namespace_cls=Space3, parents=[base_parser])
