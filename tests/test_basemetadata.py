import re
import typing
from typing import Annotated, Any, Iterable, NamedTuple, Union

import annotated_types as at
import pytest
import typeguard
from typeguard import typechecked

import typeguard_annotatedtypes_plugin  # type: ignore # noqa: F401


class Case(NamedTuple):
    """
    A test case for `annotated_types`.
    """

    annotation: Any
    valid_cases: Iterable[Any]
    invalid_cases: Iterable[Any]


def cases() -> Iterable[Case]:
    # Gt, Ge, Lt, Le
    yield Case(Annotated[int, at.Gt(4)], (5, 6, 1000), (4, 0, -1))


Constraint = Union[at.BaseMetadata, slice, "re.Pattern[bytes]", "re.Pattern[str]"]

Ge42 = Annotated[int, at.Ge(42)]


@typechecked
def expects_greaterequal_42(value: Ge42) -> None:
    pass


def test_Ge42_accepts_valid_value():
    expects_greaterequal_42(42)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(value=41, match="with value={value!r} failed {annotated_type}"),
        # "hi" fails the int constraint
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
        expects_greaterequal_42(value)


Gt4 = Annotated[int, at.Gt(4)]


@typechecked
def expects_greaterthan_4_(value: Gt4) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [
        (5, 6, 1000),
    ],
)
def test_Gt4__accepts_valid_value(valid_case):
    expects_greaterthan_4_(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        [
            dict(
                value=invalid_value,
                match="with value={value!r} failed {annotated_type}",
            )
            for invalid_value in (4, 0, -1)
        ],
        # "hi" fails the int constraint
        dict(value="hi", match="(str) is not an instance of int"),
    ],
)
def test_Gt4__raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Gt4)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_greaterthan_4_(value)


def test_constraint_accepts_valid_value(constraint, valid_case, test_func):
    test_func(valid_case)


def test_constraint_raises_TypeCheckError(constraint, invalid_case, test_func):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(constraint)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        test_func(value)
