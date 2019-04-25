import curses
#-- Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

heightStatScreen=7


MINIMUM_HEIGHT=34
MINIMUM_WIDTH=52

def createMenu(screen, menus, startX, startY):
    for menu in menus:
        menu_name = menu[0]
        menu_hotkey = menu_name[0]
        menu_no_hot = menu_name[1:]
        screen.addstr(startY, startX, menu_hotkey, hotkey_attr)
        screen.addstr(startY, startX+1, menu_no_hot, menu_attr)
        startY+=1
        # Add key handlers for this hotkey
        menu_handler(screen, (str.upper(menu_hotkey), menu[1]))
        menu_handler(screen, (str.lower(menu_hotkey), menu[1]))

    screen.refresh()

#-- Magic key handler both loads and processes keys strokes
def menu_handler(screen, key_assign=None, key_dict={}):
    if key_assign:
        key_dict[ord(key_assign[0])] = key_assign[1]
    else:
        c = screen.getch()
        if c in (curses.KEY_END, ord('!')):
            return 0
        elif c not in key_dict.keys():
            curses.beep()
            return 1
        else:
            return key_dict[c]()

def checkIfEnoughSpaceForGame(stdscr, gameScreen = None):

    maxY, maxX = stdscr.getmaxyx()

    if (maxX < MINIMUM_WIDTH or maxY < MINIMUM_HEIGHT):
        return True

    if gameScreen==None:
        return False

    return maxY <= (gameScreen.sizeY + heightStatScreen + 1) or maxX <= (gameScreen.sizeX)


class NotEnoughSpace(Exception):
    pass

class ExitTotal(Exception):
    pass

class GoBackToMainScreen(Exception):
    pass