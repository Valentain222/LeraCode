import json
import time
import os

import numpy as np
import cv2

from mcx import MCX


class Step:
    def __init__(self, name: str, is_graper: bool = False, angle: int = 0):
        self.name = name
        self.is_graper = is_graper
        self.angle = 0

    def __str__(self):
        return self.name


class Steps:
    def __init__(self, steps):
        self.__steps = steps
        self._index = 0

    @property
    def step(self):
        return self.__steps[self._index]

    def next_step(self):
        if len(self.__steps) - 1 > self._index:
            self._index += 1

    @property
    def is_stop(self):
        return True if self._index == len(self.__steps) - 1 else False



ROBOT_NAME = "Robot9_1"

GO_TO_FLASK_STEPS = (
    Step("GO_TO_FLASK"),
    Step("DESCENT_GO_TO_FLASK"),
    Step("CAPTURE_FLASK"),
    Step("UPPER_Z", True),
)

GO_TO_CAMERA_STEPS = (
    Step("GO_TO_CAMERA"),
    Step("DESCENT_TO_CAMERA"),
)

EXIT_FLASK = (
    Step("UPPER_Z", True),
    Step("GO_TO_FLASK", True),
    Step("DESCENT_GO_TO_FLASK", True),
    Step("RELEASE_FLASK"),
    Step("GO_TO_START")
)

STEPS_FIRST = (
    *GO_TO_FLASK_STEPS,
    *GO_TO_CAMERA_STEPS,
    *EXIT_FLASK
)

STEPS_SECOND = (
    *GO_TO_FLASK_STEPS,
    *GO_TO_CAMERA_STEPS,
    Step("ROTATE_FLASK", angle=45),
    *EXIT_FLASK
)

STEPS_THIRD = (
    *GO_TO_FLASK_STEPS,
    *GO_TO_CAMERA_STEPS,
    Step("RECEIVE_FLASK"),
    *EXIT_FLASK
)

Z_FLASK = 95
COUNT_IMAGES = 8
NUMBER_VIDEOS = 1
VIDEO_SIZE = (500, 500)


def get_image(manipulate: MCX):
    image_byte = manipulate.getCamera1Image()
    if image_byte:
        image_np = np.frombuffer(image_byte, np.uint8)
        image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        return image_np
    return None


def create_video():
    global NUMBER_VIDEOS

    writer = cv2.VideoWriter(f"Video_{NUMBER_VIDEOS}.mgp", cv2.VideoWriter_fourcc(*'MPEG'), 30, VIDEO_SIZE)
    images = [cv2.imread(f'tempPhotos/{file_name}') for file_name in os.listdir('tempPhotos/')]

    for image in images:
        image = cv2.resize(image, VIDEO_SIZE)
        writer.write(image)

    writer.release()

    for file in os.listdir('tempPhotos/'):
        os.remove(f'tempPhotos/{file}')

def json_load(file_name):
    with open(file_name, 'r') as json_file:
        data_from_file = json.load(json_file)
    return data_from_file


# Tree variant of function
def manipulate_move(manipulate, x, y, z, t, grapper):
    new_x = 0.1
    # manipulate.move(ROBOT_NAME, x, y, z, t, grapper)
    # -----------------------------------------------
    # while manipulate.getManipulatorStatus == 0:
    #     manipulate.move(ROBOT_NAME, x-new_x, y, z, t, grapper)
    #     new_x *= -1 
    #     time.sleep(0.5)
    # -----------------------------------------------
    start_counter = manipulate.getManipulatorCount()
    current_counter = start_counter
    while current_counter - start_counter != 0:
        manipulate.move(ROBOT_NAME, x-new_x, y, z, t, grapper)
        new_x *= -1 
        time.sleep(0.5)


def flask_move(manipulate: MCX, steps: Steps, start_coordinates: list, camera_coordinates: list, point_coordinates):
    manipulate_x, manipulate_y, manipulate_z, rotate_x, rotate_y, rotate_z = manipulate.getManipulatorMotor()
    strat_x, start_y, start_z = start_coordinates
    camera_x, camera_y, camera_z = camera_coordinates
    x, y, z = point_coordinates

    step = steps.step

    # print(f'Step: {Step}')
    # print(f"Manipulate coordinates: {manipulate_x, manipulate_y, manipulate_z}")
    # print(f'Rotates coordinates: {rotate_x, rotate_y, rotate_z}')
    # print(f'Status: {manipulate.getManipulatorStatus()}')
    if manipulate.getManipulatorStatus() == 0:
        print(f"Step: {step}")
        match step.name:
            case ("GO_TO_FLASK"):
                manipulate_move(manipulate, x, y, manipulate_z, 0, int(step.is_graper))
            case ("DESCENT_GO_TO_FLASK"):
                manipulate_move(manipulate, manipulate_x, manipulate_y, Z_FLASK, 0, int(step.is_graper))
            case ("CAPTURE_FLASK"):
                manipulate_move(manipulate, manipulate_x, manipulate_y, z, 0, 1)
            case ("UPPER_Z"):
                manipulate_move(manipulate, manipulate_x, manipulate_y, start_z, 0, int(step.is_graper))
            case ("GO_TO_CAMERA"):
                manipulate_move(manipulate, camera_x, camera_y, start_z, 0, 1)
            case ("DESCENT_TO_CAMERA"):
                manipulate_move(manipulate, manipulate_x, manipulate_y, camera_z, 0, 1)
            case ("REALESE_FLASK"):
                manipulate_move(manipulate, manipulate_x, manipulate_y, manipulate_z, 0, 0)
            case "GO_TO_START":
                manipulate_move(manipulate, start_x, start_y, start_z, 0, 0)

            case "ROTATE_FLASK":
                count_image = 0
                angles_rotate = list(range(-135, 225, step.angle))
                while count_image <= COUNT_IMAGES -1:
                    if manipulate.getManipulatorStatus() == 0:
                        cv2.imread(f"FRAME_{count_image+1}.png", get_image(manipulate))
                        manipulate.move(ROBOT_NAME, manipulate_x, manipulate_y, manipulate_z,
                                        angles_rotate[count_image], 1)
                        count_image += 1
                    time.sleep(0.7)

            case "RECEIVE_FLASK":
                manipulate.move(ROBOT_NAME, manipulate_x, manipulate_y, manipulate_z, -1, 1)

                number_image = 0
                while manipulate.getManipulatorStatus() != 0:
                    frame = get_image(manipulate)
                    cv2.imwrite(f'tempPhotos/frame_{number_image}.png', frame)

                    time.sleep(0.7)

                create_video()

        steps.next_step()
    time.sleep(1.0)


def load_point() -> str:
    point = input()
    return point


STEPS = {
    1: Steps(STEPS_FIRST),
    2: Steps(STEPS_SECOND),
    3: Steps(STEPS_THIRD)
}


def main(task: int, manipulate: MCX):
    point = load_point()
    coordinates = json_load("coordinates.json")

    if point not in coordinates.keys():
        raise ValueError("Input wrong key-point")
    steps = STEPS.get(task)

    while True:
        flask_move(manipulate, steps, coordinates.get('start'),
                   coordinates.get('camera'),
                   (*coordinates.get(point), 95))

        if manipulate.getManipulatorWarning() != 0:
            print(manipulate.getManipulatorWarningStr())


if __name__ == "__main__":
    my_robot = MCX()
    main(1, my_robot)
