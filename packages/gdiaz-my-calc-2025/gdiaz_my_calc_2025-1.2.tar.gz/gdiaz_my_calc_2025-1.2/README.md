# Mi-Calculadora

[![PyPI version](https://badge.fury.io/py/mi-calculadora.svg)](https://badge.fury.io/py/mi-calculadora)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Librería Python simple con operaciones matemáticas básicas (suma, resta, multiplicación, división, potenciacion).

## Instalación

Instala desde PyPI usando pip (asegúrate de usar el pip asociado a Python 3):

```bash
python3 -m pip install mi-calculadora


```bash


import mi_calculadora

# Operaciones
suma = mi_calculadora.sumar(10, 5)       # 15
resta = mi_calculadora.restar(10, 5)      # 5
multi = mi_calculadora.multiplicar(10, 5) # 50
div = mi_calculadora.dividir(10, 5)       # 2.0
pot = mi_calculadora.potenciacion(100, 2)       # 10000

print(f"Suma: {suma}, Resta: {resta}, Multi: {multi}, Div: {div}, Pot: {pot}")

# Manejo de errores
try:
    mi_calculadora.dividir(10, 0)
except ValueError as e:
    print(f"Error: {e}") # Error: No se puede dividir por cero.

# Versión
print(f"Versión: {mi_calculadora.__version__}") # 0.1.0 (o la versión actual)
