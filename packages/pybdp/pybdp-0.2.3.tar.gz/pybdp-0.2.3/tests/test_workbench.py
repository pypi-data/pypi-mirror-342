import pytest
import sys

sys.path.append("src")
from common import processors, wires, systems
from pybdp.workbench import Workbench
from test_toolbox import toolbox


@pytest.fixture(scope="module")
def workbench(toolbox):
    json = {
        "Processors": processors,
        "Wires": wires,
        "Systems": systems,
    }
    return Workbench(json, toolbox.blocks_map, toolbox.spaces_map)


def test_workbench_processors(workbench):
    assert len(workbench.processors) == 3
    assert workbench.processors[0].id == "P1"
    assert workbench.processors[1].id == "P2"
    assert workbench.processors[2].id == "P3"


def test_workbench_wires(workbench):
    assert len(workbench.wires) == 3
    assert workbench.wires[0].id == "W1"
    assert workbench.wires[1].id == "W2"
    assert workbench.wires[2].id == "W3"


def test_workbench_systems(workbench):
    assert len(workbench.systems) == 1
    assert workbench.systems[0].id == "Sys1"
    assert workbench.systems[0].name == "System 1"
    assert workbench.systems[0].description == "My System"
    assert [processor.id for processor in workbench.systems[0].processors] == [
        "P1",
        "P2",
        "P3",
    ]
    assert [wire.id for wire in workbench.systems[0].wires] == ["W1", "W2", "W3"]
