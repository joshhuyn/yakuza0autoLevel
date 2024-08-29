import keyboard
from time import sleep
from threading import Thread


START_KEY = "space"
STOP_KEY = "ctrl+c"


CFG_PATH = "./config/legendStyle.cfg"

UPGRADE_TIME = 7
DELAY_BETWEEN_MOVEMENT = 0.5


CANCELATION_PENDING = False


def readConfig():
    fileContent = []

    file = open(CFG_PATH, 'r')

    for line in file:
        if line.startswith("#"):
            continue

        if len(line) == 0 or line == "\n":
            continue

        fileContent.append(line.replace("\n", ""))

    file.close()

    return fileContent


def runMacros(cfgList):
    global CANCELATION_PENDING

    for x in cfgList:
        if CANCELATION_PENDING:
            return

        cfg = x.split(",")

        print("pressing " + cfg[0] + " with " + cfg[1] + " test " + str(cfg[1] != "u"))
        keyboard.press(cfg[0])
        sleep(0.1)
        keyboard.release(cfg[0])

        sleep(DELAY_BETWEEN_MOVEMENT)

        continue

        if cfg[1] != "u":
            continue

        keyboard.press("e")
        sleep(UPGRADE_TIME)
        keyboard.release("e")


def startMacroLoop(cfgList):
    global CANCELATION_PENDING

    while not CANCELATION_PENDING:
        runMacros(cfgList)


def cancelCallback():
    global CANCELATION_PENDING

    print("Cancellation triggered")
    CANCELATION_PENDING = True


def init():
    global CANCELATION_PENDING
    keyboard.add_hotkey(STOP_KEY, cancelCallback)

    while True:
        CANCELATION_PENDING = False
        keyboard.wait(START_KEY)
        fileContent = readConfig()

        macroThread = Thread(target=startMacroLoop, args=(fileContent, ))
        macroThread.start()


if __name__ == "__main__":
    init()
