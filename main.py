import json

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from db import read_data, save_workflow

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def home():
    return "Hello Orange Web"


@app.route("/data", methods=["GET"])
def get_data():
    return read_data()


@app.route("/data", methods=["POST"])
def set_data():
    print(request)
    print(request.get_json(force=True))
    data = request.get_json(force=True)
    save_workflow(data)
    return data


@socketio.on("connect")
def connected():
    # print(request.sid)
    print("user connected")
    # emit("connect", {"data": f"id: {request.sid} is connected"})


@socketio.on("dot")
def handle_dot(data: str):
    print("data from the front end!!")
    print(data)
    print("END")
    save_workflow(json.loads(data))
    emit("dot", data, broadcast=True)


@socketio.on("disconnect")
def disconnected():
    print("user disconnected")
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
