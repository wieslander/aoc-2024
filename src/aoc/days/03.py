import re


def part_1(input: str):
    matches = re.findall(r"mul\((\d+),(\d+)\)", input)
    return sum(int(m[0]) * int(m[1]) for m in matches)


def part_2(input: str):
    pattern = r"(?P<op>mul|do|don't)\((?:(?P<a>\d+),(?P<b>\d+))?\)"
    is_enabled = True
    result = 0

    for m in re.finditer(pattern, input):
        match m["op"], m["a"], m["b"]:
            case "do", _, _:
                is_enabled = True
            case "don't", _, _:
                is_enabled = False
            case "mul", a, b if is_enabled:
                result += int(a) * int(b)
            case _:
                pass

    return result
