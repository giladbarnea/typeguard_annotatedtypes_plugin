import functools
import typing
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Literal, Optional, TypeVar, Union

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

ConstraintType = Union[
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


# region debug
INDENT_COUNT = 0


def print_input_output(func):
    __tracebackhide__ = True

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global INDENT_COUNT
        __tracebackhide__ = True
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
        if isinstance(result, functools.partial):
            result_str = f"{result.func.__name__}(..., {', '.join(f'{k}={v!r}' for k, v in result.keywords.items())})"
            print(
                f"{indent}\033[38;5;{color}m⬅️  {func.__name__} ==> {result_str}\033[0m"
            )
        else:
            print(f"{indent}\033[38;5;{color}m⬅️  {func.__name__} ==> {result!r}\033[0m")
        return result

    return wrapper


def on_exception_return_none(func):
    __tracebackhide__ = True

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:  # noqa: E722
            return None

    return wrapper


R = TypeVar("R")


def partial(func: Callable[..., R], *args: Any, **kwargs: Any):
    partial_function: functools.partial[R] = functools.partial(func, *args, **kwargs)
    wrapper = functools.wraps(func)
    return wrapper(partial_function)


# endregion


# region checkers
Constraint = TypeVar("Constraint", bound=ConstraintType)
CheckerFn = Callable[[Any, Any, tuple[Any, ...], TypeCheckMemo, Constraint], bool]


def type_checker(checker: CheckerFn[Constraint]) -> CheckerFn[Constraint]:
    @functools.wraps(checker)
    def wrapper(
        value: Any,
        origin_type: Any,
        args: tuple[Any, ...],
        memo: TypeCheckMemo,
        constraint: Constraint,
    ) -> Literal[True]:
        # check_type(
        #     value,
        #     origin_type,
        #     forward_ref_policy=memo.config.forward_ref_policy,
        #     typecheck_fail_callback=memo.config.typecheck_fail_callback,
        #     collection_check_strategy=memo.config.collection_check_strategy,
        # )
        try:
            check_ok = checker(value, origin_type, args, memo, constraint)
        except Exception as e:
            raise TypeCheckError(f"with {value=!r} raised an error: {e!r}") from None
        else:
            if not check_ok:
                raise TypeCheckError(f"with {value=!r} failed {constraint}")
            return True

    return wrapper


@type_checker
def check_gt(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: annotated_types.Gt,
) -> bool:
    assert isinstance(constraint, annotated_types.Gt)
    return value > constraint.gt


@type_checker
def check_lt(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: annotated_types.Lt,
) -> bool:
    assert isinstance(constraint, annotated_types.Lt)
    return value < constraint.lt


@type_checker
def check_ge(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: annotated_types.Ge,
) -> bool:
    assert isinstance(constraint, annotated_types.Ge)
    return value >= constraint.ge


@type_checker
def check_le(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: annotated_types.Le,
) -> bool:
    assert isinstance(constraint, annotated_types.Le)
    return value <= constraint.le


@type_checker
def check_multiple_of(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: annotated_types.MultipleOf,
) -> bool:
    assert isinstance(constraint, annotated_types.MultipleOf)
    return value % constraint.multiple_of == 0


@type_checker
def check_len(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: Union[slice, annotated_types.Len],
) -> bool:
    if isinstance(constraint, slice):
        constraint = annotated_types.Len(constraint.start or 0, constraint.stop)
    assert isinstance(constraint, annotated_types.Len)
    if constraint.min_inclusive is None:
        raise TypeError
    if len(value) < constraint.min_inclusive:
        return False
    if constraint.max_exclusive is not None and len(value) >= constraint.max_exclusive:
        return False
    return True


@type_checker
def check_timezone(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: annotated_types.Timezone,
) -> None:
    assert isinstance(constraint, annotated_types.Timezone)
    assert isinstance(value, datetime)
    if isinstance(constraint.tz, str):
        return value.tzinfo is not None and constraint.tz == value.tzname()
    elif isinstance(constraint.tz, timezone):
        return value.tzinfo is not None and value.tzinfo == constraint.tz
    elif constraint.tz is None:
        return value.tzinfo is None
    # ellipsis
    return value.tzinfo is not None


@type_checker
def check_predicate(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: Predicate,
) -> None:
    assert isinstance(constraint, Predicate)
    return constraint.func(value)


# endregion

VALIDATORS: dict[ConstraintType, CheckerFn] = {
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


@print_input_output
def check_annotated_type(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    *,
    annotated_type: Constraint,
) -> None:
    checker = VALIDATORS[type(annotated_type)]
    checker(value, origin_type, args, memo, annotated_type)


@print_input_output
def match_annotated_type(
    origin_type, *instances
) -> Optional[tuple[Constraint, ConstraintType]]:
    for annotated_type in TYPE_CONSTRAINTS:
        if typing.get_origin(annotated_type) is typing.Annotated:
            extras = typing.get_args(annotated_type)
            predicate: ConstraintType = extras[1]
            # annotated_type_extras: list[tuple[Constraint, ConstraintType]] = list(
            #     filter(None, [match_annotated_type(extra) for extra in extras])
            # )
            # if not annotated_type_extras or len(annotated_type_extras) > 1:
            #     raise NotImplementedError(
            #         f"Don't know how to handle {annotated_type} with extras {extras}; "
            #         "only one annotated_type extra is supported"
            #     )
            # return annotated_type_extras[0]
            if isinstance(origin_type, predicate) or issubclass(origin_type, predicate):
                return origin_type, predicate
        if issubclass(origin_type, annotated_type):
            return origin_type, annotated_type
        assert not isinstance(origin_type, annotated_type), (
            f"origin_type {origin_type} ({type(origin_type)}) is an instance of {annotated_type} ({type(annotated_type)}), "
            "I assumed this can never happen"
        )
        for instance in instances:
            instance_type = type(instance)
            if issubclass(instance_type, annotated_type):
                assert isinstance(
                    instance, annotated_type
                ), "Well, the issubclass cant be replaced by isinstance"
                return instance, annotated_type
            assert not isinstance(instance_type, annotated_type), (
                f"instance_type {instance_type} ({type(instance_type)}) is an instance of {annotated_type} ({type(annotated_type)}), "
                "I assumed this can never happen"
            )
    return None


@print_input_output
def annotated_type_lookup(
    origin_type: Any, args: tuple[Any, ...], extras: tuple[Any, ...]
) -> Optional[functools.partial[Literal[None]]]:
    annotated_type = None
    if not (annotated_type := match_annotated_type(origin_type, *args, *extras)):
        return None

    constraint, constraint_type = annotated_type
    return partial(check_annotated_type, annotated_type=constraint)


checker_lookup_functions.extend(
    [
        # predicate_checker_lookup,
        annotated_type_lookup,
    ]
)
