# unify.py
"""
Módulo: Algoritmo de unificación
"""

def unify(x, y, substitutions=None):
    """Devuelve la sustitución necesaria para unificar x e y"""
    if substitutions is None:
        substitutions = {}

    if x == y:
        return substitutions

    if isinstance(x, str) and x.islower():
        return unify_var(x, y, substitutions)

    if isinstance(y, str) and y.islower():
        return unify_var(y, x, substitutions)

    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        for a, b in zip(x, y):
            substitutions = unify(a, b, substitutions)
            if substitutions is None:
                return None
        return substitutions

    return None


def unify_var(var, x, substitutions):
    """Unifica una variable con un valor"""
    if var in substitutions:
        return unify(substitutions[var], x, substitutions)
    elif x in substitutions:
        return unify(var, substitutions[x], substitutions)
    elif occurs_check(var, x, substitutions):
        return None
    else:
        substitutions[var] = x
        return substitutions


def occurs_check(var, x, substitutions):
    """Evita unificación infinita (ocurrencia del mismo var dentro del valor)"""
    if var == x:
        return True
    if isinstance(x, tuple):
        return any(occurs_check(var, xi, substitutions) for xi in x)
    return False
