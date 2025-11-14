import os
from ctypes import CDLL, Structure, c_double, c_int, c_int64, POINTER

class ResultadoNota(Structure):
    _fields_ = [
        ("media", c_double),
        ("status_code", c_int),
    ]

_DLL_PATH = os.path.join(os.path.dirname(__file__), "notas_avaliacao.dll")

_lib = None

def _load():
    global _lib
    if _lib is None:
        if not os.path.exists(_DLL_PATH):
            raise FileNotFoundError(f"DLL não encontrada: {_DLL_PATH}. Compile com build_msvc_avaliacao.bat.")
        lib = CDLL(_DLL_PATH)
        lib.compute_final_grade.argtypes = [c_double, c_double, c_double, POINTER(ResultadoNota)]
        lib.compute_final_grade.restype = c_int
        _lib = lib
    return _lib


def calcular_media_status(p1: float, p2: float, threshold: float = 7.0) -> dict:
    """
    Calcula média e status (aprovado/reprovado) via DLL C.
    Retorna dict: {"media": float, "status": "aprovado"|"reprovado"}
    """
    lib = _load()
    out = ResultadoNota()
    ok = lib.compute_final_grade(float(p1), float(p2), float(threshold), out)
    if not ok:
        raise ValueError("Falha no compute_final_grade")
    return {
        "media": out.media,
        "status": "aprovado" if out.status_code == 1 else "reprovado"
    }
