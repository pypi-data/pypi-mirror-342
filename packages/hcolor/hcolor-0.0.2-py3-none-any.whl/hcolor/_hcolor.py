import colorsys
import dataclasses
from typing import Tuple, Union

from hcolor._utils import Number, clamp, hash_as_float, rgb_from_str, to_u4, to_u8


@dataclasses.dataclass(init=False, repr=False)
class HColor:
    red: float
    green: float
    blue: float
    alpha: float = 1.0

    def __init__(self, *rgb_args: Union[Number, str], alpha: float = None):
        """
        Overloaded constructor:
            - HColor(rgb_hex:str, alpha:float=1.0)
            - HColor(short_rgb_hex:str, alpha:float=1.0)
            - HColor(r:float, g:float, b:float, alpha:float=1.0)

        Valid calls are:
        # full hex
        HColor('#daba31')
        HColor('#daba31', 0.4)
        HColor('#daba31', alpha=0.4)
        # short hex
        HColor('#db3')
        HColor('#db3', 0.4)
        HColor('#db3', alpha=0.4)
        # rgb given as floats in range of [0:1]
        HColor(0.23, 0.12, 0.51)
        HColor(0.23, 0.12, 0.51, 0.4)
        HColor(0.23, 0.12, 0.51, alpha=0.4)
        """

        if 1 <= len(rgb_args) <= 2:
            assert isinstance(rgb_args[0], str), "First arg has to be hexadecimal color given as string."
            self.red, self.green, self.blue = rgb_from_str(rgb_args[0])

        elif 3 <= len(rgb_args) <= 4:
            assert all(isinstance(a, (int, float)) for a in rgb_args[:3]), "All args have to be numbers."
            self.red, self.green, self.blue = (clamp(a) for a in rgb_args[:3])

        else:
            raise ValueError(f"Bad number of constructor arguments: {len(rgb_args)}.")

        if len(rgb_args) in {2, 4}:
            assert alpha is None, "Duplicated alpha value in HColor constructor call."
            self.alpha = clamp(rgb_args[len(rgb_args) - 1])

        elif alpha is not None:
            assert isinstance(alpha, float), "Alpha has to be given as float."
            self.alpha = clamp(alpha)

        else:
            self.alpha = 1.0

    def __iter__(self):
        # this operator, together with __len__ covers all needs of also "unpack" like this:
        # r, g, b = hcolor_object
        yield self.red
        yield self.green
        yield self.blue
        # self.alpha not included
        # get alpha by calling:
        # alpha = hcolor_object.alpha

    def __len__(self) -> int:
        return 3

    def __str__(self):
        """Gives html compatible format, like:
        #AABBCC
        or if there is a transparency:
        rgba(170, 184, 204, 0.5)
        """
        if self.alpha != 1.0:
            return self.as_rgba()
        return self.as_hex()

    def __repr__(self):
        args = list(self)
        if self.alpha != 1.0:
            args.append(self.alpha)
        return f"{self.__class__.__name__}({', '.join(f'{a!r}' for a in args)})"

    def copy(self, red=None, green=None, blue=None, alpha=None) -> "HColor":
        return type(self)(
            red if red is not None else self.red,
            green if green is not None else self.green,
            blue if blue is not None else self.blue,
            alpha if alpha is not None else self.alpha,
        )

    def as_hex(self) -> str:
        return f"#{to_u8(self.red):02x}{to_u8(self.green):02x}{to_u8(self.blue):02x}"

    def as_shex(self) -> str:
        return f"#{to_u4(self.red):1x}{to_u4(self.green):1x}{to_u4(self.blue):1x}"

    def as_rgb(self) -> str:
        return f"rgb({to_u8(self.red)}, {to_u8(self.green)}, {to_u8(self.blue)})"

    def as_rgba(self, alpha=None) -> str:
        return f"rgba({to_u8(self.red)}, {to_u8(self.green)}, {to_u8(self.blue)}, {alpha or self.alpha:.2f})"

    @classmethod
    def from_hash(cls, object_, light=0.5, sat=0.5):
        hue = hash_as_float(object_)
        return cls(*colorsys.hls_to_rgb(hue, light, sat))

    @classmethod
    def from_hls(cls, hue, light=0.5, sat=0.5, alpha=1.0):
        new_color = cls(*colorsys.hls_to_rgb(hue, light, sat))
        new_color.alpha = alpha
        return new_color

    @property
    def to_hls(self) -> Tuple[float, float, float]:
        return colorsys.rgb_to_hls(*self)

    @property
    def hue(self) -> float:
        return self.to_hls[0]

    @property
    def lightness(self) -> float:
        return self.to_hls[1]

    @property
    def saturation(self) -> float:
        return self.to_hls[2]

    @hue.setter
    def hue(self, new_value):
        _, light, sat = self.to_hls
        self.red, self.green, self.blue = colorsys.hls_to_rgb(clamp(new_value), light, sat)

    @lightness.setter
    def lightness(self, new_value):
        h, _, sat = self.to_hls
        self.red, self.green, self.blue = colorsys.hls_to_rgb(h, clamp(new_value), sat)

    @saturation.setter
    def saturation(self, new_value):
        h, light, _ = self.to_hls
        self.red, self.green, self.blue = colorsys.hls_to_rgb(h, light, clamp(new_value))

    def ch_hue(self, new_value: float) -> "HColor":
        new_color = self.copy()
        new_color.hue = new_value
        return new_color

    def ch_light(self, new_value: float) -> "HColor":
        new_color = self.copy()
        new_color.lightness = new_value
        return new_color

    def ch_sat(self, new_value: float) -> "HColor":
        new_color = self.copy()
        new_color.saturation = new_value
        return new_color

    def ch_alpha(self, new_value: float) -> "HColor":
        return self.copy(alpha=new_value)
