import json
import time

from mcx import MCX

class Step:
    def __init__(self, steps):
        self.__steps = steps
        self._index = 0
    
    @property
    def step(self):
        return self.__steps[self._index]
    
    def next_step(self):
        if (len(self.__steps) - 2 != self._index):
            self._index += 1

ROBOT_NAME = "Robot1_1"
STEPS = ("GO_TO_FLASK", 
        "DESCENT_GO_TO_FLASK", 
        "CAPTURE_FLASK", 
        "UPPER_START_Z",
        "GO_TO_CAMERA", 
        "DESCENT_TO_CAMERA",
        "UPPER_START_Z",
        "GO_TO_FLASK",
        "DESCENT_GO_TO_FLASK",
        "REALESE_FLASK", 
        "UPPER_START_Z")
Z_FLASK = 0

def json_load(file_name):
    with open(file_name, 'r') as json_file:
        data_from_file = json.load(json_file)
    return data_from_file

def task_first(manipulate):
    point = input()
    coordinates = json_load("coordinates.json")

    steps = Step(STEPS)

    if point not in coordinates.keys():
        raise ValueError("Input wrong key-point")
    
    x, y = coordinates.get(point)
    camera_x, camera_y, camera_z = coordinates.get("camera")

    while True:
        if manipulate.getManipulatorStatus() == 0:
            match (steps.step):
                case("GO_TO_FLASK"):
                    manipulate.move(x, y, manipulate.z, 0, 0)
                case("DESCENT_GO_TO_FLASK"):
                    manipulate.move(manipulate.x, manipulate.y, Z_FLASK, 0, 0)
                case("CAPTURE_FLASK"):
                    manipulate.move(manipulate.x, manipulate.y, manipulate.z, 0, 1)
                case("UPPER_START_Z"):
                    manipulate.move(manipulate.x, manipulate.y, coordinates.get("start")[0], 0, 0)
                case("GO_TO_CAMERA"):
                    manipulate.move(manipulate.x, manipulate.y, coordinates.get("start")[0], 0, 0)
                case("DESCENT_TO_CAMERA"):
                    manipulate.move(manipulate.x, manipulate.y, camera_z, 0, 0)
                case("REALESE_FLASK"):
                    manipulate.move(manipulate.x, manipulate.y, manipulate.z, 0, 0)

            time.sleep(0.5)
        else:
            steps.next_step()

        if manipulate.getManipulatorWarning() != 0:
            print(manipulate.getManipulatorWarningStr())

task_first(MCX())
