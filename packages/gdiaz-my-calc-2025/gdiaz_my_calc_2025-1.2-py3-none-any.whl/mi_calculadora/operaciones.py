# src/mi_calculadora/operaciones.py
"""Módulo con operaciones matemáticas básicas."""

def sumar(a, b):
  """Retorna la suma de dos números."""
  return a + b

def restar(a, b):
  """Retorna la resta de dos números (a - b)."""
  return a - b

def multiplicar(a, b):
  """Retorna la multiplicación de dos números."""
  return a * b

def dividir(a, b):
  """
  Retorna la división de dos números (a / b).
  Lanza un ValueError si se intenta dividir por cero.
  """
  if b == 0:
      raise ValueError("No se puede dividir por cero.")
  return a / b

def potenciacion(a, b):
  """
  Retorna la potencia de dos números (a / b).
  """
  return a ** b

