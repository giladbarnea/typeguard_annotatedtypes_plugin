import re
import typing
from typing import Annotated

import pytest
import typeguard
from annotated_types import Ge
from typeguard import typechecked

import typeguard_annotatedtypes_plugin  # type: ignore # noqa: F401

Ge42 = Annotated[int, Ge(42)]


@typechecked
def foo(value: Ge42) -> None:
    pass


def test_Ge42_accepts_valid_value():
    foo(42)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(value=41, match="with value={value!r} failed {annotated_type}"),
        dict(value="hi", match="(str) is not an instance of int"),
    ],
)
def test_Ge42_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Ge42)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        foo(value)
