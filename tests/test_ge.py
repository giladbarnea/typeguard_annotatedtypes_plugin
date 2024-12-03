import re
import typing
from typing import Annotated

import annotated_types as at
import pytest
import typeguard
from typeguard import typechecked

import typeguard_annotatedtypes_plugin  # type: ignore # noqa: F401

# --------[ int ]--------
Ge4 = Annotated[int, at.Ge(4)]


@typechecked
def expects_ge4(value: Ge4) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [4, 5, 6, 1000],
)
def test_Ge4_accepts_valid_value(valid_case):
    expects_ge4(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (0, -1)
    ]
    + [
        dict(value="hi", match="{value!r} is not an instance of {origin_type.__name__}")
    ],
)
def test_Ge4_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    origin_type, annotated_type = typing.get_args(Ge4)
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.escape(
            match.format(
                value=value, annotated_type=annotated_type, origin_type=origin_type
            )
        ),
    ):
        expects_ge4(value)


# --------[ float ]--------

Ge0dot5 = Annotated[float, at.Ge(0.5)]


@typechecked
def expects_ge0dot5(value: Ge0dot5) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [0.5, 0.6, 0.7, 0.8, 0.9],
)
def test_Ge0dot5_accepts_valid_value(valid_case):
    expects_ge0dot5(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (0.4, 0.0, -0.1)
    ]
    + [
        dict(value="hi", match="{value!r} is not an instance of {origin_type.__name__}")
    ],
)
def test_Ge0dot5_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    origin_type, annotated_type = typing.get_args(Ge0dot5)
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.escape(
            match.format(
                value=value, annotated_type=annotated_type, origin_type=origin_type
            )
        ),
    ):
        expects_ge0dot5(value)
