import pytest
import sys

sys.path.insert(0, "src")
from common import wires, processors
from pybdp.wire import load_wire
from test_toolbox import toolbox
from pybdp.processor import load_processor


@pytest.fixture(scope="module")
def processors_map(toolbox):
    d = {}
    for processor in processors:
        p = load_processor(processor, toolbox.blocks_map, toolbox.spaces_map)
        d[p.id] = p

    return d


@pytest.fixture(scope="module")
def spaces_map(toolbox):
    return toolbox.spaces_map


def test_load_wire(processors_map, spaces_map):
    wire = load_wire(wires[0], processors_map, spaces_map)
    assert wire.id == "W1"
    assert wire.parent.id == "S5"
    assert wire.source["Processor"].id == "P1"
    assert wire.source["Index"] == 0
    assert wire.target["Processor"].id == "P2"
    assert wire.target["Index"] == 0
    assert wire.raw_data == wires[0]
    assert (
        str(wire)
        == "< Wire ID: W1 Space: E Source: (Processor 1, 0) Target: (Processor 2, 0) >"
    )

    wire = load_wire(wires[1], processors_map, spaces_map)
    assert wire.id == "W2"
    assert wire.parent.id == "S5"
    assert wire.source["Processor"].id == "P1"
    assert wire.source["Index"] == 0
    assert wire.target["Processor"].id == "P3"
    assert wire.target["Index"] == 0
    assert wire.raw_data == wires[1]
    assert (
        str(wire)
        == "< Wire ID: W2 Space: E Source: (Processor 1, 0) Target: (Processor 3, 0) >"
    )

    wire = load_wire(wires[2], processors_map, spaces_map)
    assert wire.id == "W3"
    assert wire.parent.id == "S5"
    assert wire.source["Processor"].id == "P1"
    assert wire.source["Index"] == 0
    assert wire.target["Processor"].id == "P1"
    assert wire.target["Index"] == 1
    assert wire.raw_data == wires[2]
    assert (
        str(wire)
        == "< Wire ID: W3 Space: E Source: (Processor 1, 0) Target: (Processor 1, 1) >"
    )
