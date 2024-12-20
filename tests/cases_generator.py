import ast
from dataclasses import dataclass
from typing import List

import astor


@dataclass
class ParsedCase:
    annotation: ast.AST
    valid_cases: ast.AST
    invalid_cases: ast.AST


class TestGenerator:
    def parse_cases_file(
        self, filename: str
    ) -> tuple[List[ParsedCase], List[ast.ClassDef]]:
        with open(filename) as f:
            tree = ast.parse(f.read())

        cases_func = next(
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == "cases"
        )

        # Find all custom class definitions
        custom_classes: List[ast.ClassDef] = [
            node
            for node in cases_func.body
            if isinstance(node, ast.ClassDef)
            and any(
                isinstance(base, ast.Name)
                and base.id == "GroupedMetadata"
                or isinstance(base, ast.Attribute)
                and base.attr == "GroupedMetadata"
                for base in node.bases
            )
        ]

        parsed_cases = []
        for node in cases_func.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Yield):
                case = node.value.value
                if (
                    isinstance(case, ast.Call)
                    and isinstance(case.func, ast.Name)
                    and case.func.id == "Case"
                ):
                    parsed_cases.append(
                        ParsedCase(
                            annotation=case.args[0],
                            valid_cases=case.args[1],
                            invalid_cases=case.args[2],
                        )
                    )
        return parsed_cases, custom_classes

    def generate_type_name(self, annotation: ast.AST) -> str:
        if isinstance(annotation, ast.Subscript):
            if isinstance(annotation.slice, ast.Tuple):
                # Handle Annotated[type, constraint]
                constraint = annotation.slice.elts[1]
                if isinstance(constraint, ast.Call):
                    # Handle both Name and Attribute nodes for constraint.func
                    if isinstance(constraint.func, ast.Name):
                        constraint_name = constraint.func.id
                    elif isinstance(constraint.func, ast.Attribute):
                        constraint_name = constraint.func.attr
                    else:
                        return "Unknown"

                    # Handle BaseMetadata (positional args)
                    if constraint.args:
                        return f"{constraint_name}{astor.to_source(constraint.args[0]).strip()}"

                    # Handle GroupedMetadata (keyword args)
                    if constraint.keywords:
                        parts = []
                        for kw in constraint.keywords:
                            parts.append(f"{kw.arg}{astor.to_source(kw.value).strip()}")
                        return f"{constraint_name}_{'_'.join(parts)}"

                    return constraint_name

            else:
                # Handle both Name and Attribute nodes
                if isinstance(annotation.value, ast.Name):
                    return annotation.value.id
                elif isinstance(annotation.value, ast.Attribute):
                    return annotation.value.attr
        return "Unknown"

    def generate_test_code(self, case: ParsedCase) -> str:
        type_name = (
            self.generate_type_name(case.annotation)
            .replace(".", "_")
            .replace(",", "_")
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "")
            .replace('"', "")
            .replace("'", "")
            .replace("/", "")
            .replace("%", "")
            .replace(":", "")
            .replace("=", "")
        )
        type_name_for_func = type_name.lower()

        code = [
            f"{type_name} = {astor.to_source(case.annotation).strip()}",
            "",
            "@typechecked",
            f"def expects_{type_name_for_func}(value: {type_name}) -> None:",
            "    pass",
            "",
            "@pytest.mark.parametrize(",
            '    "valid_case",',
            f"    {astor.to_source(case.valid_cases).strip()},",
            ")",
            f"def test_{type_name}_accepts_valid_value(valid_case):",
            f"    expects_{type_name_for_func}(valid_case)",
            "",
            "@pytest.mark.parametrize(",
            '    "invalid_case",',
            "    [",
            "        dict(",
            "            value=invalid_value,",
            '            match="with value={value!r} failed {annotated_type}",',
            "        )",
            f"        for invalid_value in {astor.to_source(case.invalid_cases).strip()}",
            "    ]",
            '    + [dict(value="hi", match="(str) is not an instance of int")]',
            ")",
            f"def test_{type_name}_raises_TypeCheckError(invalid_case):",
            "    value = invalid_case['value']",
            "    match = invalid_case['match']",
            f"    annotated_type = typing.get_args({type_name})[1]",
            "    with pytest.raises(",
            "        typeguard.TypeCheckError,",
            "        match=re.compile(",
            "            re.escape(match.format(value=value, annotated_type=annotated_type))",
            "        ),",
            "    ):",
            f"        expects_{type_name_for_func}(value)",
            "",
        ]
        return "\n".join(code)

    def generate_all_tests(self, filename: str) -> str:
        imports = [
            "import re",
            "import typing",
            "import pytest",
            "import typeguard",
            "import math",
            "from datetime import date, datetime, timedelta, timezone",
            "from decimal import Decimal",
            "from typeguard import typechecked",
            "import annotated_types as at",
            "from typing import Iterator, Annotated, List, Dict, Set, Tuple",
            "import typeguard_annotatedtypes_plugin  # type: ignore # noqa: F401",
            "",
            "",
        ]

        cases, custom_classes = self.parse_cases_file(filename)

        # Generate class definitions
        class_definitions = []
        for class_def in custom_classes:
            class_code = astor.to_source(class_def)
            class_definitions.append(class_code)
        test_code = [self.generate_test_code(case) for case in cases]

        return "\n".join(imports + class_definitions + test_code)


test_generator = TestGenerator()
try:
    test_code = test_generator.generate_all_tests("tests/cases.py")
    with open("tests/test_all.py", "w") as f:
        f.write(test_code)
except Exception:
    import pdbr

    pdbr.post_mortem()
