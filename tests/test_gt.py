import re
import typing
from typing import Annotated

import pytest
import typeguard
from annotated_types import Gt
from typeguard import typechecked

import typeguard_annotatedtypes_plugin  # type: ignore # noqa: F401

# --------[ int ]--------
Gt_neg2 = Annotated[int, Gt(-2)]


@typechecked
def expects_gt_neg2(value: Gt_neg2) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [-1, 2, 6, 7, 8, 9],
)
def test_Gt_neg2_accepts_valid_value(valid_case):
    expects_gt_neg2(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (-5, -6, -7)
    ],
    # + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Gt_neg2_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Gt_neg2)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_gt_neg2(value)


# --------[ float ]--------

Gt_neg2dot0 = Annotated[float, Gt(-2.0)]


@typechecked
def expects_gt_neg2dot0(value: Gt_neg2dot0) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [-1.2, 3.0, 6.0, 7.0, 8.0, 9.0],
)
def test_Gt_neg2dot0_accepts_valid_value(valid_case):
    expects_gt_neg2dot0(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (-5.0, -6.0, -7.0)
    ],
    # + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Gt_neg2dot0_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Gt_neg2dot0)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_gt_neg2dot0(value)
