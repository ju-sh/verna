"""
Data structures used to handle colors in Verna
"""

from typing import Union, List

from verna import names


class Color(int):
    """
    Represents a color.

    Only RGB scheme is supported.
    """
    def __init__(self, integer: int):
        super().__init__()
        if integer < 0 or integer > 0xffffffff:
            raise ValueError
        self.integer = integer

    def __int__(self):
        return self.integer

    def __repr__(self):
        return f"<Color({self.integer})>"

    def __str__(self):
        """Return core value in hex form as a string with out any prefix"""
        return hex(self.integer)[2:]

    def replace(self,
                red: Union[int, str] = None,             
                green: Union[int, str] = None,             
                blue: Union[int, str] = None,             
                alpha: Union[float, str] = None) -> 'Color':
        """

        """
        if red is None:
            red_int = self.red
        else:
            red_int = self.to_int(red, skip_types=[float])

        if green is None:
            green_int = self.green
        else:
            green_int = self.to_int(green, skip_types=[float])

        if blue is None:
            blue_int = self.blue
        else:
            blue_int = self.to_int(blue, skip_types=[float])

        if alpha is None:
            alpha_int = self.alpha
        else:
            alpha_int = self.to_int(alpha)

        return self.__class__.from_rgba(red_int, green_int,
                                        blue_int, alpha_int)

    @classmethod
    def from_name(cls, name: str) -> 'Color':
        """
        Return a Color object based on the given color name.

        Only CSS3 extended color keyword names are supported.
        """
        name = name.lower()
        return cls(names.COLORS[name])

    @classmethod
    def from_rgba(cls,
                  red: Union[int, str],
                  green: Union[int, str],
                  blue: Union[int, str],
                  alpha: Union[float, str] = 0) -> 'Color':
        """
        Return a Color object from a set of RGBA values
        """
        red_int = cls.to_int(red, skip_types=[float])
        green_int = cls.to_int(green, skip_types=[float])
        blue_int = cls.to_int(blue, skip_types=[float])
        alpha_int = cls.to_int(alpha)
        integer = ((alpha_int << 24) | (red_int << 16)
                   | (green_int << 8) | blue_int)
        return cls(integer)

    @staticmethod
    def to_int(val: Union[float, str],
               skip_types: List[type] = None) -> int:
        """
        Convert float percentage strings, floats in [0,1] or ints in [0,255]
        to equivalent ints.

        Skip conversion if type of val is in skip_types.

        Used to validate color component values.

        Return equivalent int in [0, 255] if conversion is possible.
        Otherwise return None.

        Note: This function is used by the property getter-setters.
        """

        if skip_types is None:
            skip_types = []

        if (type(val) in skip_types) or (type(val) not in [int, float, str]):
            raise ValueError("Invalid value type")

        if isinstance(val, str):
            # For str, the value should be a float percentage
            # with a '%' symbol at the end.
            val = val.strip()
            if val[-1] != "%":
                raise ValueError("String args must be percentages")

            percent_val = float(val[:-1])
            if percent_val < 0 or percent_val > 100:
                raise ValueError("Invalid percentage")
            int_val = round((percent_val/100) * 0xff)

        elif isinstance(val, int):
            # For int, value should be between 0 and 255 (inclusive)
            if val < 0 or val > 255:
                raise ValueError("Invalid value")
            int_val = val

        else:
            # By this point, val must be a float
            # For float, value should be between 0.0 and 1.0 (inclusive)
            if val < 0 or val > 1:
                raise ValueError("Invalid value")
            int_val = round(val * 0xff)

        return int_val

    @property
    def alpha(self) -> float:
        """
        Alpha value ranges from 0 to 1.0
        """
        return (self.integer >> 24) / 0xff

    @alpha.setter
    def alpha(self, val: Union[float, str]):
        val_int = self.to_int(val)
        self.integer = (val_int << 24) | (self.integer & 0x00ffffff)

    @property
    def red(self) -> int:
        """
        Red value ranges from 0 to 255
        """
        return (self.integer >> 16) & 0xff

    @red.setter
    def red(self, val: Union[float, str]):
        val_int = self.to_int(val)
        self.integer = (val_int << 16) | (self.integer & 0xff00ffff)

    @property
    def green(self) -> int:
        """
        Grren value ranges from 0 to 255
        """
        return (self.integer >> 8) & 0xff

    @green.setter
    def green(self, val: Union[float, str]):
        val_int = self.to_int(val)
        self.integer = (val_int << 8) | (self.integer & 0xffff00ff)

    @property
    def blue(self) -> int:
        """
        Blue value ranges from 0 to 255
        """
        return self.integer & 0xff

    @blue.setter
    def blue(self, val: Union[float, str]):
        val_int = self.to_int(val)
        self.integer = val_int | (self.integer & 0xffffff00)
