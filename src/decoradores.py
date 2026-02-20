from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Generic, ParamSpec, TypeVar, cast

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class ResultadoTiempo(Generic[R]):
    resultado: R
    segundos: float

def medir_tiempo(funcion: Callable[P, R]) -> Callable[P, ResultadoTiempo[R]]:
    """
    Decorador: mide tiempo de ejecución y devuelve ResultadoTiempo.
    """

    @wraps(funcion)
    def envoltura(*args: P.args, **kwargs: P.kwargs) -> ResultadoTiempo[R]:
        inicio = time.perf_counter()
        salida = funcion(*args, **kwargs)
        fin = time.perf_counter()
        return ResultadoTiempo(resultado=salida, segundos=fin - inicio)

    return envoltura


def requerir_columnas(*columnas: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorador (factory): valida en tiempo de ejecución que el primer argumento
    tenga atributo .columns y contenga las columnas requeridas.
    Ideal para funciones tipo: f(df: DataFrame, ...)
    """

    def decorador(funcion: Callable[P, R]) -> Callable[P, R]:
        @wraps(funcion)
        def envoltura(*args: P.args, **kwargs: P.kwargs) -> R:
            if len(args) == 0:
                raise TypeError("Se esperaba un DataFrame como primer argumento posicional.")

            obj = args[0]
            cols = getattr(obj, "columns", None)
            if cols is None:
                raise TypeError("El primer argumento no parece ser un DataFrame (no tiene .columns).")

            faltantes = [c for c in columnas if c not in cols]
            if faltantes:
                raise ValueError(f"Faltan columnas requeridas: {faltantes}")

            return funcion(*args, **kwargs)

        return cast(Callable[P, R], envoltura)

    return decorador