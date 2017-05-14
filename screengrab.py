from mss import mss
from PIL import Image

import time


def screengrab(monitor=0, output="screenshot.png"):
    """ Uses MSS to capture a screenshot quickly. """

    sct = mss()
    monitors = sct.enum_display_monitors()
    game_x = 600
    game_y = 600
    mon_x = monitors[monitor]["left"]
    mon_y = monitors[monitor]["top"]
    size_x = monitors[monitor]["width"]
    size_y = monitors[monitor]["height"]
    x = int(mon_x + (size_x - game_x)/2)
    y = int(mon_y + 140 + (game_x//2))
    mon = {'top': y, 'left': x, 'width': game_x, 'height': game_y}
    sct.to_png(data=sct.get_pixels(mon), output=output)


def findheart(image="screenshot.png"):
    """ Finds the heart. """

    image_data = Image.open(image)
    width = image_data.size[0]
    heart = list()
    for count, i in enumerate(image_data.getdata()):
        if i == (0, 0, 0):
            continue
        elif i == (0, 255, 0):
            x = count % width
            y = int(count/width)
            heart.append([x, y])

    if not heart:
        return
    sh = len(heart)
    cx = int(sum([x[0] for x in heart])/sh)
    cy = int(sum([y[1] for y in heart])/sh)

    return cx, cy


def getsize(image="screenshot.png"):
    """ Returns the size of the image. """

    image_data = Image.open(image)
    return image_data.size[0], image_data.size[1]


def findarrows(image="screenshot.png"):
    """ Finds arrows in the specified image, by finding the closest pixel of a certain color. """

    try:
        image_data = Image.open(image)
        width = image_data.size[0]
        height = image_data.size[1]
        matches = list()
        heart = list()
        for count, i in enumerate(image_data.getdata()):
            if i == (0, 0, 0):
                continue
            elif i == (47, 208, 255):
                count += 1
                x = count % width
                y = int(count/width)
                matches.append([x, y])
            elif i == (0, 255, 0):
                x = count % width
                y = int(count/width)
                heart.append([x, y])

        sh = len(heart)
        cx = int(sum([x[0] for x in heart])/sh)
        cy = int(sum([y[1] for y in heart])/sh)

        max_match = (0, 0, width)
        x_dist = width//40
        x_s = width//2 - x_dist
        x_b = width//2 + x_dist

        y_dist = height//40
        y_s = height//2 - y_dist
        y_b = height//2 + y_dist
        for i in matches:
            if y_s < i[1] < y_b:
                if (abs(cx-i[0])) < max_match[2]:
                    max_match = (i[0], i[1], abs(cx-i[0]))
            elif x_s < i[0] < x_b:
                if (abs(cy-i[1])) < max_match[2]:
                    max_match = (i[0], i[1], abs(cy-i[1]))
        return max_match
    except ZeroDivisionError:
        return None


if __name__ == "__main__":
    print(findarrows(image="screenshot.png"))
