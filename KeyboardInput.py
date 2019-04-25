global isWindows
isWindows = False

try:
    from win32api import STD_INPUT_HANDLE
    from win32console import GetStdHandle, KEY_EVENT, ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT
    isWindows = True
except ImportError as e:
    import sys, select, termios

class KeyPoller(object):
    def __enter__(self):
        global isWindows
        if(isWindows):
            self.readHandle = GetStdHandle(STD_INPUT_HANDLE)
            self.readHandle.SetConsoleMode(ENABLE_LINE_INPUT|ENABLE_ECHO_INPUT|ENABLE_PROCESSED_INPUT)

            self.currEventLength = 0
            self.currKeysLength = 0

            self.capturedChars = []
        else:
            #Save terminal settings
            self.fd = sys.stdin.fileno()
            self.newTerm = termios.tcgetattr(self.fd)
            self.oldTerm = termios.tcgetattr(self.fd)

            #New terminal setting unbuffered
            self.newTerm[3] = (self.newTerm[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.newTerm)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if isWindows:
            pass
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldTerm)
    def poll(self):
        if(isWindows):
            if(not len(self.capturedChars) == 0):
                return self.capturedChars.pop(0)
            eventsPeek = self.readHandle.PeekConsoleInput(10000)
            if len(eventsPeek) == 0:
                return None

            if not len(eventsPeek) == self.currEventLength:
                for curEvent in eventsPeek[self.currEventLength]:
                    if(curEvent.EventType == KEY_EVENT):
                        if(ord(curEvent.Char) == 0 or not curEvent.KeyDown):
                            pass
                        else:
                            curChar = str(curEvent.Char)
                            self.capturedChars.append(curChar)
                self.currEventLength = len(eventsPeek)
            if(not len(self.capturedChars) == 0):
                return self.capturedChars.pop(0)
            else:
                return None
        else:
            dr,dw,de = select.select([sys.stdin], [], [], 0)
            if(not dr == []):
                return sys.stdin.read(1)
            return None

if __name__ == "__main__":
    #Simle use case
    with KeyPoller() as keyPoler:
        while True:
            c = keyPoler.poll()
            if(not c is None):
                if c == "c":
                    break
                print(c)
