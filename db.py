from typing import Dict
import json


def read_data() -> Dict:
    with open("workflows.json", "r") as f:
        return json.load(f)


def save_workflow(workflow: Dict):
    with open("workflows.json", "r") as f:
        data: Dict = json.load(f)

    for w in data["workflows"]:
        if w["id"] == workflow["id"]:
            w.update(workflow)
            break

    with open("workflows.json", "w") as f:
        json.dump(data, f)


def read_names() -> Dict:
    with open("names.json", "r") as f:
        return json.load(f)


if __name__ == "__main__":
    workflows = read_data()
    save_workflow({"id": "Foo",
                   "nodes": [
                       {"fill": "#3f51b5", "id": 0, "x": 0, "y": 20},
                       {"fill": "#9c27b0", "id": 1, "x": 200, "y": 120},
                       {"id": 3, "x": 67, "y": 343, "fill": "#9c27b0"},
                       {"id": 4, "x": 343, "y": 324, "fill": "#673ab7"}
                   ]})
