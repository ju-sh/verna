import pytest

from verna import Color


class TestToInt:
    """Test Color.to_int()"""
    @pytest.mark.parametrize('val,expected', [
        (1.0, 255),
        (0.754, 192),
        (0.47, 0x78),
        (1, 1),
        (245, 245),
    ])
    def test_valid(self, val, expected):
        assert Color.to_int(val) == expected

    @pytest.mark.parametrize('val', [
        "120",  # invalid type
        11.0,   # > 1.0
        -0.32,  # < 0.0
        -32,    # < 0
        True,   # invalid type
    ])
    def test_invalid(self, val):
        with pytest.raises(ValueError):
            Color.to_int(val)


@pytest.mark.parametrize('val,expected', [
    (1.0, 1),
    (0x2e, 0.1803921568627451)
])
def test_to_float(val, expected):
    """Test Color.to_float()"""
    assert Color.to_float(val) == expected
