import pyautogui, time, os, logging, sys, random, copy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')

def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    return os.path.join('images', filename)


def getGameRegion():
    """Obtains the region that the game is on the screen and assigns it to GAME_REGION"""
    global GAME_REGION

    # identify the top-left corner
    logging.debug('Finding game region...')
    region = pyautogui.locateOnScreen(imPath('CheckStart.png'))
    if region is None:
        raise Exception('Could not find game on screen. Is the game visible?')

    # calculate the region of the entire game
    topRightX = region[0] + region[2] # left + width
    topRightY = region[1] # top
    GAME_REGION = (topRightX - 478, topRightY, 478, 101)
    logging.debug('Game region found: %s' % (GAME_REGION,))

def setupCoordinates():
    global BET1, BET2, START, DOUBLE, HALVE, CASHOUT
    BET1 = (GAME_REGION[0] + 710, GAME_REGION[1] - 40)
    BET2 = (GAME_REGION[0] + 800, GAME_REGION[1] - 40)
    START = (GAME_REGION[0] + 235, GAME_REGION[1] + 130)
    CASHOUT = (GAME_REGION[0] + 235, GAME_REGION[1] + 130)
    DOUBLE = (GAME_REGION[0] + 365, GAME_REGION[1] - 40)
    HALVE = (GAME_REGION[0] + 310, GAME_REGION[1] - 40)

def startBet():
    if pyautogui.locateOnScreen(imPath('StartGame.png'), region=(GAME_REGION[0], GAME_REGION[1] + 80, 500, 100)) is not None:
        print("StartGame")
        pyautogui.click(START, duration=0.25)
        time.sleep(1)

def resetBet():
    while pyautogui.locateOnScreen(imPath('BaseStart.png'), region=(GAME_REGION[0], GAME_REGION[1] - 100, 300, 110)) is None:
        print("Resetting")
        pyautogui.click(HALVE, clicks=5, interval=0.25)
        time.sleep(1)
    pyautogui.click(DOUBLE, clicks=3, duration=0.1)

def clickStars():
    curPos = pyautogui.position()
    if curPos[0] < 200:
        return None
    startBet()
    time.sleep(1)
    while pyautogui.locateOnScreen(imPath('DoubleWinStar.png'), region=(GAME_REGION[0] + 600, GAME_REGION[1] - 100, 250, 150)) is None and \
            pyautogui.locateOnScreen(imPath('Bomb.png'), region=(GAME_REGION[0] + 600, GAME_REGION[1] - 100, 250, 150)) is None:
        pyautogui.click(BET1, duration=0.1)
        time.sleep(1)
        pyautogui.click(BET2, duration=0.1)
        time.sleep(2)
        curPos = pyautogui.position()
        if curPos[0] < 200:
            return None
    if pyautogui.locateOnScreen(imPath('DoubleWinStar.png'), region=(GAME_REGION[0] + 600, GAME_REGION[1] - 100, 250, 150)) is not None:
        pyautogui.click(CASHOUT, duration=0.1)
        resetBet()
        clickStars()
    else:
        pyautogui.click(DOUBLE, duration=0.1)
        clickStars()

def main():
    """Runs the entire program. Roobet must be on the screen"""
    logging.debug('Program Started. Press Ctrl-C to abort at any time.')
    logging.debug('To interrupt mouse movement, move mouse to upper left corner.')
    getGameRegion()
    setupCoordinates()
    resetBet()
    clickStars()

main()
