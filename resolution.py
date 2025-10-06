# resolution.py
"""
Módulo: Resolución por refutación con unificación
"""

from unify import unify

def negar_literal(literal):
    """Devuelve la negación de un literal"""
    if literal.startswith("¬"):
        return literal[1:]
    else:
        return "¬" + literal

def parse_literal(literal):
    """Convierte un literal como 'P(x,y)' en (predicado, [arg1,arg2,...], negado)"""
    negado = literal.startswith("¬")
    if negado:
        literal = literal[1:]
    pred, args = literal.split("(", 1)
    args = args[:-1].split(",")  # quitar paréntesis final
    return pred.strip(), [a.strip() for a in args], negado

def aplicar_sustitucion(literal, sustituciones):
    """Aplica una sustitución a un literal"""
    pred, args, negado = parse_literal(literal)
    nuevos_args = [sustituciones.get(a, a) for a in args]
    lit = f"{pred}({','.join(nuevos_args)})"
    return f"¬{lit}" if negado else lit

def resolve(clause1, clause2):
    """Aplica resolución entre dos cláusulas con unificación"""
    resolvents = []
    for lit1 in clause1:
        pred1, args1, neg1 = parse_literal(lit1)
        for lit2 in clause2:
            pred2, args2, neg2 = parse_literal(lit2)

            # Si son del mismo predicado y uno es negado
            if pred1 == pred2 and neg1 != neg2 and len(args1) == len(args2):
                # Intentar unificar
                subst = unify(tuple(args1), tuple(args2))
                if subst is not None:
                    # Aplicar sustitución al resto de cláusulas
                    nueva = (clause1.union(clause2)) - {lit1, lit2}
                    nueva = {aplicar_sustitucion(l, subst) for l in nueva}
                    resolvents.append(nueva)
    return resolvents

def resolution(kb):
    """Algoritmo principal de resolución por refutación"""
    kb = [set(c) for c in kb]
    pasos = []
    new = set()

    while True:
        pares = [(kb[i], kb[j]) for i in range(len(kb)) for j in range(i + 1, len(kb))]

        for (ci, cj) in pares:
            resolventes = resolve(ci, cj)
            for r in resolventes:
                pasos.append(f"Resolviendo {ci} y {cj} -> {r}")
                if not r:  # cláusula vacía
                    pasos.append(" Se derivó la cláusula vacía. Teorema demostrado.")
                    return True, pasos
            new.update(map(frozenset, resolventes))

        # No se generaron nuevas cláusulas
        if new.issubset(set(map(frozenset, kb))):
            pasos.append(" No se puede derivar la cláusula vacía.")
            return False, pasos

        for c in new:
            if set(c) not in kb:
                kb.append(set(c))
