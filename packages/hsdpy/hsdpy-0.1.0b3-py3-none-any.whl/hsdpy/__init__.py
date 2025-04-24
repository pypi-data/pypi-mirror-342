import ctypes
import importlib.metadata
import logging
import numpy as np
import numpy.typing as npt
from typing import Dict, Tuple, Union, Optional, Type, Any, cast

_logger = logging.getLogger(__name__)
try:
    __version__ = importlib.metadata.version("hsdpy")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0-unknown"
    _logger.warning(
        "Could not determine package version using importlib.metadata. "
        "Is the package installed correctly?"
    )

from . import _ctypes_bindings as ct
from ._ctypes_bindings import get_library_info


class HsdError(Exception):
    def __init__(self, status_code: int, message: str = "") -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"HSD Error [{status_code}]: {message}")


_ERROR_MAP: Dict[int, str] = {
    ct.HSD_ERR_NULL_PTR: "Null pointer error encountered in C library",
    ct.HSD_ERR_UNSUPPORTED: "Unsupported operation/feature requested from C library",
    ct.HSD_ERR_INVALID_INPUT: "Invalid input data provided to C library (e.g., NaN, Inf, incompatible size)",
    ct.HSD_FAILURE: "General failure reported by C library",
}


def _check_status(status: int) -> None:
    if status != ct.HSD_SUCCESS:
        message = _ERROR_MAP.get(status, f"Unknown error code {status} from C library")
        raise HsdError(status, message)


CtypesPtr = Type[ctypes._Pointer]


def _validate_and_prepare_numpy_pair(
    a: np.ndarray,
    b: np.ndarray,
    expected_dtype: npt.DTypeLike,
    ctypes_ptr_type: CtypesPtr,
    casting: str = 'safe'
) -> Tuple[CtypesPtr, CtypesPtr, int]:
    if not isinstance(a, np.ndarray) or not isinstance(b, np.ndarray):
        raise TypeError("Inputs must be NumPy arrays.")
    if a.shape != b.shape:
        raise ValueError(f"Input arrays must have the same shape ({a.shape} != {b.shape}).")
    if a.ndim != 1:
        raise ValueError("Input arrays must be 1-dimensional.")

    if a.dtype != expected_dtype:
        try:
            a = a.astype(expected_dtype, casting=casting, copy=False)
        except TypeError:
            raise TypeError(
                f"Input array 'a' cannot be safely cast to {expected_dtype} from {a.dtype} with casting='{casting}'")
    if not a.flags['C_CONTIGUOUS']:
        a = np.ascontiguousarray(a, dtype=expected_dtype)

    if b.dtype != expected_dtype:
        try:
            b = b.astype(expected_dtype, casting=casting, copy=False)
        except TypeError:
            raise TypeError(
                f"Input array 'b' cannot be safely cast to {expected_dtype} from {b.dtype} with casting='{casting}'")
    if not b.flags['C_CONTIGUOUS']:
        b = np.ascontiguousarray(b, dtype=expected_dtype)

    n = a.size

    if n > 0:
        a_ptr = a.ctypes.data_as(ctypes_ptr_type)
        b_ptr = b.ctypes.data_as(ctypes_ptr_type)
    else:
        a_ptr = ctypes.cast(None, ctypes_ptr_type)
        b_ptr = ctypes.cast(None, ctypes_ptr_type)

    return cast(CtypesPtr, a_ptr), cast(CtypesPtr, b_ptr), n


def dist_sqeuclidean_f32(a: np.ndarray, b: np.ndarray) -> float:
    c_func = ct.hsd_dist_sqeuclidean_f32
    if c_func is None:
        raise NotImplementedError("hsd_dist_sqeuclidean_f32 not available in C library")

    a_ptr, b_ptr, n = _validate_and_prepare_numpy_pair(
        a, b, np.float32, ct.c_float_p, casting='same_kind'
    )
    result = ctypes.c_float()
    status = c_func(a_ptr, b_ptr, n, ctypes.byref(result))
    _check_status(status)
    return result.value


def dist_manhattan_f32(a: np.ndarray, b: np.ndarray) -> float:
    c_func = ct.hsd_dist_manhattan_f32
    if c_func is None:
        raise NotImplementedError("hsd_dist_manhattan_f32 not available in C library")

    a_ptr, b_ptr, n = _validate_and_prepare_numpy_pair(
        a, b, np.float32, ct.c_float_p, casting='same_kind'
    )
    result = ctypes.c_float()
    status = c_func(a_ptr, b_ptr, n, ctypes.byref(result))
    _check_status(status)
    return result.value


def dist_hamming_u8(a: np.ndarray, b: np.ndarray) -> int:
    c_func = ct.hsd_dist_hamming_u8
    if c_func is None:
        raise NotImplementedError("hsd_dist_hamming_u8 not available in C library")

    a_ptr, b_ptr, n = _validate_and_prepare_numpy_pair(
        a, b, np.uint8, ct.c_uint8_p, casting='safe'
    )
    result = ctypes.c_uint64()
    status = c_func(a_ptr, b_ptr, n, ctypes.byref(result))
    _check_status(status)
    return result.value


def sim_dot_f32(a: np.ndarray, b: np.ndarray) -> float:
    c_func = ct.hsd_sim_dot_f32
    if c_func is None:
        raise NotImplementedError("hsd_sim_dot_f32 not available in C library")

    a_ptr, b_ptr, n = _validate_and_prepare_numpy_pair(
        a, b, np.float32, ct.c_float_p, casting='same_kind'
    )
    result = ctypes.c_float()
    status = c_func(a_ptr, b_ptr, n, ctypes.byref(result))
    _check_status(status)
    return result.value


def sim_cosine_f32(a: np.ndarray, b: np.ndarray) -> float:
    c_func = ct.hsd_sim_cosine_f32
    if c_func is None:
        raise NotImplementedError("hsd_sim_cosine_f32 not available in C library")

    a_ptr, b_ptr, n = _validate_and_prepare_numpy_pair(
        a, b, np.float32, ct.c_float_p, casting='same_kind'
    )
    result = ctypes.c_float()
    status = c_func(a_ptr, b_ptr, n, ctypes.byref(result))
    _check_status(status)
    return result.value


def sim_jaccard_u16(a: np.ndarray, b: np.ndarray) -> float:
    c_func = ct.hsd_sim_jaccard_u16
    if c_func is None:
        raise NotImplementedError("hsd_sim_jaccard_u16 not available in C library")

    a_ptr, b_ptr, n = _validate_and_prepare_numpy_pair(
        a, b, np.uint16, ct.c_uint16_p, casting='safe'
    )
    result = ctypes.c_float()
    status = c_func(a_ptr, b_ptr, n, ctypes.byref(result))
    _check_status(status)
    return result.value


def get_backend() -> str:
    c_func = ct.hsd_get_backend
    if c_func is None:
        return "unknown (hsd_get_backend function not found in C library)"
    try:
        backend_bytes = c_func()
        return backend_bytes.decode('utf-8') if backend_bytes else "unknown"
    except Exception as e:
        return f"error retrieving backend info: {e}"


__all__ = [
    "dist_sqeuclidean_f32",
    "dist_manhattan_f32",
    "dist_hamming_u8",
    "sim_dot_f32",
    "sim_cosine_f32",
    "sim_jaccard_u16",
    "get_backend",
    "HsdError",
    "get_library_info"
]
