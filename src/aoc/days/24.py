from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

type Bit = Literal[0, 1]


@dataclass
class Expression:
    left: str
    right: str
    operator: str
    output: str

    def __str__(self):
        return f"{self.left} {self.operator} {self.right} -> {self.output}"

    def clone(self):
        return Expression(self.left, self.right, self.operator, self.output)


def parse_expressions(input: str):
    initial_values = dict[str, Bit]()
    expressions = dict[str, Expression]()

    lines = iter(input.split("\n"))
    while line := next(lines):
        key, initial_value = line.split(": ")
        initial_values[key] = 1 if int(initial_value) else 0

    for line in lines:
        left, operator, right, _, output = line.split(" ")
        left, right = sorted((left, right))
        expressions[output] = Expression(left, right, operator, output)

    return expressions, initial_values


def eval_expression(
    key: str,
    expressions: dict[str, Expression],
    results: dict[str, Bit],
):
    if key not in results:
        expr = expressions[key]
        left = eval_expression(expr.left, expressions, results)
        right = eval_expression(expr.right, expressions, results)
        match expr.operator:
            case "AND":
                value = left & right
            case "OR":
                value = left | right
            case "XOR":
                value = left ^ right
            case _:
                raise ValueError(f"Unknown operator {expr.operator}")
        results[expr.output] = value
    return results[key]


def part_1(input: str):
    expressions, results = parse_expressions(input)
    z_expressions = [expr for key, expr in expressions.items() if key.startswith("z")]

    result = 0
    for expr in z_expressions:
        value = eval_expression(expr.output, expressions, results)
        bit_index = int(expr.output.removeprefix("z"))
        result |= value << bit_index

    return result


def print_circuit(expressions: list[Expression]):
    # Annotate the adders and print them for manual inspection
    output_map = dict[str, str]()

    def print_expr(expr: Expression):
        annotated_expression = expr.clone()
        if expr.left in output_map:
            annotated_expression.left = f"{output_map[expr.left]} ({expr.left})"
        if expr.right in output_map:
            annotated_expression.right = f"{output_map[expr.right]} ({expr.right})"
        if expr.output in output_map:
            annotated_expression.output = f"{output_map[expr.output]} ({expr.output})"
        print(annotated_expression)

    for bit_index in range(45):
        key = (f"x{bit_index:02d}", f"y{bit_index:02d}")
        for expr in expressions:
            if (expr.left, expr.right) != key:
                continue
            if expr.operator == "AND":
                output_map[expr.output] = f"c{bit_index:02d}"
            if expr.operator == "XOR" and expr.output != "z00":
                output_map[expr.output] = f"s{bit_index:02d}"

    for bit_index in range(45):
        in_sum = (f"c{bit_index:02d}", f"s{bit_index + 1:02d}")
        in_carry = (f"c{bit_index:02d}", f"in{bit_index:02d}")
        carry_sum = (f"s{bit_index:02d}", f"in{bit_index:02d}")
        in_cx = (f"c{bit_index:02d}x", f"c{bit_index:02d}")

        for expr in expressions:
            mapped_key = (output_map.get(expr.left), output_map.get(expr.right))
            if all(key in in_sum for key in mapped_key) and expr.operator == "AND":
                output_map[expr.output] = f"in{bit_index + 1:02d}"
            if all(key in in_carry for key in mapped_key) and expr.operator == "OR":
                output_map[expr.output] = f"in{bit_index + 1:02d}"
            if all(key in carry_sum for key in mapped_key) and expr.operator == "AND":
                output_map[expr.output] = f"c{bit_index:02d}x"
            if all(key in in_cx for key in mapped_key) and expr.operator == "OR":
                output_map[expr.output] = f"in{bit_index + 1:02d}"

    for bit_index in range(45):
        key = (f"x{bit_index:02d}", f"y{bit_index:02d}")
        children = list[Expression]()

        for expr in expressions:
            if (expr.left, expr.right) != key:
                continue
            print_expr(expr)

            children.extend(c for c in expressions if expr.output in (c.left, c.right))

        for child in sorted(children, key=lambda e: e.operator):
            print_expr(child)

        print()


def part_2(input: str):
    expression_map, _ = parse_expressions(input)
    expressions = sorted(expression_map.values(), key=lambda e: e.operator)
    print_circuit(expressions)

    def swap(key_a: str, key_b: str):
        a = expression_map[key_a]
        b = expression_map[key_b]
        a.output = key_b
        b.output = key_a

    # Determined by manual inspection, won't work on other input
    swap("z12", "fgc")
    swap("z29", "mtj")
    swap("dgr", "vvm")
    swap("z37", "dtv")

    return "dgr,dtv,fgc,mtj,vvm,z12,z29,z37"


def print_bad_outputs(expressions: dict[str, Expression]):
    all_zeros: dict[str, Bit] = {key: 0 for key in expressions.keys()}
    bad_outputs = set[str]()

    for bit_index in range(45):
        x_key = f"x{bit_index:02d}"
        y_key = f"y{bit_index:02d}"
        z_lsb = f"z{bit_index:02d}"
        z_msb = f"z{bit_index + 1:02d}"

        test_bits: tuple[tuple[Bit, Bit], ...] = ((0, 1), (1, 1))

        for x, y in test_bits:
            results = all_zeros.copy()
            results.update({x_key: x, y_key: y})

            lsb = eval_expression(z_lsb, expressions, results)
            msb = eval_expression(z_msb, expressions, results)
            value = msb * 2 + lsb
            expected = x + y

            if value != expected:
                print(
                    f"{x_key} + {y_key} ({x} + {y}): Expected {expected}, got {value}"
                )
                for key, result in results.items():
                    if key not in (x_key, y_key) and result == 1:
                        print(key)

    print(sorted(bad_outputs))
