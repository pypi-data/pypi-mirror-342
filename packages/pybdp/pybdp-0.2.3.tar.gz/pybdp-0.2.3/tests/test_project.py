import pytest
import sys

sys.path.insert(0, "src")
from common import project_json
from pybdp.project import Project


@pytest.fixture(scope="module")
def project():
    return Project(project_json)


def test_project_toolbox(project):
    assert project.toolbox is not None
    assert len(project.toolbox.spaces) == 5
    assert len(project.toolbox.blocks) == 3


def test_project_workbench(project):
    assert project.workbench is not None
    assert len(project.workbench.processors) == 3
    assert len(project.workbench.wires) == 3
    assert len(project.workbench.systems) == 1


def test_project_systems(project):
    assert len(project.workbench.systems) == 1
    system = project.workbench.systems[0]
    assert system.id == "Sys1"
    assert system.name == "System 1"
    assert system.description == "My System"
    assert [processor.id for processor in system.processors] == ["P1", "P2", "P3"]
    assert [wire.id for wire in system.wires] == ["W1", "W2", "W3"]
