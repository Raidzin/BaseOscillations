from sympy import solve, symbols, sympify, Eq, solveset, re, im


def solve_symbolic(
        first_equation: Eq,
        second_equation: Eq,
):
    x, y = symbols('x, y')
    sol = solve([first_equation, second_equation], [x, y])
    return sol


def determinate_state(
        first_equation,
        second_equation,
        point
):
    x, y = symbols('x, y')
    a = first_equation.diff(x)
    b = first_equation.diff(y)
    c = second_equation.diff(x)
    d = second_equation.diff(y)
    subs = {symbols(key): item for key, item in point.items()}
    a0 = a.evalf(subs=subs)
    b0 = b.evalf(subs=subs)
    c0 = c.evalf(subs=subs)
    d0 = d.evalf(subs=subs)
    lmbd = symbols('lmbd')
    h_eq = lmbd ** 2 - lmbd * (a0 + d0) + a0 * d0 - b0 * c0
    lmbd1, lmbd2 = solveset(h_eq, lmbd)
    if im(lmbd1) == 0:
        if re(lmbd1) > 0 and re(lmbd2) > 0:
            return 'Неустойчивый узел'
        elif re(lmbd1) < 0 and re(lmbd2) < 0:
            return 'Устойчивый узел'
        else:
            return 'Седло'
    else:
        if re(lmbd1) > 0 and re(lmbd2) > 0:
            return 'Неустойчивый фокус'
        elif re(lmbd1) < 0 and re(lmbd2) < 0:
            return 'Устойчивый фокус'
        elif re(lmbd1) == 0 and re(lmbd2) == 0:
            return 'Седло'
        else:
            return 'Неизвестный'


def resolve_dynamic_system(
        first_equation: str,
        second_equation: str,
):
    f1 = sympify(first_equation)
    f2 = sympify(second_equation)
    eq1 = Eq(f1, rhs=0)
    eq2 = Eq(f2, rhs=0)
    points = solve_symbolic(eq1, eq2)
    res = [determinate_state(f1, f2, {'x': x, 'y': y}) for x, y in points]
    return points, res


if __name__ == '__main__':
    f1 = 'x ** 3 + x * (y ** 2) - 10 * y'
    f2 = 'x + (x ** 2) * y + (y ** 3) - 7 * y'
    points, states = resolve_dynamic_system(f1, f2)
    print(points)
    print(states)
