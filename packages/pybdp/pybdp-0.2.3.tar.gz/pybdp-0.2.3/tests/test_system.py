import pytest
import sys

sys.path.insert(0, "src")
from common import systems, processors, wires
from pybdp.system import load_system
from pybdp.processor import load_processor
from pybdp.wire import load_wire
from test_toolbox import toolbox


@pytest.fixture(scope="module")
def system(toolbox):
    processors_map = {}
    wires_map = {}
    for processor in processors:
        processors_map[processor["ID"]] = load_processor(
            processor, toolbox.blocks_map, toolbox.spaces_map
        )
    for wire in wires:
        wires_map[wire["ID"]] = load_wire(wire, processors_map, toolbox.spaces_map)
    return load_system(systems[0], processors_map, wires_map)


def test_load_system(system):
    assert system.id == "Sys1"
    assert system.name == "System 1"
    assert system.description == "My System"
    assert [processor.id for processor in system.processors] == ["P1", "P2", "P3"]
    assert [wire.id for wire in system.wires] == ["W1", "W2", "W3"]


def test_system_processors(system):
    assert len(system.processors) == 3
    assert system.processors[0].id == "P1"
    assert system.processors[1].id == "P2"
    assert system.processors[2].id == "P3"


def test_system_wires(system):
    assert len(system.wires) == 3
    assert system.wires[0].id == "W1"
    assert system.wires[1].id == "W2"
    assert system.wires[2].id == "W3"


def test_get_available_terminals(system):
    terminals_open_only = system.get_available_terminals(open_only=True)
    terminals_all = system.get_available_terminals(open_only=False)

    terminals_open_only = [[str(x[0]), x[1], str(x[2])] for x in terminals_open_only]
    terminals_all = [[str(x[0]), x[1], str(x[2])] for x in terminals_all]

    assert len(terminals_open_only) == 2, "There should be 2 open terminals"
    assert terminals_open_only == [
        [
            "< Processor ID: P2 Name: Processor 2 ['E']->['C']>",
            0,
            "< Space ID: S3 Name: C >",
        ],
        [
            "< Processor ID: P3 Name: Processor 3 ['E', 'B']->['D']>",
            0,
            "< Space ID: S4 Name: D >",
        ],
    ]

    assert len(terminals_all) == 3, "There should be 3 terminals in total"

    assert terminals_all == [
        [
            "< Processor ID: P1 Name: Processor 1 ['A', 'E']->['E']>",
            0,
            "< Space ID: S5 Name: E >",
        ],
        [
            "< Processor ID: P2 Name: Processor 2 ['E']->['C']>",
            0,
            "< Space ID: S3 Name: C >",
        ],
        [
            "< Processor ID: P3 Name: Processor 3 ['E', 'B']->['D']>",
            0,
            "< Space ID: S4 Name: D >",
        ],
    ]


def test_get_open_ports(system):
    open_ports = system.get_open_ports()
    open_ports = [[str(x[0]), x[1], str(x[2])] for x in open_ports]

    assert len(open_ports) == 2, "There should be 2 open ports"
    print(open_ports)
    assert open_ports == [
        [
            "< Processor ID: P1 Name: Processor 1 ['A', 'E']->['E']>",
            0,
            "< Space ID: S1 Name: A >",
        ],
        [
            "< Processor ID: P3 Name: Processor 3 ['E', 'B']->['D']>",
            1,
            "< Space ID: S2 Name: B >",
        ],
    ]


def test_is_connected(system):
    assert system.is_connected() == True


def test_is_directed(system):
    assert system.is_directed() == False


def test_is_valid(system):
    assert system.is_valid() == False


def test_is_dynamical(system):
    assert system.is_dynamical() == True


def test_connected_components(system):
    components = system.get_connected_components()
    assert len(components) == 1, "There should be 1 cluster of connected component"
    assert sorted([processor.id for processor in components[0]]) == ["P1", "P2", "P3"]


def test_get_hierarchy(system):
    hierarchy = system.get_hierarchy()
    assert len(hierarchy) == 3, "There should be 3 entries in the hierarchy"
    assert (
        str(hierarchy["P1"])
        == "< Processor ID: P1 Name: Processor 1 ['A', 'E']->['E']>"
    )
    assert str(hierarchy["P2"]) == "< Processor ID: P2 Name: Processor 2 ['E']->['C']>"
    assert (
        str(hierarchy["P3"])
        == "< Processor ID: P3 Name: Processor 3 ['E', 'B']->['D']>"
    )


def test_get_spaces(system):
    spaces = system.get_spaces()
    assert len(spaces) == 5, "There should be 5 spaces"
    assert sorted([space.id for space in spaces]) == ["S1", "S2", "S3", "S4", "S5"]


def test_get_subsystems(system):
    subsystems = system.get_subsystems()
    assert len(subsystems) == 0, "There should be no subsystems"
