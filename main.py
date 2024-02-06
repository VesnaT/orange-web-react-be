import random
from typing import Dict

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from db import read_data, save_workflow, read_names

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def home():
    return "Hello Orange Web"


@app.route("/data", methods=["GET"])
def get_data() -> Dict:
    return read_data()


@app.route("/name/<workflow_id>", methods=["GET"])
def get_name(workflow_id: str) -> Dict:
    names = read_names()["names"]
    data = read_data()
    workflows = data["workflows"]
    workflow = next(filter(lambda w: w["id"] == workflow_id, workflows), None)
    # if workflow is None:
    #     return "Workflow not found", 404

    forbidden_names = [node["name"] for node in workflow["nodes"]]
    available_names = [name for name in names if name not in forbidden_names]
    # if len(available_names) == 0:
    #     return "No available names", 404

    return {"name": random.choice(available_names)}


@app.route("/data", methods=["POST"])
def set_data():
    data = request.get_json(force=True)
    try:
        session_id = data.pop("sessionID")
        save_workflow(data)
        emit("updated", {"workflowID": data["id"], "sessionID": session_id},
             namespace="/", broadcast=True)
    except Exception as e:
        pass
    return data


if __name__ == "__main__":
    socketio.run(app)
