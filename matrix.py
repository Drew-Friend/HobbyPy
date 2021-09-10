const = [
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
]
b = [-1, -1, -1, -1, -1]


def add(eqBase, eqChange):
    coef = -1 * const[eqBase][0] / const[eqChange][0]
    for i in const[eqChange]:
        i = i * coef
    b[eqChange] = b[eqChange] * coef
