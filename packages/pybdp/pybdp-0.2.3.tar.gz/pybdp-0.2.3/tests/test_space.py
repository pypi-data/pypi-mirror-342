import sys

sys.path.insert(0, "src")
from common import spaces, blocks, processors, wires, systems, project_json
from pybdp.space import load_space


def test_load_space():
    space = load_space(spaces[0])
    assert space.id == "S1"
    assert space.name == "A"
    assert space.description == "Space 1"
    assert space.raw_data == spaces[0]
    assert str(space) == "< Space ID: S1 Name: A >"

    space = load_space(spaces[1])
    assert space.id == "S2"
    assert space.name == "B"
    assert space.description == None
    assert space.raw_data == spaces[1]
    assert str(space) == "< Space ID: S2 Name: B >"

    space = load_space(spaces[2])
    assert space.id == "S3"
    assert space.name == "C"
    assert space.description == "Space 3"
    assert space.raw_data == spaces[2]
    assert str(space) == "< Space ID: S3 Name: C >"

    space = load_space(spaces[3])
    assert space.id == "S4"
    assert space.name == "D"
    assert space.description == None
    assert space.raw_data == spaces[3]
    assert str(space) == "< Space ID: S4 Name: D >"

    space = load_space(spaces[4])
    assert space.id == "S5"
    assert space.name == "E"
    assert space.description == "Space 5"
    assert space.raw_data == spaces[4]
    assert str(space) == "< Space ID: S5 Name: E >"
