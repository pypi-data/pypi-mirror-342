import pytest
import sys

sys.path.insert(0, "src")
from common import spaces, blocks
from pybdp.toolbox import Toolbox


@pytest.fixture(scope="module")
def toolbox():
    json = {
        "Spaces": spaces,
        "Blocks": blocks,
    }
    return Toolbox(json)


def test_toolbox_spaces(toolbox):
    assert len(toolbox.spaces) == 5
    assert toolbox.spaces[0].id == "S1"
    assert toolbox.spaces[1].id == "S2"
    assert toolbox.spaces[2].id == "S3"
    assert toolbox.spaces[3].id == "S4"
    assert toolbox.spaces[4].id == "S5"
    assert str(toolbox.spaces[0]) == "< Space ID: S1 Name: A >"
    assert str(toolbox.spaces[1]) == "< Space ID: S2 Name: B >"
    assert str(toolbox.spaces[2]) == "< Space ID: S3 Name: C >"
    assert str(toolbox.spaces[3]) == "< Space ID: S4 Name: D >"
    assert str(toolbox.spaces[4]) == "< Space ID: S5 Name: E >"


def test_toolbox_blocks(toolbox):
    assert len(toolbox.blocks) == 3
    assert toolbox.blocks[0].id == "B1"
    assert toolbox.blocks[1].id == "B2"
    assert toolbox.blocks[2].id == "B3"
    assert str(toolbox.blocks[0]) == "< Block ID: B1 Name: Block 1 ['A', 'E']->['E']>"
    assert str(toolbox.blocks[1]) == "< Block ID: B2 Name: Block 2 ['E']->['C']>"
    assert str(toolbox.blocks[2]) == "< Block ID: B3 Name: Block 3 ['E', 'B']->['D']>"


def test_toolbox_mappings(toolbox):
    assert len(toolbox.blocks_map) == 3
    assert toolbox.blocks_map["B1"].id == "B1"
    assert toolbox.blocks_map["B2"].id == "B2"
    assert toolbox.blocks_map["B3"].id == "B3"

    assert len(toolbox.spaces_map) == 5
    assert toolbox.spaces_map["S1"].id == "S1"
    assert toolbox.spaces_map["S2"].id == "S2"
    assert toolbox.spaces_map["S3"].id == "S3"
    assert toolbox.spaces_map["S4"].id == "S4"
    assert toolbox.spaces_map["S5"].id == "S5"

    assert len(toolbox.toolbox_map) == 8
    assert toolbox.toolbox_map["S1"].id == "S1"
    assert toolbox.toolbox_map["S2"].id == "S2"
    assert toolbox.toolbox_map["S3"].id == "S3"
    assert toolbox.toolbox_map["S4"].id == "S4"
    assert toolbox.toolbox_map["S5"].id == "S5"
    assert toolbox.toolbox_map["B1"].id == "B1"
    assert toolbox.toolbox_map["B2"].id == "B2"
    assert toolbox.toolbox_map["B3"].id == "B3"
