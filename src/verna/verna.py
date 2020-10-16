"""
Data structures used to handle colors in Verna
"""

from typing import Union, List, Tuple
import colorsys

from verna import names

def _round(val: float) -> int:
    """
    Built-in round() rounds towards an even value if val is equidistant from both
    limits as in examples below.
    >>> round(1.5)  # 2
    >>> round(2.5)  # 2
    >>> round(3.5)  # 4

    This function will round towards higher value in similar situations.
    >>> _round(1.5)  # 2
    >>> _round(2.5)  # 3
    >>> _round(3.5)  # 4
    >>> _round(4.4)  # 4
    >>> _round(5.6)  # 6
    """
    val_str = str(val)
    if ('.' in val_str) and (val_str[-1] == '5'):
        val_str = val_str[:-1] + '6'
    return round(float(val_str))


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
        Return a new Color by changing properties of a pre-existing instance.
        """
        if red is None:
            red_int = self.red
        else:
            red_int = self.normalize(red, skip_types=[float])

        if green is None:
            green_int = self.green
        else:
            green_int = self.normalize(green, skip_types=[float])

        if blue is None:
            blue_int = self.blue
        else:
            blue_int = self.normalize(blue, skip_types=[float])

        if alpha is None:
            alpha_int = self.alpha
        else:
            alpha_int = self.normalize(alpha)

        return self.__class__.from_rgba(red_int, green_int,
                                        blue_int, alpha_int)

    def rgba(self) -> Tuple[int, int, int, int]:
        """Return red, green, blue, alpha as a tuple in that order"""
        return self.red, self.green, self.blue, self.alpha

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
        red_int = cls.normalize(red, skip_types=[float])
        green_int = cls.normalize(green, skip_types=[float])
        blue_int = cls.normalize(blue, skip_types=[float])
        alpha_int = cls.normalize(alpha)
        integer = ((alpha_int << 24) | (red_int << 16)
                   | (green_int << 8) | blue_int)
        return cls(integer)

    @classmethod
    def to_float(cls, val: Union[float, str]) -> float:
        """
        Return equivalent float ranging from 0.0 to 1.0 from:
         - a percentage in string form with a '%' at end (eg: "50%" -> 0.5)
         - a int ranging from 0 to 255 (eg: 255 -> 1.0)
        Value of val is returned unchanged if it is a float from 0.0 to 1.0

        Raises ValueError if conversion cannot be performed.
        """
        return cls.normalize(val, target='float')

    
    @classmethod
    def to_percentage(cls, val: Union[float, str]) -> float:
        """
        Return equivalent percentage as a float ranging from 0.0 to 100.0 from:
         - a percentage in string form with a '%' at end (eg: "50%" -> 50.0)
         - a int ranging from 0 to 255 (eg: 255 -> 100.0)
         - a float ranging from 0 to 1.0 (eg: 0.5 -> 50.0)

        Raises ValueError if conversion cannot be performed.

        val is first converted to an int which is then converted to a
        percentage float value.

        Note: Returned value would be a value with decimal point that may need
        to be rounded to fit CSS values.
        For example: to_percentage(128) would return 50.19607843137255
        which you may want to round() to 50

        Note: val is first converted to an int before conversion to percentage
        is performed. This means that
        to_percentage("50%") gives 50.19607843137255
        """
        return cls.normalize(val, target='percentage')

    @classmethod
    def to_int(cls, val: Union[float, str]) -> int:
        """
        Return equivalent int ranging from 0 to 255 from:
         - a percentage in string form with a '%' at end (eg: "50%" -> 128)
         - a float ranging from 0 to 1.0 (eg: 0.5 -> 128)
        Value of val is returned unchanged if it is an integer from 0 to 255.

        Raises ValueError if conversion cannot be performed.
        """
        return cls.normalize(val, target='int')

    @staticmethod
    def normalize(val: Union[float, str],
                  skip_types: List[type] = None,
                  target: str = 'int') -> float:
        """
        Convert one of the following values of val:
         - percentage value as a string with '%' at end (eg: "50%"),
         - float value ranging from 0 to 0.1 (eg: 0.5)
         - int value ranging from 0 to 255 (eg: 128)
        to an equivalent value of the specified target type which ranges from:
         - 0 to 255 for 'int'
         - 0.0 to 1.0 for 'float'
         - 0.0 to 100.0 for 'percentage'

        Skip conversion if type of val is in skip_types.

        Used to validate color component values.

        Returns equivalent value of specified target type.

        Raises ValueError if conversion cannot be done or
        for invalid target type.

        Note: Property getter-setters of this class relies on this function.
        """

        target = target.lower()
        if target not in ['int', 'percentage', 'float']:
            raise ValueError(f"{target}: Unknown conversion target type")

        if skip_types is None:
            skip_types = []

        #if (type(val) in skip_types) or (type(val) not in [int, float, str]):
        if (isinstance(val, tuple(skip_types))
            or not isinstance(val, (int, float, str))):
            #XXX: make skip types arg a tuple instead of list
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
            int_val = _round((percent_val/100) * 0xff)

        elif isinstance(val, int) and not isinstance(val, bool):
            # For int, value should be between 0 and 255 (inclusive)
            if val < 0 or val > 255:
                raise ValueError("Invalid value")
            int_val = val

        elif not isinstance(val, bool):
            # By this point, val must be a float
            # For float, value should be between 0.0 and 1.0 (inclusive)
            if val < 0 or val > 1:
                raise ValueError("Invalid value")
            int_val = _round(val * 0xff)
        else:
            raise ValueError("Invalid value")

        if target == "int":
            return int_val
        if target == "float":
            return int_val / 0xff
        if target == "percentage":
            return (int_val / 0xff) * 100.0

    @property
    def alpha(self) -> float:
        """
        Alpha value ranges from 0 to 1.0
        """
        return (self.integer >> 24) / 0xff

    @alpha.setter
    def alpha(self, val: Union[float, str]):
        val_int = self.normalize(val)
        self.integer = (val_int << 24) | (self.integer & 0x00ffffff)

    @property
    def red(self) -> int:
        """
        Red value ranges from 0 to 255
        """
        return (self.integer >> 16) & 0xff

    @red.setter
    def red(self, val: Union[float, str]):
        val_int = self.normalize(val)
        self.integer = (val_int << 16) | (self.integer & 0xff00ffff)

    @property
    def green(self) -> int:
        """
        Grren value ranges from 0 to 255
        """
        return (self.integer >> 8) & 0xff

    @green.setter
    def green(self, val: Union[float, str]):
        val_int = self.normalize(val)
        self.integer = (val_int << 8) | (self.integer & 0xffff00ff)

    @property
    def blue(self) -> int:
        """
        Blue value ranges from 0 to 255
        """
        return self.integer & 0xff

    @blue.setter
    def blue(self, val: Union[float, str]):
        val_int = self.normalize(val)
        self.integer = val_int | (self.integer & 0xffffff00)

#XXX: Rename to_int() to _normalize() and create a to_int??
