from main import *

import json

# steps = Steps((Step("Start"), Step("End")))
# print(steps.step)
# steps.next_step()
# print(steps.step)


def flask_move_test(steps: Steps, start_coordinates: list, camera_coordinates: list, point_coordinates, status):
    manipulate_x, manipulate_y, manipulate_z, _, _, _ = (0.1, 0.1, 0.1, None, None, None)
    strat_x, start_y, start_z = start_coordinates
    camera_x, camera_y, camera_z = camera_coordinates
    x, y, z = point_coordinates

    step = steps.step

    if status == 0:
        print(step.name)
        match step.name:
            case ("GO_TO_FLASK"):
                print(x, y, manipulate_z, step.is_graper)
            case ("DESCENT_GO_TO_FLASK"):
                print(manipulate_x, manipulate_y, Z_FLASK, int(step.is_graper))
            case ("CAPTURE_FLASK"):
                print(manipulate_x, manipulate_y, manipulate_z, 1)
            case ("UPPER_Z"):
                print(manipulate_x, manipulate_y, start_z, int(step.is_graper))
            case ("GO_TO_CAMERA"):
                print(manipulate_x, manipulate_y, start_z, 1)
            case ("DESCENT_TO_CAMERA"):
                print(manipulate_x, manipulate_y, camera_z, 1)
            case ("REALESE_FLASK"):
                print(manipulate_x, manipulate_y, manipulate_z, 0)
        steps.next_step()
        time.sleep(0.5)


def main_first_test():
    point = input()
    coordinates = json_load("coordinates.json")
    stepss = Steps(STEPS_FIRST)

    if point not in coordinates.keys():
        raise ValueError("Input wrong key-point")

    while True:
        status = int(input())
        flask_move_test(stepss, coordinates.get('start'),
                   coordinates.get('camera'),
                   (*coordinates.get(point), 95), status)

# create_video()
# create_video()
