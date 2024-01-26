from typing import Dict
import json


def read_data() -> Dict:
    with open("workflows.json", "r") as f:
        return json.load(f)


def save_data(workflows_data: Dict):
    with open("workflows.json", "r") as f:
        data: Dict = json.load(f)

    data.update(workflows_data)

    with open("workflows.json", "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    workflows = read_data()
    print(workflows)
