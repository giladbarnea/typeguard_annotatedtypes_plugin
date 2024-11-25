from datetime import datetime, timezone
from functools import partial
from typing import Any, Optional

import annotated_types
from annotated_types import BaseMetadata, Predicate
from typeguard import (
    TypeCheckError,
    TypeCheckMemo,
    check_type,
    checker_lookup_functions,
)


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


def check_annotated_type(
    value: Any,
    origin_type: Any,
    args: tuple[Any, ...],
    memo: TypeCheckMemo,
    *,
    annotated_type: BaseMetadata,
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


def basemetadata_checker_lookup(
    origin_type: Any, args: tuple[Any, ...], extras: tuple[Any, ...]
) -> Optional[partial[None]]:
    annotated_type = None
    if isinstance(origin_type, BaseMetadata):
        annotated_type = origin_type
    elif not (
        annotated_type := next(
            (extra for extra in extras if isinstance(extra, BaseMetadata)), None
        )
    ):
        return None

    return partial(check_annotated_type, annotated_type=annotated_type)


checker_lookup_functions.extend(
    [
        predicate_checker_lookup,
        basemetadata_checker_lookup,
    ]
)
