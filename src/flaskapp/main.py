import os
from flask import Flask, request, render_template
from controller import Controller, TV_IP
from buttonmap import ButtonMap

PORT = 10101
BUTTON_MAP_PATH = "./data/button_map.json"

# load up the buttons
# TODO probably change this into a remote class instead
remote_buttons = ButtonMap(BUTTON_MAP_PATH)

# init a controller connection
controller = Controller()
controller.connect(TV_IP)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/remote_event")
def command():
    try:
        x = int(request.args["x"])
        y = int(request.args["y"])
        w = int(request.args["w"])
        h = int(request.args["h"])
        action = remote_buttons.find_button(x, y, w)
        if action:
            print(action)
            controller.key_event(action)

    except Exception as e:
        print(e)
        return "Error", 400
    return "Success", 200


def start_app():
    app.run(port=PORT)
    os.chdir("./flask")
