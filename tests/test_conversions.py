import pytest

from verna import Color


class TestToInt:
    """Test Color.to_int()"""
    @pytest.mark.parametrize('val,expected', [
        ("50%", 128),
        (1.0, 255),
        (1, 1),
        (0.754, 192),
        ("70%", 0xb3),
    ])
    def test_valid(self, val, expected):
        assert Color.to_int(val) == expected

    @pytest.mark.parametrize('val', [
        "120", 11.0
    ])
    def test_invalid(self, val):
        with pytest.raises(ValueError):
            Color.to_int(val)


class TestToFloat:
    """Test Color.to_float()"""
    @pytest.mark.parametrize('val,expected', [
        ("50%", 0.5019607843137255),
        (1.0, 1),
        (1, 0.00392156862745098)
    ])
    def test_valid(self, val, expected):
        assert Color.to_float(val) == expected

    @pytest.mark.parametrize('val', [
        "120", 11.0
    ])
    def test_invalid(self, val):
        with pytest.raises(ValueError):
            Color.to_float(val)


class TestToPercentage:
    """Test Color.to_percentage()"""
    @pytest.mark.parametrize('val,expected', [
        ("50%", 50.19607843137255),  # implicit conversion to int happens
        (1.0, 100.0),
        (128, 50.19607843137255)
    ])
    def test_valid(self, val, expected):
        assert Color.to_percentage(val) == expected

    @pytest.mark.parametrize('val', [
        "120", 11.0
    ])
    def test_invalid(self, val):
        with pytest.raises(ValueError):
            Color.to_percentage(val)
