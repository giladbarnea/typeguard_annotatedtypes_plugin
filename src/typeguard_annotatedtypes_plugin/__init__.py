from functools import partial
from typing import Any, Optional

from annotated_types import Predicate
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
        check_failed = not predicate.func(value)
    except Exception as e:
        raise TypeCheckError(f"with {value=!r} raised an error: {e!r}")
    else:
        if check_failed:
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


checker_lookup_functions.append(predicate_checker_lookup)
