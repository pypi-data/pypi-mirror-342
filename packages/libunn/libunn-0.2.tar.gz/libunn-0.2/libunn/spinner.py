# Part of libunn, view: https://github.com/juanvel4000/libunn
import threading, time, sys

running = False

def _spinner(message=None):
    global running
    spinner = ['/', '-', '\\', '|']
    while running:
        for char in spinner:
            if message is not None:
                sys.stdout.write(f'\r{char} {message}')
            else:
                sys.stdout.write(f'\r{char}')
            sys.stdout.flush()
            time.sleep(0.2)
def start(message=None):
    global running
    if not running:
        running = True
        spnthr = threading.Thread(target=_spinner, args=(message,))
        spnthr.daemon = True
        spnthr.start()
def stop():
    global running
    running = False
    time.sleep(0.2)
    sys.stdout.write('\n')