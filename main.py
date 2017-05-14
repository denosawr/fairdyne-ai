import pyautogui
import screengrab as sg
import time


def find_direction(x, y, cx, cy, size):
    """ Gets the direction of the arrow from the centre (cx, cy) """

    width, height = size

    max_match = (0, 0, width)
    x_dist = width // 40
    x_s = width // 2 - x_dist
    x_b = width // 2 + x_dist

    y_dist = height // 40
    y_s = height // 2 - y_dist
    y_b = height // 2 + y_dist

    direction = ""
    if y_s < y < y_b:
        if x < cx:
            direction = "left"
        else:
            direction = "right"
    elif x_s < x < x_b:
        if y < cy:
            direction = "up"
        else:
            direction = "down"

    return direction


def main(image="screenshot.png"):
    sg.screengrab(output=image)

    heart, size = [], []
    size = sg.getsize(image)

    nodir = True
    prevrun = False
    while True:
        try:
            start = time.time()
            sg.screengrab(output=image)
            arrow = sg.findarrows(image)
            if not arrow:
                continue
            if nodir and not prevrun:
                heart = sg.findheart(image)
                prevrun = True
            direction = find_direction(*arrow[:2], *heart, size)
            print(direction)
            end = time.time()
            nodir = False
            pyautogui.press(direction)
            print(end-start)
        except ZeroDivisionError:
            prevrun = False
            nodir = True


if __name__ == "__main__":
    main()
