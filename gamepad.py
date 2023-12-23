import vgamepad as vg
import time

class Gamepad():
    gamepad = None

    directions = {
        1: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHWEST,
        2: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH,
        3: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHEAST,
        4: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST,
        5: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE,
        6: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST,
        7: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST,
        8: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH,
        9: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHEAST,
    }

    actions = {
        "none": [],
        "light": [vg.DS4_BUTTONS.DS4_BUTTON_SQUARE],
        "medium": [vg.DS4_BUTTONS.DS4_BUTTON_CROSS],
        "heavy": [vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE],
        "special": [vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE],
        "assist_light": [vg.DS4_BUTTONS.DS4_BUTTON_SQUARE, vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT],
        "assist_medium": [vg.DS4_BUTTONS.DS4_BUTTON_CROSS, vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT],
        "assist_heavy": [vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE, vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT],
        "overdrive": [vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE, vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT],
        "super_arts": [vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE, vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE],
        "throw": [vg.DS4_BUTTONS.DS4_BUTTON_CROSS, vg.DS4_BUTTONS.DS4_BUTTON_SQUARE],
        "impact": [vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT],
        "parry": [vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT]
    }

    def __init__(self) -> None:
        self.gamepad = vg.VDS4Gamepad()

    def play_action(self, buttons):
        for button in buttons:
            self.gamepad.press_button(button=button)

    def send_action(self, direction, action):
        self.gamepad.reset()
        self.gamepad.directional_pad(direction=self.directions[direction])
        self.play_action(buttons=self.actions[action])
        self.gamepad.update()

    def reset_training(self):
        self.gamepad.reset()
        self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHARE)
        self.gamepad.update()
        time.sleep(1)

    def pause(self):
        self.gamepad.reset()
        self.gamepad.update()
        time.sleep(0.5)
        self.gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS)
        self.gamepad.update()
        time.sleep(0.5)