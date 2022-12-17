from time_burns_away import _convert2second
import pytest


@pytest.mark.parametrize(
    ("input_hhmm", "expected"),
    (
        ("1:0", 3600),
        ("0:1", 60),
        ("3:5", 11100),
    ),
)
def test__convert2second(input_hhmm, expected):
    assert expected == _convert2second(input_hhmm)
