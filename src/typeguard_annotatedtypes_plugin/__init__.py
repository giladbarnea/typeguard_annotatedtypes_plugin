import functools
import typing
from datetime import datetime, timezone
from typing import Any, Callable, Optional, TypeVar, Union

import annotated_types as at
from typeguard import (
    TypeCheckError,
    TypeCheckMemo,
    checker_lookup_functions,
)

from .util import print_input_output

# HashableNot = dataclass(Not, frozen=True)

# ConstraintType = Union[
#     BaseMetadata,
#     GroupedMetadata,
#     # HashableNot,
#     Predicate,
#     LowerCase,
#     UpperCase,
#     IsDigit,
#     IsDigits,
#     IsAscii,
#     IsFinite,
#     # IsNotFinite,
#     IsNan,
#     # IsNotNan,
#     IsInfinite,
#     # IsNotInfinite,
# ]
TYPE_CONSTRAINTS = (
    at.Ge,
    at.Gt,
    at.Interval,
    at.IsAscii,
    at.IsDigit,
    at.IsDigits,
    at.IsFinite,
    at.IsInfinite,
    at.IsNan,
    at.IsNotFinite,
    at.IsNotInfinite,
    at.IsNotNan,
    at.Le,
    at.Len,
    at.LowerCase,
    at.Lt,
    at.MaxLen,
    at.MinLen,
    at.MultipleOf,
    at.Not,
    at.Predicate,
    at.Timezone,
    at.Unit,
    at.UpperCase,
)


R = TypeVar("R")


# def partial(func: Callable[..., R], *args: Any, **kwargs: Any):
#     partial_function: functools.partial[R] = functools.partial(func, *args, **kwargs)
#     wrapper = functools.wraps(func)
#     return wrapper(partial_function)


# region checkers
Constraint = TypeVar(
    "Constraint",
    # bound=ConstraintType
)
CheckerFn = Callable[[Any, Any, tuple[Any, ...], TypeCheckMemo, Constraint], bool]


def type_checker(checker):
    @functools.wraps(checker)
    def wrapper(
        value,
        origin_type,
        args,
        memo,
        constraint,
    ):
        # check_type(
        #     value,
        #     origin_type,
        #     forward_ref_policy=memo.config.forward_ref_policy,
        #     typecheck_fail_callback=memo.config.typecheck_fail_callback,
        #     collection_check_strategy=memo.config.collection_check_strategy,
        # )
        # tg.check_type_internal(
        #     value,
        #     origin_type,
        #     memo
        # )
        if not isinstance(value, origin_type):
            raise TypeCheckError(
                f"{value!r} is not an instance of {origin_type.__name__}"
            )
        try:
            check_ok = checker(value, origin_type, args, memo, constraint)
        except Exception as e:
            raise TypeCheckError(f"with value={value!r} raised an error: {e!r}")
        else:
            if not check_ok:
                raise TypeCheckError(f"with value={value!r} failed {constraint}")
            return True

    return wrapper


@type_checker
def check_gt(
    value,
    origin_type,
    args,
    memo,
    constraint: at.Gt,
) -> bool:
    return value > constraint.gt


@type_checker
def check_lt(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: at.Lt,
) -> bool:
    return value < constraint.lt


@type_checker
def check_ge(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: at.Ge,
) -> bool:
    return value >= constraint.ge


@type_checker
def check_le(
    value,
    origin_type,
    args,
    memo,
    constraint: at.Le,
) -> bool:
    return value <= constraint.le


@type_checker
def check_multiple_of(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: at.MultipleOf,
) -> bool:
    assert isinstance(constraint, at.MultipleOf)
    return value % constraint.multiple_of == 0


@type_checker
def check_len(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: Union[slice, at.Len],
) -> bool:
    if isinstance(constraint, slice):
        constraint = at.Len(constraint.start or 0, constraint.stop)
    assert isinstance(constraint, at.Len)
    if constraint.min_inclusive is None:
        raise TypeError
    if len(value) < constraint.min_inclusive:
        return False
    return not (
        constraint.max_exclusive is not None and len(value) >= constraint.max_exclusive
    )


@type_checker
def check_timezone(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: at.Timezone,
) -> None:
    assert isinstance(constraint, at.Timezone)
    assert isinstance(value, datetime)
    if isinstance(constraint.tz, str):
        return value.tzinfo is not None and constraint.tz == value.tzname()
    elif isinstance(constraint.tz, timezone):
        return value.tzinfo is not None and value.tzinfo == constraint.tz
    elif constraint.tz is None:
        return value.tzinfo is None
    # ellipsis
    return value.tzinfo is not None


# @type_checker
def check_predicate(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    constraint: at.Predicate,
) -> None:
    try:
        check_ok = constraint.func(value)
        # check_ok = checker(value, origin_type, args, memo, constraint)
    except Exception as e:
        raise TypeCheckError(f"with {value=!r} raised an error: {e!r}") from None
    else:
        if not check_ok:
            raise TypeCheckError(f"with {value=!r} failed {constraint}")
        return True
    # assert isinstance(constraint, Predicate)
    # return constraint.func(value)


# endregion

VALIDATORS: dict[Any, CheckerFn] = {
    at.Gt: check_gt,
    at.Lt: check_lt,
    at.Ge: check_ge,
    at.Le: check_le,
    at.MultipleOf: check_multiple_of,
    at.Predicate: check_predicate,
    at.Len: check_len,
    at.Timezone: check_timezone,
    slice: check_len,
}


# @print_input_output
def check_annotated_type(
    value,
    origin_type,
    args,
    memo,
    *,
    annotated_type,
) -> None:
    checker = VALIDATORS[type(annotated_type)]
    checker(value, origin_type, args, memo, annotated_type)


@print_input_output
def match_annotated_type(origin_type, *instances) -> Optional[tuple]:
    for annotated_type in TYPE_CONSTRAINTS:
        if typing.get_origin(annotated_type) is typing.Annotated:
            extras = typing.get_args(annotated_type)
            predicate: Any = extras[1]
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
                assert isinstance(instance, annotated_type), (
                    "Well, the issubclass cant be replaced by isinstance"
                )
                return instance, annotated_type
            assert not isinstance(instance_type, annotated_type), (
                f"instance_type {instance_type} ({type(instance_type)}) is an instance of {annotated_type} ({type(annotated_type)}), "
                "I assumed this can never happen"
            )
    return None


@print_input_output
def annotated_type_lookup(origin_type, args, extras):
    annotated_type = None
    if not (annotated_type := match_annotated_type(origin_type, *args, *extras)):
        return None

    constraint, _constraint_type = annotated_type
    return functools.partial(check_annotated_type, annotated_type=constraint)


checker_lookup_functions.insert(0, annotated_type_lookup)
