import time
import pyautogui
import keyboard
from mss import mss
from PIL import Image

IMG_DIR = "imgCache/"

PERCENTAGE = None


def getResKeepResolution(width, height, targetWidth):
    global PERCENTAGE
    PERCENTAGE = 100 / width * targetWidth
    pheight = height / 100 * PERCENTAGE

    return (targetWidth, int(pheight))


def getScreenshot():
    return mss().shot(output=IMG_DIR + "screenshot.png")


def resize(file, rate):
    img = Image.open(file)

    resValues = getResKeepResolution(img.size[0], img.size[1], rate)
    resized = img.resize(resValues, Image.Resampling.BILINEAR)

    resDirectory = IMG_DIR + "resized.png"

    resized.save(resDirectory)
    return resDirectory


def scaleUpCoord(x, y):
    pX = x / PERCENTAGE * 100
    pY = y / PERCENTAGE * 100

    return (pX, pY)


def isNotUpgraded(colors):
    # red
    if (colors[1] < 15 and colors[2] < 15):
        if (colors[0] > 100 and colors[0] < 130):
            return True

    # purple / dark blue
    if (colors[0] < 50 and colors[1] < 30):
        if (colors[2] > 100 and colors[2] < 130):
            return True

    # light blue
    if (colors[0] < 10):
        if (colors[1] > 100 and colors[1] < 130):
            if (colors[2] > 100 and colors[1] < 130):
                return True

    # yellow
    if (colors[2] < 20):
        if (colors[0] > 100 and colors[0] < 130):
            if (colors[1] > 90 and colors[1] < 100):
                return True

    return False


def getNotUpgradedPixels(file):
    img = Image.open(file)

    imgList = []

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if isNotUpgraded(img.getpixel((x, y))):
                print(img.getpixel((x, y)))
                imgList.append((x, y))

    return imgList


def init():
    for x in range(100):
        keyboard.wait("shift+space")

        colorsExist = True

        while colorsExist:
            image = getScreenshot()
            resized = resize(image, 500)

            pixels = getNotUpgradedPixels(resized)

            if (len(pixels)) > 0:
                colorsExist = True
                coord = pixels[0]

                scaled = scaleUpCoord(coord[0], coord[1])
                pyautogui.moveTo(1080 + scaled[0], scaled[1])
                pyautogui.mouseDown()
                time.sleep(0.5)
                pyautogui.mouseUp()
                time.sleep(1)

                pyautogui.mouseDown()
                time.sleep(5)
                pyautogui.mouseUp()


if __name__ == "__main__":
    init()
