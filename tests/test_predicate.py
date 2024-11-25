import re
from typing import Annotated

import pytest
import typeguard
from annotated_types import Predicate
from typeguard import typechecked

import typeguard_annotatedtypes_plugin  # noqa: F401


def _is_glob(path: str) -> bool:
    return "*" in path or "?" in path


predicate = Predicate(_is_glob)
TGlob = Annotated[str, predicate]


def test_predicate():
    @typechecked
    def foo(value: TGlob) -> None:
        pass

    invalid_value = "hi"
    with pytest.raises(
        typeguard.TypeCheckError,
        match=re.compile(re.escape(f"with value='{invalid_value}' failed {predicate}")),
    ):
        foo("hi")
        
    valid_value = "hi*"
    foo(valid_value)
