import typing
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import partial
from typing import Annotated, Any, Optional, Union

import annotated_types
from annotated_types import (
    BaseMetadata,
    Ge,
    GroupedMetadata,
    Gt,
    Interval,
    IsAscii,
    IsDigit,
    IsDigits,
    IsFinite,
    IsInfinite,
    IsNan,
    IsNotFinite,
    IsNotInfinite,
    IsNotNan,
    Le,
    Len,
    LowerCase,
    Lt,
    MaxLen,
    MinLen,
    MultipleOf,
    Not,
    Predicate,
    Timezone,
    Unit,
    UpperCase,
)
from typeguard import (
    TypeCheckError,
    TypeCheckMemo,
    check_type,
    checker_lookup_functions,
)

HashableNot = dataclass(Not, frozen=True)

Constraint = Union[
    BaseMetadata,
    GroupedMetadata,
    HashableNot,
    Predicate,
    LowerCase,
    UpperCase,
    IsDigit,
    IsDigits,
    IsAscii,
    IsFinite,
    IsNotFinite,
    IsNan,
    IsNotNan,
    IsInfinite,
    IsNotInfinite,
]
TYPE_CONSTRAINTS: tuple[
    BaseMetadata,
    GroupedMetadata,
    Not,
    Predicate,
    LowerCase,
    UpperCase,
    IsDigit,
    IsDigits,
    IsAscii,
    IsFinite,
    IsNotFinite,
    IsNan,
    IsNotNan,
    IsInfinite,
    IsNotInfinite,
] = (
    Ge,
    Gt,
    Interval,
    IsAscii,
    IsDigit,
    IsDigits,
    IsFinite,
    IsInfinite,
    IsNan,
    IsNotFinite,
    IsNotInfinite,
    IsNotNan,
    Le,
    Len,
    LowerCase,
    Lt,
    MaxLen,
    MinLen,
    MultipleOf,
    Not,
    Predicate,
    Timezone,
    Unit,
    UpperCase,
)


# region printer
INDENT_COUNT = 0


def print_input_output(func):
    def wrapper(*args, **kwargs):
        global INDENT_COUNT
        args_str = [f"{arg!r}" for arg in args]
        kwargs_str = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_args = ", ".join(args_str + kwargs_str)

        indent = "  " * INDENT_COUNT
        print(
            f"{indent}\033[38;5;246m➡️  {func.__name__}({all_args})\033[0m"
        )  # Gray color

        INDENT_COUNT += 1
        try:
            result = func(*args, **kwargs)
        finally:
            INDENT_COUNT -= 1

        indent = "  " * INDENT_COUNT
        color = "67" if result is None else "75"
        if isinstance(result, partial):
            result_str = f"{result.func.__name__}(..., {', '.join(f'{k}={v!r}' for k, v in result.keywords.items())})"
            print(
                f"{indent}\033[38;5;{color}m⬅️  {func.__name__} ==> {result_str}\033[0m"
            )
        else:
            print(f"{indent}\033[38;5;{color}m⬅️  {func.__name__} ==> {result!r}\033[0m")
        return result

    return wrapper


# endregion


# region checkers
def check_gt(constraint, val) -> bool:
    assert isinstance(constraint, annotated_types.Gt)
    return val > constraint.gt


def check_lt(constraint, val) -> bool:
    assert isinstance(constraint, annotated_types.Lt)
    return val < constraint.lt


def check_ge(constraint, val) -> bool:
    assert isinstance(constraint, annotated_types.Ge)
    return val >= constraint.ge


def check_le(constraint, val) -> bool:
    assert isinstance(constraint, annotated_types.Le)
    return val <= constraint.le


def check_multiple_of(constraint, val) -> bool:
    assert isinstance(constraint, annotated_types.MultipleOf)
    return val % constraint.multiple_of == 0


def check_len(constraint, val) -> bool:
    if isinstance(constraint, slice):
        constraint = annotated_types.Len(constraint.start or 0, constraint.stop)
    assert isinstance(constraint, annotated_types.Len)
    if constraint.min_inclusive is None:
        raise TypeError
    if len(val) < constraint.min_inclusive:
        return False
    if constraint.max_exclusive is not None and len(val) >= constraint.max_exclusive:
        return False
    return True


def check_predicate(constraint, val) -> bool:
    assert isinstance(constraint, annotated_types.Predicate)
    return constraint.func(val)


def check_timezone(constraint, val) -> bool:
    assert isinstance(constraint, annotated_types.Timezone)
    assert isinstance(val, datetime)
    if isinstance(constraint.tz, str):
        return val.tzinfo is not None and constraint.tz == val.tzname()
    elif isinstance(constraint.tz, timezone):
        return val.tzinfo is not None and val.tzinfo == constraint.tz
    elif constraint.tz is None:
        return val.tzinfo is None
    # ellipsis
    return val.tzinfo is not None


# endregion

VALIDATORS = {
    annotated_types.Gt: check_gt,
    annotated_types.Lt: check_lt,
    annotated_types.Ge: check_ge,
    annotated_types.Le: check_le,
    annotated_types.MultipleOf: check_multiple_of,
    annotated_types.Predicate: check_predicate,
    annotated_types.Len: check_len,
    annotated_types.Timezone: check_timezone,
    slice: check_len,
}


# region predicate
def check_predicate(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    *,
    predicate: Predicate,
) -> None:
    check_type(
        value,
        origin_type,
        forward_ref_policy=memo.config.forward_ref_policy,
        typecheck_fail_callback=memo.config.typecheck_fail_callback,
        collection_check_strategy=memo.config.collection_check_strategy,
    )
    try:
        check_ok = predicate.func(value)
    except Exception as e:
        raise TypeCheckError(f"with {value=!r} raised an error: {e!r}") from None
    else:
        if not check_ok:
            raise TypeCheckError(f"with {value=!r} failed {predicate}")


@print_input_output
def predicate_checker_lookup(
    origin_type: Any, args: tuple[Any, ...], extras: tuple[Any, ...]
) -> Optional[partial[None]]:
    predicate = None
    if isinstance(origin_type, Predicate):
        predicate = origin_type
    elif not (
        predicate := next(
            (extra for extra in extras if isinstance(extra, Predicate)), None
        )
    ):
        return None

    return partial(check_predicate, predicate=predicate)


# endregion


@print_input_output
def check_annotated_type(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    *,
    annotated_type: Constraint,
) -> None:
    check_type(
        value,
        origin_type,
        forward_ref_policy=memo.config.forward_ref_policy,
        typecheck_fail_callback=memo.config.typecheck_fail_callback,
        collection_check_strategy=memo.config.collection_check_strategy,
    )
    try:
        check_ok = VALIDATORS[type(annotated_type)](annotated_type, value)
    except Exception as e:
        raise TypeCheckError(f"with {value=!r} raised an error: {e!r}") from None
    else:
        if not check_ok:
            raise TypeCheckError(f"with {value=!r} failed {annotated_type}")


def on_exception_return_none(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:  # noqa: E722
            return None

    return wrapper


@on_exception_return_none
def match_annotated_type(origin_type, *instances) -> Optional[Constraint]:
    for annotated_type in TYPE_CONSTRAINTS:
        if typing.get_origin(annotated_type) is typing.Annotated:
            extras = typing.get_args(annotated_type)
            annotated_type_extras = list(
                filter(None, [match_annotated_type(extra) for extra in extras])
            )
            if not annotated_type_extras or len(annotated_type_extras) > 1:
                raise NotImplementedError(
                    f"Don't know how to handle {annotated_type} with extras {extras}; "
                    "only one annotated_type extra is supported"
                )
            return annotated_type_extras[0]
        if issubclass(origin_type, annotated_type):
            return annotated_type
        assert not isinstance(origin_type, annotated_type), (
            f"origin_type {origin_type} ({type(origin_type)}) is an instance of {annotated_type} ({type(annotated_type)}), "
            "I assumed this can never happen"
        )
        for instance_type in map(type, instances):
            if issubclass(instance_type, annotated_type):
                return annotated_type
            assert not isinstance(instance_type, annotated_type), (
                f"instance_type {instance_type} ({type(instance_type)}) is an instance of {annotated_type} ({type(annotated_type)}), "
                "I assumed this can never happen"
            )

    return None


@print_input_output
def annotated_type_lookup(
    origin_type: Any, args: tuple[Any, ...], extras: tuple[Any, ...]
) -> Optional[partial[None]]:
    annotated_type = None
    # if predicate := next(
    #     (extra for extra in (origin_type,) + extras if isinstance(extra, Predicate)),
    #     None,
    # ):
    #     return partial(
    #         check_predicate,
    #         predicate=predicate,
    #     )
    if not (annotated_type := match_annotated_type(origin_type, *args, *extras)):
        return None

    return partial(check_annotated_type, annotated_type=annotated_type)


checker_lookup_functions.extend(
    [
        # predicate_checker_lookup,
        annotated_type_lookup,
    ]
)
