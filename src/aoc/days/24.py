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
    # Annotate the adders for manual inspection, grouped by bit position
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


def print_bad_outputs(expressions: dict[str, Expression]):
    # Debug code for manual inspection of the adder.
    # Try to add values one bit position at a time.  If the actual
    # result doesn't match the expected result, print the incorrect
    # bit position along with any non-zero gate outputs.
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


def find_bad_outputs(expressions: list[Expression]):
    # Check the half/full adder for each bit and return any outputs
    # that doesn't match the expected structure.
    #
    # Not entirely bullet-proof, but should cover most cases in practice.
    expression_map = {(e.left, e.operator, e.right): e for e in expressions}

    bad_outputs = set[str]()

    def get_fuzzy(left: str, operator: str, right: str):
        left, right = sorted([left, right])
        expr = expression_map.get((left, operator, right))
        if expr:
            return expr

        for e in expressions:
            if e.operator != operator:
                continue
            inputs = (e.left, e.right)
            if left in inputs or right in inputs:
                bad_outputs.update(
                    key for key in (left, right) if key and key not in inputs
                )
                return e

        bad_outputs.update(output for output in (left, right) if output)

    def expr(left: str, operator: str, right: str):
        left, right = sorted([left, right])
        return expression_map[(left, operator, right)]

    carry_in = ""
    first_carry = ""

    for bit_index in range(45):
        x_key = f"x{bit_index:02d}"
        y_key = f"y{bit_index:02d}"
        z_key = f"z{bit_index:02d}"

        carry_expr = expr(x_key, "AND", y_key)
        sum_expr = expr(x_key, "XOR", y_key)

        if bit_index == 0:
            if not sum_expr.output == z_key:
                bad_outputs.update([sum_expr.output, z_key])
            if carry_expr.output.startswith("z"):
                bad_outputs.add(carry_expr.output)
            else:
                first_carry = carry_expr.output

        elif bit_index == 1:
            if carry_expr.output.startswith("z"):
                bad_outputs.add(carry_expr.output)
            if sum_expr.output.startswith("z"):
                bad_outputs.add(sum_expr.output)

            carry_in_expr = get_fuzzy(first_carry, "AND", sum_expr.output)
            if carry_in_expr:
                if carry_in_expr.output.startswith("z"):
                    bad_outputs.add(carry_in_expr.output)
                else:
                    carry_in = carry_in_expr.output

            z_output_expr = get_fuzzy(first_carry, "XOR", sum_expr.output)
            if z_output_expr and z_output_expr.output != z_key:
                bad_outputs.update([z_output_expr.output, z_key])

            out_expr = get_fuzzy(carry_expr.output, "OR", carry_in)
            if out_expr:
                if out_expr.output.startswith("z"):
                    bad_outputs.add(out_expr.output)
                    carry_in = ""
                else:
                    carry_in = out_expr.output

        elif bit_index > 1:
            if carry_expr.output.startswith("z"):
                bad_outputs.add(carry_expr.output)
            if sum_expr.output.startswith("z"):
                bad_outputs.add(sum_expr.output)

            z_output_expr = get_fuzzy(carry_in, "XOR", sum_expr.output)
            if z_output_expr and z_output_expr.output != z_key:
                bad_outputs.update([z_output_expr.output, z_key])

            carry_expr_2 = get_fuzzy(carry_in, "AND", sum_expr.output)
            carry_in = ""
            if carry_expr_2:
                if carry_expr_2.output.startswith("z"):
                    bad_outputs.add(carry_expr_2.output)
                else:
                    out_expr = get_fuzzy(carry_expr.output, "OR", carry_expr_2.output)
                    if out_expr:
                        if out_expr.output.startswith("z"):
                            if bit_index < 44:
                                bad_outputs.add(out_expr.output)
                        else:
                            carry_in = out_expr.output

    return bad_outputs


def part_2(input: str):
    expression_map, _ = parse_expressions(input)
    expressions = sorted(expression_map.values(), key=lambda e: e.operator)
    bad_outputs = find_bad_outputs(expressions)
    return ",".join(sorted(bad_outputs))
