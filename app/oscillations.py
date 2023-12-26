from enum import StrEnum

from sympy import Eq, symbols, sympify, solve, solveset, im, re


class EquilibriumState(StrEnum):
    unstable_knot = 'Неустойчивый узел'
    stable_knot = 'Устойчивый узел'
    saddle = 'Седло'
    unstable_focus = 'Неустойчивый фокус'
    stable_focus = 'Устойчивый фокус'
    center = 'Центр'
    unknown = 'Неизвестный'


def resolve_dynamic_system(
        first_function_text: str,
        second_function_text: str,
):
    first_function = sympify(first_function_text)
    second_function = sympify(second_function_text)
    equilibrium_points = find_equilibrium_points(
        first_function=first_function,
        second_function=second_function,
    )
    derived_functions = find_derived_functions(
        first_function=first_function,
        second_function=second_function,
    )
    all_characteristic_roots = [
        find_characteristic_equation_roots(derived_functions, {'x': x, 'y': y})
        for x, y in equilibrium_points
    ]
    equilibrium_states = [
        determinate_equilibrium_state(characteristic_root)
        for characteristic_root in all_characteristic_roots
    ]
    return [
        (point, state)
        for point, state in zip(equilibrium_points, equilibrium_states)
    ]


def find_equilibrium_points(first_function, second_function):
    x, y = symbols('x, y')
    points = solve(
        [Eq(first_function, rhs=0), Eq(second_function, rhs=0)],
        [x, y]
    )
    return [(x, y) for x, y in points if im(x) == 0 and im(y) == 0]


def find_derived_functions(
        first_function,
        second_function,
):
    x, y = symbols('x, y')
    a = first_function.diff(x)
    b = first_function.diff(y)
    c = second_function.diff(x)
    d = second_function.diff(y)
    return a, b, c, d


def find_characteristic_equation_roots(derived_functions, point):
    subs = {symbols(key): item for key, item in point.items()}
    a, b, c, d = [diff.evalf(subs=subs) for diff in derived_functions]
    lmbd = symbols('lmbd')
    characteristic_equation = lmbd ** 2 - lmbd * (a + d) + a * d - b * c
    return solveset(characteristic_equation, lmbd)


def determinate_equilibrium_state(characteristic_roots):
    lmbd1, lmbd2 = characteristic_roots
    match (im(lmbd1), im(lmbd2), re(lmbd1), re(lmbd2)):
        case (0, 0, re1, re2) if re1 > 0 and re2 > 0:
            return EquilibriumState.unstable_knot
        case (0, 0, re1, re2) if re1 < 0 and re2 < 0:
            return EquilibriumState.stable_knot
        case (0, 0, _, _):
            return EquilibriumState.saddle
        case (_, _, re1, re2) if re1 > 0 and re2 > 0:
            return EquilibriumState.unstable_focus
        case (_, _, re1, re2) if re1 < 0 and re2 < 0:
            return EquilibriumState.stable_focus
        case (_, _, 0, 0):
            return EquilibriumState.center
        case _:
            return EquilibriumState.unknown



