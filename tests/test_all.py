import math
import re
import typing
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Annotated, Dict, Iterator, List, Set, Tuple

import annotated_types as at
import pytest
import typeguard
from typeguard import typechecked

import typeguard_annotatedtypes_plugin  # type: ignore # noqa: F401


class MyCustomGroupedMetadata(at.GroupedMetadata):
    def __iter__(self) -> Iterator[at.Predicate]:
        yield at.Predicate(lambda x: float(x).is_integer())


Gt4 = Annotated[int, at.Gt(4)]


@typechecked
def expects_gt4(value: Gt4) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (5, 6, 1000),
)
def test_Gt4_accepts_valid_value(valid_case):
    expects_gt4(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (4, 0, -1)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Gt4_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Gt4)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_gt4(value)


Gt0_5 = Annotated[float, at.Gt(0.5)]


@typechecked
def expects_gt0_5(value: Gt0_5) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (0.6, 0.7, 0.8, 0.9),
)
def test_Gt0_5_accepts_valid_value(valid_case):
    expects_gt0_5(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (0.5, 0.0, -0.1)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Gt0_5_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Gt0_5)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_gt0_5(value)


Gtdatetime2000_1_1 = Annotated[datetime, at.Gt(datetime(2000, 1, 1))]


@typechecked
def expects_gtdatetime2000_1_1(value: Gtdatetime2000_1_1) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [datetime(2000, 1, 2), datetime(2000, 1, 3)],
)
def test_Gtdatetime2000_1_1_accepts_valid_value(valid_case):
    expects_gtdatetime2000_1_1(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [datetime(2000, 1, 1), datetime(1999, 12, 31)]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Gtdatetime2000_1_1_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Gtdatetime2000_1_1)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_gtdatetime2000_1_1(value)


Gtdate2000_1_1 = Annotated[datetime, at.Gt(date(2000, 1, 1))]


@typechecked
def expects_gtdate2000_1_1(value: Gtdate2000_1_1) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [date(2000, 1, 2), date(2000, 1, 3)],
)
def test_Gtdate2000_1_1_accepts_valid_value(valid_case):
    expects_gtdate2000_1_1(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [date(2000, 1, 1), date(1999, 12, 31)]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Gtdate2000_1_1_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Gtdate2000_1_1)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_gtdate2000_1_1(value)


GtDecimal1_123 = Annotated[datetime, at.Gt(Decimal("1.123"))]


@typechecked
def expects_gtdecimal1_123(value: GtDecimal1_123) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [Decimal("1.1231"), Decimal("123")],
)
def test_GtDecimal1_123_accepts_valid_value(valid_case):
    expects_gtdecimal1_123(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [Decimal("1.123"), Decimal("0")]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_GtDecimal1_123_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(GtDecimal1_123)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_gtdecimal1_123(value)


Ge4 = Annotated[int, at.Ge(4)]


@typechecked
def expects_ge4(value: Ge4) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (4, 5, 6, 1000, 4),
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
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Ge4_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Ge4)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_ge4(value)


Ge0_5 = Annotated[float, at.Ge(0.5)]


@typechecked
def expects_ge0_5(value: Ge0_5) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (0.5, 0.6, 0.7, 0.8, 0.9),
)
def test_Ge0_5_accepts_valid_value(valid_case):
    expects_ge0_5(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (0.4, 0.0, -0.1)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Ge0_5_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Ge0_5)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_ge0_5(value)


Gedatetime2000_1_1 = Annotated[datetime, at.Ge(datetime(2000, 1, 1))]


@typechecked
def expects_gedatetime2000_1_1(value: Gedatetime2000_1_1) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [datetime(2000, 1, 2), datetime(2000, 1, 3)],
)
def test_Gedatetime2000_1_1_accepts_valid_value(valid_case):
    expects_gedatetime2000_1_1(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [datetime(1998, 1, 1), datetime(1999, 12, 31)]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Gedatetime2000_1_1_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Gedatetime2000_1_1)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_gedatetime2000_1_1(value)


Lt4 = Annotated[int, at.Lt(4)]


@typechecked
def expects_lt4(value: Lt4) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (0, -1),
)
def test_Lt4_accepts_valid_value(valid_case):
    expects_lt4(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (4, 5, 6, 1000, 4)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Lt4_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Lt4)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_lt4(value)


Lt0_5 = Annotated[float, at.Lt(0.5)]


@typechecked
def expects_lt0_5(value: Lt0_5) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (0.4, 0.0, -0.1),
)
def test_Lt0_5_accepts_valid_value(valid_case):
    expects_lt0_5(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (0.5, 0.6, 0.7, 0.8, 0.9)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Lt0_5_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Lt0_5)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_lt0_5(value)


Ltdatetime2000_1_1 = Annotated[datetime, at.Lt(datetime(2000, 1, 1))]


@typechecked
def expects_ltdatetime2000_1_1(value: Ltdatetime2000_1_1) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [datetime(1999, 12, 31), datetime(1999, 12, 31)],
)
def test_Ltdatetime2000_1_1_accepts_valid_value(valid_case):
    expects_ltdatetime2000_1_1(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [datetime(2000, 1, 2), datetime(2000, 1, 3)]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Ltdatetime2000_1_1_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Ltdatetime2000_1_1)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_ltdatetime2000_1_1(value)


Le4 = Annotated[int, at.Le(4)]


@typechecked
def expects_le4(value: Le4) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (4, 0, -1),
)
def test_Le4_accepts_valid_value(valid_case):
    expects_le4(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (5, 6, 1000)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Le4_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Le4)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_le4(value)


Le0_5 = Annotated[float, at.Le(0.5)]


@typechecked
def expects_le0_5(value: Le0_5) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (0.5, 0.0, -0.1),
)
def test_Le0_5_accepts_valid_value(valid_case):
    expects_le0_5(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (0.6, 0.7, 0.8, 0.9)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Le0_5_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Le0_5)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_le0_5(value)


Ledatetime2000_1_1 = Annotated[datetime, at.Le(datetime(2000, 1, 1))]


@typechecked
def expects_ledatetime2000_1_1(value: Ledatetime2000_1_1) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [datetime(2000, 1, 1), datetime(1999, 12, 31)],
)
def test_Ledatetime2000_1_1_accepts_valid_value(valid_case):
    expects_ledatetime2000_1_1(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [datetime(2000, 1, 2), datetime(2000, 1, 3)]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Ledatetime2000_1_1_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Ledatetime2000_1_1)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_ledatetime2000_1_1(value)


Interval_gt4 = Annotated[int, at.Interval(gt=4)]


@typechecked
def expects_interval_gt4(value: Interval_gt4) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (5, 6, 1000),
)
def test_Interval_gt4_accepts_valid_value(valid_case):
    expects_interval_gt4(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (4, 0, -1)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Interval_gt4_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Interval_gt4)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_interval_gt4(value)


Interval_gt4_lt10 = Annotated[int, at.Interval(gt=4, lt=10)]


@typechecked
def expects_interval_gt4_lt10(value: Interval_gt4_lt10) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (5, 6),
)
def test_Interval_gt4_lt10_accepts_valid_value(valid_case):
    expects_interval_gt4_lt10(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (4, 10, 1000, 0, -1)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Interval_gt4_lt10_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Interval_gt4_lt10)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_interval_gt4_lt10(value)


Interval_ge0_5_le1 = Annotated[float, at.Interval(ge=0.5, le=1)]


@typechecked
def expects_interval_ge0_5_le1(value: Interval_ge0_5_le1) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (0.5, 0.9, 1),
)
def test_Interval_ge0_5_le1_accepts_valid_value(valid_case):
    expects_interval_ge0_5_le1(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (0.49, 1.1)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Interval_ge0_5_le1_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Interval_ge0_5_le1)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_interval_ge0_5_le1(value)


Interval_gtdatetime2000_1_1_ledatetime2000_1_3 = Annotated[
    datetime, at.Interval(gt=datetime(2000, 1, 1), le=datetime(2000, 1, 3))
]


@typechecked
def expects_interval_gtdatetime2000_1_1_ledatetime2000_1_3(
    value: Interval_gtdatetime2000_1_1_ledatetime2000_1_3,
) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [datetime(2000, 1, 2), datetime(2000, 1, 3)],
)
def test_Interval_gtdatetime2000_1_1_ledatetime2000_1_3_accepts_valid_value(valid_case):
    expects_interval_gtdatetime2000_1_1_ledatetime2000_1_3(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [datetime(2000, 1, 1), datetime(2000, 1, 4)]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Interval_gtdatetime2000_1_1_ledatetime2000_1_3_raises_TypeCheckError(
    invalid_case,
):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Interval_gtdatetime2000_1_1_ledatetime2000_1_3)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_interval_gtdatetime2000_1_1_ledatetime2000_1_3(value)


MultipleOf_multiple_of3 = Annotated[int, at.MultipleOf(multiple_of=3)]


@typechecked
def expects_multipleof_multiple_of3(value: MultipleOf_multiple_of3) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (0, 3, 9),
)
def test_MultipleOf_multiple_of3_accepts_valid_value(valid_case):
    expects_multipleof_multiple_of3(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (1, 2, 4)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_MultipleOf_multiple_of3_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(MultipleOf_multiple_of3)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_multipleof_multiple_of3(value)


MultipleOf_multiple_of0_5 = Annotated[float, at.MultipleOf(multiple_of=0.5)]


@typechecked
def expects_multipleof_multiple_of0_5(value: MultipleOf_multiple_of0_5) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (0, 0.5, 1, 1.5),
)
def test_MultipleOf_multiple_of0_5_accepts_valid_value(valid_case):
    expects_multipleof_multiple_of0_5(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (0.4, 1.1)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_MultipleOf_multiple_of0_5_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(MultipleOf_multiple_of0_5)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_multipleof_multiple_of0_5(value)


MinLen3 = Annotated[str, at.MinLen(3)]


@typechecked
def expects_minlen3(value: MinLen3) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ("123", "1234", "x" * 10),
)
def test_MinLen3_accepts_valid_value(valid_case):
    expects_minlen3(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ("", "1", "12")
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_MinLen3_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(MinLen3)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_minlen3(value)


Len3 = Annotated[str, at.Len(3)]


@typechecked
def expects_len3(value: Len3) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ("123", "1234", "x" * 10),
)
def test_Len3_accepts_valid_value(valid_case):
    expects_len3(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ("", "1", "12")
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Len3_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Len3)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_len3(value)


MinLen3 = Annotated[List[int], at.MinLen(3)]


@typechecked
def expects_minlen3(value: MinLen3) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ([1, 2, 3], [1, 2, 3, 4], [1] * 10),
)
def test_MinLen3_accepts_valid_value(valid_case):
    expects_minlen3(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ([], [1], [1, 2])
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_MinLen3_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(MinLen3)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_minlen3(value)


Len3 = Annotated[List[int], at.Len(3)]


@typechecked
def expects_len3(value: Len3) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ([1, 2, 3], [1, 2, 3, 4], [1] * 10),
)
def test_Len3_accepts_valid_value(valid_case):
    expects_len3(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ([], [1], [1, 2])
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Len3_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Len3)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_len3(value)


MaxLen4 = Annotated[str, at.MaxLen(4)]


@typechecked
def expects_maxlen4(value: MaxLen4) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ("", "1234"),
)
def test_MaxLen4_accepts_valid_value(valid_case):
    expects_maxlen4(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ("12345", "x" * 10)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_MaxLen4_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(MaxLen4)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_maxlen4(value)


Len0 = Annotated[str, at.Len(0, 4)]


@typechecked
def expects_len0(value: Len0) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ("", "1234"),
)
def test_Len0_accepts_valid_value(valid_case):
    expects_len0(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ("12345", "x" * 10)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Len0_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Len0)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_len0(value)


MaxLen4 = Annotated[List[str], at.MaxLen(4)]


@typechecked
def expects_maxlen4(value: MaxLen4) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ([], ["a", "bcdef"], ["a", "b", "c"]),
)
def test_MaxLen4_accepts_valid_value(valid_case):
    expects_maxlen4(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (["a"] * 5, ["b"] * 10)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_MaxLen4_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(MaxLen4)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_maxlen4(value)


Len0 = Annotated[List[str], at.Len(0, 4)]


@typechecked
def expects_len0(value: Len0) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ([], ["a", "bcdef"], ["a", "b", "c"]),
)
def test_Len0_accepts_valid_value(valid_case):
    expects_len0(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (["a"] * 5, ["b"] * 10)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Len0_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Len0)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_len0(value)


Len3 = Annotated[str, at.Len(3, 5)]


@typechecked
def expects_len3(value: Len3) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ("123", "12345"),
)
def test_Len3_accepts_valid_value(valid_case):
    expects_len3(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ("", "1", "12", "123456", "x" * 10)
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Len3_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Len3)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_len3(value)


Len3 = Annotated[str, at.Len(3, 3)]


@typechecked
def expects_len3(value: Len3) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ("123",),
)
def test_Len3_accepts_valid_value(valid_case):
    expects_len3(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ("12", "1234")
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Len3_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Len3)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_len3(value)


Len2 = Annotated[Dict[int, int], at.Len(2, 3)]


@typechecked
def expects_len2(value: Len2) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [{(1): 1, (2): 2}],
)
def test_Len2_accepts_valid_value(valid_case):
    expects_len2(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [{}, {(1): 1}, {(1): 1, (2): 2, (3): 3, (4): 4}]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Len2_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Len2)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_len2(value)


Len2 = Annotated[Set[int], at.Len(2, 3)]


@typechecked
def expects_len2(value: Len2) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ({1, 2}, {1, 2, 3}),
)
def test_Len2_accepts_valid_value(valid_case):
    expects_len2(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in (set(), {1}, {1, 2, 3, 4})
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Len2_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Len2)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_len2(value)


Len2 = Annotated[Tuple[int, ...], at.Len(2, 3)]


@typechecked
def expects_len2(value: Len2) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ((1, 2), (1, 2, 3)),
)
def test_Len2_accepts_valid_value(valid_case):
    expects_len2(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ((), (1,), (1, 2, 3, 4))
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Len2_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Len2)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_len2(value)


TimezoneNone = Annotated[datetime, at.Timezone(None)]


@typechecked
def expects_timezonenone(value: TimezoneNone) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [datetime(2000, 1, 1)],
)
def test_TimezoneNone_accepts_valid_value(valid_case):
    expects_timezonenone(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [datetime(2000, 1, 1, tzinfo=timezone.utc)]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_TimezoneNone_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(TimezoneNone)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_timezonenone(value)


Timezone___ = Annotated[datetime, at.Timezone(...)]


@typechecked
def expects_timezone___(value: Timezone___) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [datetime(2000, 1, 1, tzinfo=timezone.utc)],
)
def test_Timezone____accepts_valid_value(valid_case):
    expects_timezone___(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [datetime(2000, 1, 1)]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Timezone____raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Timezone___)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_timezone___(value)


Timezonetimezone_utc = Annotated[datetime, at.Timezone(timezone.utc)]


@typechecked
def expects_timezonetimezone_utc(value: Timezonetimezone_utc) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [datetime(2000, 1, 1, tzinfo=timezone.utc)],
)
def test_Timezonetimezone_utc_accepts_valid_value(valid_case):
    expects_timezonetimezone_utc(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [
            datetime(2000, 1, 1),
            datetime(2000, 1, 1, tzinfo=timezone(timedelta(hours=6))),
        ]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Timezonetimezone_utc_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Timezonetimezone_utc)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_timezonetimezone_utc(value)


TimezoneEuropeLondon = Annotated[datetime, at.Timezone("Europe/London")]


@typechecked
def expects_timezoneeuropelondon(value: TimezoneEuropeLondon) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [datetime(2000, 1, 1, tzinfo=timezone(timedelta(0), name="Europe/London"))],
)
def test_TimezoneEuropeLondon_accepts_valid_value(valid_case):
    expects_timezoneeuropelondon(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [
            datetime(2000, 1, 1),
            datetime(2000, 1, 1, tzinfo=timezone(timedelta(hours=6))),
        ]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_TimezoneEuropeLondon_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(TimezoneEuropeLondon)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_timezoneeuropelondon(value)


Unit_unitm = Annotated[float, at.Unit(unit="m")]


@typechecked
def expects_unit_unitm(value: Unit_unitm) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    (5, 4.2),
)
def test_Unit_unitm_accepts_valid_value(valid_case):
    expects_unit_unitm(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ("5m", "4.2m")
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Unit_unitm_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Unit_unitm)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_unit_unitm(value)


LowerCase = at.LowerCase[str]


@typechecked
def expects_lowercase(value: LowerCase) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ["abc", "foobar"],
)
def test_LowerCase_accepts_valid_value(valid_case):
    expects_lowercase(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ["", "A", "Boom"]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_LowerCase_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(LowerCase)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_lowercase(value)


UpperCase = at.UpperCase[str]


@typechecked
def expects_uppercase(value: UpperCase) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ["ABC", "DEFO"],
)
def test_UpperCase_accepts_valid_value(valid_case):
    expects_uppercase(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ["", "a", "abc", "AbC"]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_UpperCase_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(UpperCase)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_uppercase(value)


IsDigit = at.IsDigit[str]


@typechecked
def expects_isdigit(value: IsDigit) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ["123"],
)
def test_IsDigit_accepts_valid_value(valid_case):
    expects_isdigit(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ["", "ab", "a1b2"]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_IsDigit_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(IsDigit)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_isdigit(value)


IsAscii = at.IsAscii[str]


@typechecked
def expects_isascii(value: IsAscii) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    ["123", "foo bar"],
)
def test_IsAscii_accepts_valid_value(valid_case):
    expects_isascii(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in ["£100", "😊", "whatever 👀"]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_IsAscii_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(IsAscii)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_isascii(value)


Predicatelambdaxx20 = Annotated[int, at.Predicate(lambda x: x % 2 == 0)]


@typechecked
def expects_predicatelambdaxx20(value: Predicatelambdaxx20) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [0, 2, 4],
)
def test_Predicatelambdaxx20_accepts_valid_value(valid_case):
    expects_predicatelambdaxx20(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [1, 3, 5]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_Predicatelambdaxx20_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(Predicatelambdaxx20)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_predicatelambdaxx20(value)


IsFinite = at.IsFinite[float]


@typechecked
def expects_isfinite(value: IsFinite) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [1.23],
)
def test_IsFinite_accepts_valid_value(valid_case):
    expects_isfinite(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [math.nan, math.inf, -math.inf]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_IsFinite_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(IsFinite)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_isfinite(value)


IsNotFinite = at.IsNotFinite[float]


@typechecked
def expects_isnotfinite(value: IsNotFinite) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [math.nan, math.inf],
)
def test_IsNotFinite_accepts_valid_value(valid_case):
    expects_isnotfinite(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [1.23]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_IsNotFinite_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(IsNotFinite)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_isnotfinite(value)


IsNan = at.IsNan[float]


@typechecked
def expects_isnan(value: IsNan) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [math.nan],
)
def test_IsNan_accepts_valid_value(valid_case):
    expects_isnan(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [1.23, math.inf]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_IsNan_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(IsNan)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_isnan(value)


IsNotNan = at.IsNotNan[float]


@typechecked
def expects_isnotnan(value: IsNotNan) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [1.23, math.inf],
)
def test_IsNotNan_accepts_valid_value(valid_case):
    expects_isnotnan(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [math.nan]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_IsNotNan_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(IsNotNan)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_isnotnan(value)


IsInfinite = at.IsInfinite[float]


@typechecked
def expects_isinfinite(value: IsInfinite) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [math.inf],
)
def test_IsInfinite_accepts_valid_value(valid_case):
    expects_isinfinite(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [math.nan, 1.23]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_IsInfinite_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(IsInfinite)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_isinfinite(value)


IsNotInfinite = at.IsNotInfinite[float]


@typechecked
def expects_isnotinfinite(value: IsNotInfinite) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [math.nan, 1.23],
)
def test_IsNotInfinite_accepts_valid_value(valid_case):
    expects_isnotinfinite(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [math.inf]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_IsNotInfinite_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(IsNotInfinite)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_isnotinfinite(value)


IsInfinite = at.IsInfinite[Annotated[float, at.Predicate(lambda x: x > 0)]]


@typechecked
def expects_isinfinite(value: IsInfinite) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [math.inf],
)
def test_IsInfinite_accepts_valid_value(valid_case):
    expects_isinfinite(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [-math.inf, 1.23, math.nan]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_IsInfinite_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(IsInfinite)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_isinfinite(value)


docAnumber = Annotated[int, at.doc("A number")]


@typechecked
def expects_docanumber(value: docAnumber) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [1, 2],
)
def test_docAnumber_accepts_valid_value(valid_case):
    expects_docanumber(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in []
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_docAnumber_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(docAnumber)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_docanumber(value)


MyCustomGroupedMetadata = Annotated[float, MyCustomGroupedMetadata()]


@typechecked
def expects_mycustomgroupedmetadata(value: MyCustomGroupedMetadata) -> None:
    pass


@pytest.mark.parametrize(
    "valid_case",
    [0, 2.0],
)
def test_MyCustomGroupedMetadata_accepts_valid_value(valid_case):
    expects_mycustomgroupedmetadata(valid_case)


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(
            value=invalid_value,
            match="with value={value!r} failed {annotated_type}",
        )
        for invalid_value in [0.01, 1.5]
    ]
    + [dict(value="hi", match="(str) is not an instance of int")],
)
def test_MyCustomGroupedMetadata_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    annotated_type = typing.get_args(MyCustomGroupedMetadata)[1]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(
            re.escape(match.format(value=value, annotated_type=annotated_type))
        ),
    ):
        expects_mycustomgroupedmetadata(value)
