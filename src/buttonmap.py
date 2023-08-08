import json
import math
from dotmap import DotMap


class ButtonMap:
    def __init__(self, json_path) -> None:
        with open(json_path) as file:
            data = DotMap(json.load(file))
            self.width = data["width"]
            self.height = data["height"]
            self.targets = data["targets"]

    def find_button(self, x, y, width):
        scale = self.width / width
        x *= scale
        y *= scale

        for target in self.targets:
            if pt_in_target(x, y, target):
                return target.action
        return False


def pt_in_target(x, y, target):
    if target.type == "circle":
        return target.r >= math.sqrt((x - target.x) ** 2 + (y - target.y) ** 2)
    elif target.type == "rectangle":
        return x >= target.x1 and x <= target.x2 and y >= target.y1 and y <= target.y2
