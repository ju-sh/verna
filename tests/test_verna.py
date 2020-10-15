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


class TestToInt:
    @pytest.mark.parametrize('val,skip_types,expected', [
        ("50%", [], 128),
        (0.5, [], 128),
    ])
    def test_valid(self, val, skip_types, expected):
        assert Color.to_int(val, skip_types) == expected

    @pytest.mark.parametrize('val,skip_types', [
        ("50", []),
        (0.5, [float]),
    ])
    def test_invalid(self, val, skip_types):
        with pytest.raises(ValueError):
            assert Color.to_int(val, skip_types)


def test_from_name():
    assert Color.from_name('gainsboro') == 0xdcdcdc
