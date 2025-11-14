import os
from ctypes import CDLL, Structure, c_double, c_size_t, c_int, POINTER

class StatsBasico(Structure):
    _fields_ = [
        ("media", c_double),
        ("minimo", c_double),
        ("maximo", c_double),
    ]

# Caminho absoluto para a DLL ao lado deste arquivo (../c/notas_basico.dll)
_DLL_PATH = os.path.join(os.path.dirname(__file__), "notas_basico.dll")

def _load_lib():
    if not os.path.exists(_DLL_PATH):
        raise FileNotFoundError(f"DLL não encontrada: {_DLL_PATH}. Compile primeiro (build_msvc.bat).")
    lib = CDLL(_DLL_PATH)
    lib.compute_basic_stats.argtypes = [POINTER(c_double), c_size_t, POINTER(StatsBasico)]
    lib.compute_basic_stats.restype = c_int
    return lib

_LIB = None

def calcular_stats(notas):
    """
    Calcula média, mínimo e máximo usando a DLL C.
    notas: lista de floats.
    Retorna dict {media, minimo, maximo} ou lança ValueError.
    """
    global _LIB
    if _LIB is None:
        _LIB = _load_lib()
    if not notas:
        return {"media": None, "minimo": None, "maximo": None}

    # Converte para array C
    arr = (c_double * len(notas))(*[float(x) for x in notas])
    out = StatsBasico()
    ok = _LIB.compute_basic_stats(arr, len(notas), out)
    if not ok:
        raise ValueError("Falha no cálculo (lista vazia ou dados inválidos)")
    return {"media": out.media, "minimo": out.minimo, "maximo": out.maximo}
