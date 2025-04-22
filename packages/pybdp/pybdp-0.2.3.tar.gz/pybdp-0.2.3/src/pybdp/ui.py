from .project import Project
import json


def create_empty_project():
    json = {
        "Toolbox": {
            "Spaces": [],
            "Blocks": [],
        },
        "Workbench": {
            "Processors": [],
            "Wires": [],
            "Systems": [],
        },
    }
    return Project(json)


def load_from_json(path):
    """
    Load a project from a JSON file.
    """
    with open(path, "r") as f:
        json_content = json.load(f)
    return Project(json_content)
