from mlb_learning import myfunctions
# content of test_sample.py
def test_dummy():
    someVar = 2
    assert 2 == someVar

def test_zero():
    assert myfunctions.zero() == 0