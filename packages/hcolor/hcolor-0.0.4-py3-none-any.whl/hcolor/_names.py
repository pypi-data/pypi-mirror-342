from hcolor._hcolor import HColor
from hcolor._utils import calc_hash_hex


class Colors:
    """A handy namespace that creates HColor instances with certain named hue.
    Usage:

    red = Colors.red()
    pale_red = Colors.red(sat=0.25, light = 0.7)
    """

    def __init__(self):
        raise TypeError("Colors cannot be instantiated directly. Use one of the color creation methods instead.")

    @classmethod
    def from_hash(cls, bytes_blob: bytes, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """Reproducible method to get a color with pseudo-random hue.
        Pretty useful when you don't actually care what's the actual color, but you would like
        to get always the same pseudo-random color of given lightness and saturation.
        Usage:

        my_color_1 = Colors.from_hash(b"any bytes here")
        my_color_2 = Colors.from_hash(my_object.name.encode(), light=0.76, sat=1)
        """

        if not isinstance(bytes_blob, bytes):
            raise TypeError("bytes_blob must be of type bytes")
        hue = int(calc_hash_hex(bytes_blob)[:8], 16) / 0xFFFFFFFF
        return HColor.from_hls(hue=hue, light=light, sat=sat, alpha=alpha)

    @classmethod
    def red(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with red hue."""
        return HColor.from_hls(hue=0.0, light=light, sat=sat, alpha=alpha)

    @classmethod
    def orange_red(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with orange_red hue."""
        return HColor.from_hls(hue=0.05, light=light, sat=sat, alpha=alpha)

    @classmethod
    def orange(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with orange hue."""
        return HColor.from_hls(hue=0.083, light=light, sat=sat, alpha=alpha)

    @classmethod
    def yellow_orange(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with yellow_orange hue."""
        return HColor.from_hls(hue=0.125, light=light, sat=sat, alpha=alpha)

    @classmethod
    def yellow(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with yellow hue."""
        return HColor.from_hls(hue=0.167, light=light, sat=sat, alpha=alpha)

    @classmethod
    def yellow_green(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with yellow_green hue."""
        return HColor.from_hls(hue=0.25, light=light, sat=sat, alpha=alpha)

    @classmethod
    def green(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with green hue."""
        return HColor.from_hls(hue=0.333, light=light, sat=sat, alpha=alpha)

    @classmethod
    def green_cyan(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with green_cyan hue."""
        return HColor.from_hls(hue=0.417, light=light, sat=sat, alpha=alpha)

    @classmethod
    def cyan(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with cyan hue."""
        return HColor.from_hls(hue=0.5, light=light, sat=sat, alpha=alpha)

    @classmethod
    def sky_blue(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with sky_blue hue."""
        return HColor.from_hls(hue=0.583, light=light, sat=sat, alpha=alpha)

    @classmethod
    def blue(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with blue hue."""
        return HColor.from_hls(hue=0.667, light=light, sat=sat, alpha=alpha)

    @classmethod
    def indigo(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with indigo hue."""
        return HColor.from_hls(hue=0.708, light=light, sat=sat, alpha=alpha)

    @classmethod
    def violet(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with violet hue."""
        return HColor.from_hls(hue=0.75, light=light, sat=sat, alpha=alpha)

    @classmethod
    def purple(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with purple hue."""
        return HColor.from_hls(hue=0.792, light=light, sat=sat, alpha=alpha)

    @classmethod
    def magenta(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with magenta hue."""
        return HColor.from_hls(hue=0.833, light=light, sat=sat, alpha=alpha)

    @classmethod
    def pink_magenta(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with pink_magenta hue."""
        return HColor.from_hls(hue=0.875, light=light, sat=sat, alpha=alpha)

    @classmethod
    def rose(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with rose hue."""
        return HColor.from_hls(hue=0.917, light=light, sat=sat, alpha=alpha)

    @classmethod
    def red_rose(cls, light: float = 0.5, sat: float = 0.5, alpha: float = 1.0) -> HColor:
        """HLS constructor for creating HColor class with red_rose hue."""
        return HColor.from_hls(hue=0.958, light=light, sat=sat, alpha=alpha)
