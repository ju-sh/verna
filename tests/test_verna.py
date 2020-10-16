import pytest

from verna import Color


class TestEdit:
    """Check if the property values can be modified"""
    @pytest.mark.parametrize('prop,color_hex,arg', [
        ('alpha', 0xeeff22aa, 0x1ff),    # > 0xff
        ('alpha', 0xeeff22aa, -1),       # < 0.0
        ('alpha', 0xeeff22aa, "120%"),   # > 100%
        ('alpha', 0xeeff22aa, "120"),    # No '%'
        ('alpha', 0xeeff22aa, 1.2),      # > 1.0
        ('alpha', 0xeeff22aa, True),     # Invalid type: bool

        ('red', 0xeeff22aa, 0x3ed),
        ('red', 0xeeff22aa, "399%"),
    ])
    def test_invalid_edit(self, prop, color_hex, arg):
        """Modifications that should raise exception"""
        color = Color(color_hex)
        with pytest.raises(ValueError):
            setattr(color, prop, arg)

    @pytest.mark.parametrize('prop,color_hex,arg,expected', [
        ('alpha', 0xeeff22aa, 0xff, 0xffff22aa),     # int/hex
        ('alpha', 0xeeff22aa, "50%", 0x80ff22aa),    # percentage
        ('alpha', 0xeeff22aa, 0.5, 0x80ff22aa),      # float

        ('red', 0xeeff22aa, 0xed, 0xeeed22aa),
        ('red', 0xeeff22aa, "99%", 0xeefc22aa),

        ('green', 0xeeff22aa, 0x58, 0xeeff58aa),
        ('green', 0xeeff22aa, "68%", 0xeeffadaa),

        ('blue', 0xeeff22aa, 0xbe, 0xeeff22be),
        ('blue', 0xeeff22aa, "59%", 0xeeff2296),
    ])
    def test_valid_edit(self, prop, color_hex, arg, expected):
        """Edit a color which already has an alpha value"""
        color = Color(color_hex)
        setattr(color, prop, arg)
        assert color.integer == expected


class TestPropAccess:
    """See if the different properties can be accessed"""
    @pytest.mark.parametrize('prop,color_hex,expected', [
        ('red', 0xeeff22aa, 0xff),
        ('green', 0xeeff22aa, 0x22),
        ('blue', 0xeeff22aa, 0xaa),
    ])
    def test_rgb(self, prop, color_hex, expected):
        color = Color(color_hex)
        assert getattr(color, prop) == expected

    def test_alpha(self):
        color = Color(0xeeff22aa)
        assert round(color.alpha, 2) == 0.93


class TestFromRGBA:
    def test_with_alpha(self):
        color = Color.from_rgba(0xef, 0xa1, 0xde, 0.5)
        assert color.integer == 0x80efa1de

    def test_without_alpha(self):
        color = Color.from_rgba(0xef, 0xa1, 0xde)
        assert color.integer == 0xefa1de


class TestDunders:
    """Test the magic methods of Color class"""
    def test_invalid_init(self):
        with pytest.raises(ValueError):
            Color(-1)

    def test_int(self):
        color = Color(0xeeff22aa)
        assert int(color) == 0xeeff22aa

    def test_repr(self):
        color = Color(0xeeff22aa)
        assert repr(color) == "<Color(4009697962)>"

    def test_str(self):
        color = Color(0xeeff22aa)
        assert str(color) == "eeff22aa"


class TestNormalize:
    @pytest.mark.parametrize('val,target,expected', [
        ("50%", "int", 128),
        (0.5, "int", 128),
        (120, "percentage", 47.05882352941176),
    ])
    def test_valid(self, val, target, expected):
        assert Color.normalize(val, target) == expected

    @pytest.mark.parametrize('val,target', [
        ("50", "int"),
        (0.55, "bool"),
    ])
    def test_invalid(self, val, target):
        with pytest.raises(ValueError):
            assert Color.normalize(val, target)


class TestReplace:
    @pytest.mark.parametrize('props,color_hex,expected', [
        ({'red': '50%', 'blue': 234}, 0x1abcdef, 0x180cdea),
        ({'red': None, 'green': None, 'blue': None, 'alpha': None},
         0x1abcdef, 0x1abcdef),
        ({'red': 1, 'green': '70%', 'blue': 181, 'alpha': 0},
         0x1abcdef, 0x0001b3b5),
        ({'red': 1.0, 'green': '70%', 'blue': 181, 'alpha': 0},
         0x1abcdef, 0xffb3b5),
    ])
    def test_valid(self, props, color_hex, expected):
        color = Color(color_hex)
        assert color.replace(**props).integer == expected

    def test_invalid(self):
        color = Color(0x1abcdef)
        with pytest.raises(ValueError):
            color.replace(red=True)


def test_from_name():
    assert Color.from_name('gainsboro') == Color(0xdcdcdc)


def test_rgba():
    color = Color(0x80abcdef)
    red, green, blue, alpha = color.rgba()
    alpha = round(alpha, 2)
    assert (red, green, blue, alpha) == (0xab, 0xcd, 0xef, 0.5)
