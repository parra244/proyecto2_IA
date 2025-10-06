import re
import itertools

# -------------------------------
# Utilidades básicas
# -------------------------------

_var_counter = itertools.count()

def nueva_variable(base="x"):
    """Genera un nombre de variable único."""
    return f"{base}{next(_var_counter)}"

def eliminar_implicaciones(expr: str) -> str:
    """Reemplaza A -> B por ¬A ∨ B"""
    return re.sub(r"\((.*?)\s*->\s*(.*?)\)", r"(¬\1 ∨ \2)", expr)

def mover_negaciones(expr: str) -> str:
    """Aplica leyes de De Morgan y mueve negaciones hacia adentro."""
    cambios = True
    while cambios:
        antes = expr
        # Doble negación
        expr = expr.replace("¬¬", "")
        # De Morgan
        expr = expr.replace("¬(A ∧ B)", "(¬A ∨ ¬B)")
        expr = expr.replace("¬(A ∨ B)", "(¬A ∧ ¬B)")
        # Cuantificadores
        expr = expr.replace("¬∀", "∃¬")
        expr = expr.replace("¬∃", "∀¬")
        cambios = expr != antes
    return expr

def estandarizar_variables(expr: str) -> str:
    """Renombra variables para evitar colisiones."""
    variables = re.findall(r"[a-z]\w*", expr)
    mapping = {}
    for v in variables:
        if v not in mapping:
            mapping[v] = nueva_variable("v")
    for old, new in mapping.items():
        expr = re.sub(rf"\b{old}\b", new, expr)
    return expr

def skolemizar(expr: str) -> str:
    """
    Sustituye variables existenciales por constantes o funciones de Skolem.
    Simplificación: si ∃x.P(x) -> P(c), si ∃x depende de variables universales, se convierte en función.
    """
    cambios = True
    while cambios:
        antes = expr
        # Caso simple: ∃x P(x)
        match = re.search(r"∃([a-z]\w*)\.(.*)", expr)
        if match:
            var, subexpr = match.groups()
            # Constante de Skolem
            skolem_const = f"c_{var}"
            expr = re.sub(rf"\b{var}\b", skolem_const, subexpr)
        cambios = expr != antes
    return expr

def eliminar_cuantificadores(expr: str) -> str:
    """Elimina cuantificadores ∀ y ∃ una vez procesados."""
    expr = re.sub(r"[∀∃][a-z]\w*\.", "", expr)
    return expr

def distribuir_or_sobre_and(expr: str) -> str:
    """Distribuye ∨ sobre ∧ para obtener FNC."""
    cambios = True
    while cambios:
        antes = expr
        expr = re.sub(r"\((.*?) ∨ \((.*?) ∧ (.*?)\)\)", r"((\1 ∨ \2) ∧ (\1 ∨ \3))", expr)
        expr = re.sub(r"\(\((.*?) ∧ (.*?)\) ∨ (.*?)\)", r"((\1 ∨ \3) ∧ (\2 ∨ \3))", expr)
        cambios = expr != antes
    return expr

def extraer_clausulas(expr: str):
    """Convierte la expresión final en lista de cláusulas (sets de literales)."""
    # Quitar paréntesis exteriores
    expr = expr.strip()
    if expr.startswith("(") and expr.endswith(")"):
        expr = expr[1:-1]

    clausulas = []
    for conj in expr.split("∧"):
        disy = conj.replace("(", "").replace(")", "").strip()
        literales = [lit.strip() for lit in disy.split("∨")]
        clausulas.append(set(literales))
    return clausulas

# -------------------------------
# Función principal
# -------------------------------

def convertir_a_fnc(expr: str):
    """Pipeline completo de conversión a FNC con trazas paso a paso."""
    pasos = []

    pasos.append(f"Entrada: {expr}")
    expr = eliminar_implicaciones(expr)
    pasos.append(f"Sin implicaciones: {expr}")

    expr = mover_negaciones(expr)
    pasos.append(f"Negaciones movidas: {expr}")

    expr = estandarizar_variables(expr)
    pasos.append(f"Estandarización: {expr}")

    expr = skolemizar(expr)
    pasos.append(f"Skolemización: {expr}")

    expr = eliminar_cuantificadores(expr)
    pasos.append(f"Sin cuantificadores: {expr}")

    expr = distribuir_or_sobre_and(expr)
    pasos.append(f"Distribución: {expr}")

    clausulas = extraer_clausulas(expr)
    pasos.append(f"Cláusulas: {clausulas}")

    return clausulas, pasos

# -------------------------------
# Prueba rápida
# -------------------------------
if __name__ == "__main__":
    formula = "∀x (P(x) -> ∃y Q(x,y))"
    clausulas, pasos = convertir_a_fnc(formula)
    for p in pasos:
        print(p)
    print("Resultado en FNC:", clausulas)

