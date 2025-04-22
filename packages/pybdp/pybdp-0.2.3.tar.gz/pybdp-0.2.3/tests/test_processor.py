import pytest
import sys

sys.path.insert(0, "src")
from common import processors
from pybdp.processor import load_processor
from test_toolbox import toolbox


@pytest.fixture(scope="module")
def blocks_map(toolbox):
    return toolbox.blocks_map


@pytest.fixture(scope="module")
def spaces_map(toolbox):
    return toolbox.spaces_map


def test_load_processor(blocks_map, spaces_map):
    processor = load_processor(processors[0], blocks_map, spaces_map)
    assert processor.id == "P1"
    assert processor.name == "Processor 1"
    assert processor.description == "Processor 1"
    assert processor.parent.id == "B1"
    assert [port.id for port in processor.ports] == ["S1", "S5"]
    assert [terminal.id for terminal in processor.terminals] == ["S5"]
    assert processor.raw_data == processors[0]
    assert str(processor) == "< Processor ID: P1 Name: Processor 1 ['A', 'E']->['E']>"

    processor = load_processor(processors[1], blocks_map, spaces_map)
    assert processor.id == "P2"
    assert processor.name == "Processor 2"
    assert processor.description == None
    assert processor.parent.id == "B2"
    assert [port.id for port in processor.ports] == ["S5"]
    assert [terminal.id for terminal in processor.terminals] == ["S3"]
    assert processor.raw_data == processors[1]
    assert str(processor) == "< Processor ID: P2 Name: Processor 2 ['E']->['C']>"

    processor = load_processor(processors[2], blocks_map, spaces_map)
    assert processor.id == "P3"
    assert processor.name == "Processor 3"
    assert processor.description == None
    assert processor.parent.id == "B3"
    assert [port.id for port in processor.ports] == ["S5", "S2"]
    assert [terminal.id for terminal in processor.terminals] == ["S4"]
    assert processor.raw_data == processors[2]
    assert str(processor) == "< Processor ID: P3 Name: Processor 3 ['E', 'B']->['D']>"


def test_is_primitive(blocks_map, spaces_map):
    processor = load_processor(processors[0], blocks_map, spaces_map)
    assert processor.is_primitive() == True

    processor = load_processor(processors[1], blocks_map, spaces_map)
    assert processor.is_primitive() == True

    processor = load_processor(processors[2], blocks_map, spaces_map)
    assert processor.is_primitive() == True


def test_get_system(blocks_map, spaces_map):
    processor = load_processor(processors[0], blocks_map, spaces_map)
    assert processor.get_system() == None

    processor = load_processor(processors[1], blocks_map, spaces_map)
    assert processor.get_system() == None

    processor = load_processor(processors[2], blocks_map, spaces_map)
    assert processor.get_system() == None


def test_get_shape(blocks_map, spaces_map):
    processor = load_processor(processors[0], blocks_map, spaces_map)
    assert processor.get_shape().id == "B1"

    processor = load_processor(processors[1], blocks_map, spaces_map)
    assert processor.get_shape().id == "B2"

    processor = load_processor(processors[2], blocks_map, spaces_map)
    assert processor.get_shape().id == "B3"
