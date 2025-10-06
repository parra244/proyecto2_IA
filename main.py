import os
from resolution import resolution
from fnc import convertir_a_fnc

def cargar_clausulas(ruta):
    """
    Lee el archivo de entrada y devuelve una lista de cláusulas (sets de literales).
    Si encuentra una fórmula lógica en lugar de cláusulas en FNC, la convierte automáticamente.
    """
    clausulas = []

    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read().strip()

    # Si el archivo tiene varios renglones con "∨" o "∧", lo tratamos como cláusulas directas
    if "∨" in contenido or "v" in contenido or "V" in contenido:
        for linea in contenido.splitlines():
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            # limpiar numeración tipo "1. "
            if linea[0].isdigit() and "." in linea:
                linea = linea.split(".", 1)[1].strip()
            # normalizar disyunciones
            linea = linea.replace(" v ", "∨").replace(" V ", "∨")
            literales = [lit.strip() for lit in linea.split("∨")]
            clausulas.append(set(literales))
    else:
        # Caso: es una fórmula lógica, la convertimos a FNC
        clausulas, pasos = convertir_a_fnc(contenido)
        print("=== Conversión a FNC ===")
        for p in pasos:
            print(p)
        print("========================")

    return clausulas


def ejecutar_caso(nombre, ruta):
    """Ejecuta la resolución para un caso y guarda resultados."""
    clausulas = cargar_clausulas(ruta)
    resultado, pasos = resolution(clausulas)

    # Crear carpeta de resultados si no existe
    os.makedirs("resultados", exist_ok=True)

    ruta_salida = os.path.join("resultados", f"{nombre}_resultado.txt")
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write("Base de conocimiento:\n")
        for c in clausulas:
            f.write(f"{c}\n")
        f.write("\nPasos de resolución:\n")
        for p in pasos:
            f.write(p + "\n")
        f.write("\nResultado final:\n")
        f.write("El teorema fue demostrado \n" if resultado else "El teorema no pudo ser demostrado \n")

    print(f"Resultado guardado en: {ruta_salida}")


if __name__ == "__main__":
    # Ejemplo: caso directo en FNC
    ejecutar_caso("marco_cesar", "casos/marco_cesar.txt")

    # Ejemplo: fórmula lógica a transformar
    ejecutar_caso("teorema_ancestor", "casos/teorema_ancestor.txt")

