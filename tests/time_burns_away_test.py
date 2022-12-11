from time_burns_away import _convert2second


def test__convert2second():
    assert 3600 + 2 * 60 == _convert2second("01:02")
