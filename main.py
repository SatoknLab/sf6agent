import cv2
import numpy
import time
from gamepad import Gamepad
import random
import vgamepad as vg
from utils.fps import Fps

gamepad = Gamepad()

actions = {
    "none": [],
    "light": [vg.DS4_BUTTONS.DS4_BUTTON_SQUARE],
    "medium": [vg.DS4_BUTTONS.DS4_BUTTON_CROSS],
    "heavy": [vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE],
    "special": [vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE],
    "throw": [vg.DS4_BUTTONS.DS4_BUTTON_CROSS, vg.DS4_BUTTONS.DS4_BUTTON_SQUARE],
    "impact": [vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT],
    "parry": [vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT],
    "super_arts": [vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE, vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE]
}

def get_p1_hp(p1_hp, hp_bar_p1):
    for i in range(len(hp_bar_p1[0])):
        if not(31 <= hp_bar_p1[0][i][0] <= 81 and 0 <= hp_bar_p1[0][i][1] <= 12 and 93 <= hp_bar_p1[0][i][2] <= 181) and i != len(hp_bar_p1[0]) - 1:
            if 31 <= hp_bar_p1[0][i+1][0] <= 81 and 0 <= hp_bar_p1[0][i+1][1] <= 12 and 93 <= hp_bar_p1[0][i+1][2] <= 181:
                p1_hp = int((hp_bar_p1.shape[1] - i) / hp_bar_p1.shape[1] * 100)
                break

        if not(101 <= hp_bar_p1[0][i][0] <= 132 and 226 <= hp_bar_p1[0][i][1] <= 255 and 226 <= hp_bar_p1[0][i][2] <= 250) and i != len(hp_bar_p1[0]) - 1:
            if 101 <= hp_bar_p1[0][i+1][0] <= 132 and 226 <= hp_bar_p1[0][i+1][1] <= 255 and 226 <= hp_bar_p1[0][i+1][2] <= 250:
                p1_hp = int((hp_bar_p1.shape[1] - i) / hp_bar_p1.shape[1] * 100)
                break
    return p1_hp

def get_p2_hp(p2_hp, hp_bar_p2):
    for i in range(len(hp_bar_p2[0])-1, 0, -1):
        if not(116 <= hp_bar_p2[0][i][0] <= 173 and 54 <= hp_bar_p2[0][i][1] <= 104 and 31 <= hp_bar_p2[0][i][2] <= 43) and i != 0:
            if 116 <= hp_bar_p2[0][i-1][0] <= 173 and 54 <= hp_bar_p2[0][i-1][1] <= 104 and 31 <= hp_bar_p2[0][i-1][2] <= 43:
                p2_hp = int(i / hp_bar_p2.shape[1] * 100)
                break

        if not(101 <= hp_bar_p2[0][i][0] <= 132 and 226 <= hp_bar_p2[0][i][1] <= 255 and 226 <= hp_bar_p2[0][i][2] <= 250) and i != 0:
            if 101 <= hp_bar_p2[0][i-1][0] <= 132 and 226 <= hp_bar_p2[0][i-1][1] <= 255 and 226 <= hp_bar_p2[0][i-1][2] <= 250:
                p2_hp = int(i / hp_bar_p2.shape[1] * 100)
                break
    return p2_hp

def get_sa_stock(sa_stock_img):
    result = list(map(lambda x: cv2.minMaxLoc(cv2.matchTemplate(sa_stock_img, cv2.cvtColor(cv2.imread(f"{x}.png"), cv2.COLOR_BGR2GRAY), cv2.TM_CCORR_NORMED))[1], range(5)))
    sa_stock = result.index(max(result))

    return sa_stock

capture = cv2.VideoCapture(5)
fps = Fps()
screen_size = (960, 540)
p1_hp = 100
p2_hp = 100
sa_stock_p1 = 0
sa_stock_p2 = 0
ko_img = cv2.cvtColor(cv2.imread("ko2.png"), cv2.COLOR_BGR2GRAY)

gamepad.reset_training()

try:
    while capture.isOpened():
        ret, frame = capture.read()

        direction = random.randint(1,9)
        action = random.choice(list(actions.keys()))
        gamepad.send_action(direction=direction, action=action)

        current_fps = fps.calc()
        resized_img = cv2.resize(frame, screen_size)
        grey_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        small_img = cv2.resize(grey_img, (256, 144))

        hp_bar_length = 333
        hp_bar_p1 = resized_img[35:36, 423-hp_bar_length:423]
        hp_bar_p2 = resized_img[35:36, 872-hp_bar_length:872]
        sa_stock_p1_img = grey_img[480:518, 50:71]
        sa_stock_p2_img = grey_img[480:518, 890:911]

        p1_hp = get_p1_hp(p1_hp, hp_bar_p1)
        p2_hp = get_p2_hp(p2_hp, hp_bar_p2)

        sa_stock_p1 = get_sa_stock(sa_stock_p1_img)
        sa_stock_p2 = get_sa_stock(sa_stock_p2_img)

        _, max_v, _,  _ = cv2.minMaxLoc(cv2.matchTemplate(small_img, ko_img, cv2.TM_CCORR_NORMED))
        if max_v > 0.9845:
            print(f"winner: {'p1' if p1_hp > p2_hp else 'p2'}")

        cv2.putText(resized_img, f"fps:{current_fps}", (20, 100), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255,0,0))
        cv2.putText(resized_img, f"{direction}, {action}", (20, 140), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255,0,0))
        cv2.putText(resized_img, f"hp p1:{p1_hp}% p2: {p2_hp}%", (20, 180), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255,0,0))
        cv2.putText(resized_img, f"sa p1:{sa_stock_p1} p2:{sa_stock_p2}", (20, 220), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255,0,0))
        cv2.imshow("screen", resized_img)

        # save image
        # cv2.imwrite("screen.png", cv2.resize(resized_img, (256, 144))[47:97, 131:161])

        # numpy to list
        # l_hp_bar_p1 = hp_bar_p1.tolist()
        # print(l_hp_bar_p1[0])

        # Press "q" to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

    cv2.destroyAllWindows()
    capture.release()
    gamepad.pause()

except KeyboardInterrupt:
    cv2.destroyAllWindows()
    capture.release()
    gamepad.pause()