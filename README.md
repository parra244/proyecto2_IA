# Proyecto G7 - Sistema de Resolución por Refutación

Este proyecto implementa un sistema de resolución por refutación para lógica de primer orden, incluyendo conversión a Forma Normal Conjuntiva (FNC) y unificación de términos.

## Características

- **Conversión a FNC**: Convierte fórmulas lógicas complejas a Forma Normal Conjuntiva
- **Unificación**: Implementa el algoritmo de unificación para términos lógicos
- **Resolución por Refutación**: Demuestra teoremas usando el método de resolución
- **Casos de Prueba**: Incluye ejemplos del "Teorema de Marco y César" y el "Teorema de Ancestros"

## Estructura del Proyecto

```
├── main.py              # Archivo principal que ejecuta los casos de prueba
├── fnc.py              # Conversión a Forma Normal Conjuntiva
├── resolution.py       # Algoritmo de resolución por refutación
├── unify.py           # Algoritmo de unificación
├── casos/             # Archivos de entrada con casos de prueba
│   ├── marco_cesar.txt
│   └── teorema_ancestor.txt
└── resultados/        # Archivos de salida con los resultados
    ├── marco_cesar_resultado.txt
    └── teorema_ancestor_resultado.txt
```

## Casos de Prueba

### 1. Marco y César
Demuestra que Marco odia a César basándose en:
- Marco es hombre y pompeyano
- Los pompeyanos son romanos
- Los romanos son leales a César o lo odian
- Marco intenta asesinar a César
- Si alguien intenta asesinar a su gobernante, no es leal a él

### 2. Teorema de Ancestros
Demuestra que Anna es ancestro de John basándose en:
- Anna es padre de Bob
- Bob es padre de Carol
- Carol es padre de John
- Definición recursiva de ancestro

## Uso

```bash
python main.py
```

El programa ejecutará ambos casos de prueba y generará los archivos de resultado en la carpeta `resultados/`.

## Requisitos

- Python 3.6+

## Autor

Parra - Proyecto G7
