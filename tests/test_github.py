"""Example test class, to test github action"""

def uut(a:int,b:int) -> int:
    return a + b

def test_uut():
    assert uut(1,2) == 3