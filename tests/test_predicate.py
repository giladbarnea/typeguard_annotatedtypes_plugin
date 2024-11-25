import re
from typing import Annotated

import pytest
import typeguard
from annotated_types import Predicate
from typeguard import typechecked

import typeguard_annotatedtypes_plugin  # type: ignore # noqa: F401


def _is_glob(path: str) -> bool:
    return "*" in path or "?" in path


predicate = Predicate(_is_glob)
TGlob = Annotated[str, predicate]


@typechecked
def foo(value: TGlob) -> None:
    pass


def test_predicate_accepts_valid_value():
    foo("hi*")


@pytest.mark.parametrize(
    "invalid_case",
    [
        dict(value="hi", match="with value='{value}' failed {predicate}"),
        dict(value=1, match="(int) is not an instance of str"),
    ],
)
def test_predicate_raises_TypeCheckError(invalid_case):
    value = invalid_case["value"]
    match = invalid_case["match"]
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(re.escape(match.format(value=value, predicate=predicate))),
    ):
        foo(value)
