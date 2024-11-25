from functools import partial
from typing import Any, Optional

from annotated_types import BaseMetadata, Predicate
from typeguard import (
    TypeCheckError,
    TypeCheckMemo,
    check_type,
    checker_lookup_functions,
)


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
        check_ok = value >= annotated_type.ge
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
