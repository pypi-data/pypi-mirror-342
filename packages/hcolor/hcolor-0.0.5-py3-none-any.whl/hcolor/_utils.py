import hashlib
import pprint
from typing import Any, Tuple, Union

Number = Union[int, float]


def clamp(value: Number, min_val=0.0, max_val=1.0) -> Number:
    return min((max_val, max((min_val, value))))


def to_u4(value: float) -> int:
    return int(round(clamp(value) * 0xF))


def to_u8(value: float) -> int:
    return int(round(clamp(value) * 0xFF))


def float_from_u8_str(string_value: str) -> float:
    return clamp(int(string_value, base=16) / 255)


def hash_as_float(object_: Any) -> float:
    special_method = getattr(object_, "repr_for_hash", None)
    repr_ = str(special_method()) if special_method else pprint.pformat(object_)
    hex_digest = calc_hash_hex(repr_)[:8]
    return int(hex_digest, 16) / 0xFFFFFFFF


def rgb_from_str(rgb_as_hex: str) -> Tuple[float, float, float]:
    """Converts e.g. '#fff' -> (1, 1, 1) and '#ffffff' -> (1, 1, 1)"""
    assert isinstance(rgb_as_hex, str), f"Hex color has to be specified as string, got {type(rgb_as_hex).__name__}."
    s = rgb_as_hex if not rgb_as_hex.startswith("#") else rgb_as_hex[1:]
    assert len(s) in {3, 6}, f"Color should be specified with 3 or 6 hexadecimal chars, got: {s!r}"
    assert all(c in "0123456789abcdef" for c in s), f"Color should be specified with hexadecimal chars, got: {s!r}"

    if len(s) == 3:
        r, g, b = s[0] * 2, s[1] * 2, s[2] * 2
    else:
        r, g, b = s[0:2], s[2:4], s[4:6]

    return float_from_u8_str(r), float_from_u8_str(g), float_from_u8_str(b)


def calc_hash_hex(string_castable: Any) -> str:
    return hashlib.sha1(str(string_castable).encode("utf-8")).hexdigest()
