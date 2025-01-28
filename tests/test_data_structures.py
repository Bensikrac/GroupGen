import pytest
from src.data_structures import Participant


def test_participant():
    ed = dict()
    fd = {"fez": "baz"}
    fdd = {"foo": "bar"}
    p = Participant()
    assert p.uid == 0
    assert p.attributes == ed
    with pytest.raises(Exception):
        p["test"]
        p.uid = 3
        p.attributes = fd
    p.attributes["foo"] = "bar"
    assert p["foo"] == "bar"
    p = Participant(2)
    assert p.uid == 2
    assert p.attributes == ed
    p = Participant(fd, 5)
    assert p.uid == 5
    assert p.attributes == fd
    assert p["fez"] == "baz"
    p = Participant(8, fd)
    assert p.uid == 8
    assert p.attributes == fd
    assert p["fez"] == "baz"
    p = Participant(1, 2, fd)
    assert p.uid == 2
    assert p.attributes == fd
    assert p["fez"] == "baz"
    p = Participant(11, fd, 21, ed)
    assert p.uid == 21
    assert p.attributes == ed
    p = Participant(31, foo="bar")
    assert p.uid == 31
    assert p.attributes == fdd
    assert p["foo"] == "bar"
    p = Participant(42, fd, foo="bar")
    assert p.uid == 42
    assert p.attributes == (fd | fdd)
    assert p["fez"] == "baz"
    assert p["foo"] == "bar"
    p1 = Participant(1)
    p2 = Participant(2)
    assert p1 != p2
    p2 = Participant(1)
    assert p1 == p2
