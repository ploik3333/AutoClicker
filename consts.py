import pygame, os, threading, classes, json
from pathlib import Path
import pywinctl as pwc
from platformdirs import user_config_path

BACKGROUND = pygame.Color("#fb9e91")
FPS = 60
CONFIG_PATH = user_config_path("ObjectivlyTheBestAutoclickerEverIfIDoSaySoMyself",
                               ensure_exists=True) / 'autoclicker.json'
print(CONFIG_PATH)

(_WINDOW_WIDTH, _WINDOW_HEIGHT) = (350, 300)
XBOUNDS = (200, float('inf'))
YBOUNDS = (175, float('inf'))
_WINDOW = pygame.display.set_mode((_WINDOW_WIDTH, _WINDOW_HEIGHT), pygame.RESIZABLE)
running = classes.Pointer(True)


def ESTOP(*args):
    print("exiting")
    running.value = False
    os._exit(1)


play_hook = classes.Hook()
estop_hook = classes.Hook(callback=ESTOP)

CLICK_EVENT = threading.Event()
IS_ON_TOP = classes.Pointer(False)
space = classes.Pointer(0)

# Needed for saving, so passed in later
spaceLabel = classes.Pointer(None)
onTopToggle = classes.Pointer(None)


# Functions that rely on above globals and constants
def get_window():
    return _WINDOW

constrain = lambda v, l, u: min(max(v, l), u)
def set_size(v):
    global WINDOW_HEIGHT, WINDOW_WIDTH, _WINDOW
    new_x = constrain(v[0], *XBOUNDS)
    new_y = constrain(v[1], *YBOUNDS)
    if (new_x, new_y) != get_size():
        (_WINDOW_WIDTH, _WINDOW_HEIGHT) = (new_x, new_y)
        _WINDOW = pygame.display.set_mode((_WINDOW_WIDTH, _WINDOW_HEIGHT), pygame.RESIZABLE)
        setOnTop(IS_ON_TOP.value)


def get_size():
    return (_WINDOW_WIDTH, _WINDOW_HEIGHT)


def w():
    return _WINDOW_WIDTH


def h():
    return _WINDOW_HEIGHT


def get_all_hooks():  # MUST NOT CHANGE MID PROGRAM
    return play_hook, estop_hook


def get_hooks_enabled_state():
    return [*map(lambda v: v.enabled, get_all_hooks())]


def set_hooks_enabled_state(values: list[bool]):
    for v, e in zip(get_all_hooks(), values):
        v.set_enabled(values[e])


def load_state():
    global play_hook, estop_hook
    config = Path(CONFIG_PATH)
    if config.exists():
        with open(CONFIG_PATH, "r") as fin:
            loaded_state = json.load(fin)
        play_key = loaded_state.get("play_key", None)
        if play_key:
            play_hook.set(play_key)
            if play_hook.text_area:
                play_hook.text_area.set_text(play_key)
        estop_key = loaded_state.get("estop_key", None)
        if estop_key:
            estop_hook.set(estop_key)
            if estop_hook.text_area:
                estop_hook.text_area.set_text(estop_key)

        space.value = loaded_state.get("click_time", 0)
        if spaceLabel.value:
            spaceLabel.value.set_text(str(space.value))

        IS_ON_TOP.value = loaded_state.get("ONTOP", False)
        if onTopToggle.value:
            onTopToggle.value.set_state(IS_ON_TOP.value)


def save_state():
    config = Path(CONFIG_PATH)
    if config.exists():
        with open(CONFIG_PATH, "r") as fin:
            loaded_state = json.load(fin)
    else:
        loaded_state = {}

    _play_hook, _estop_hook = get_all_hooks()

    loaded_state.update({"click_time": space.value})
    loaded_state.update({"ONTOP": IS_ON_TOP.value})
    if len(_play_hook.key) > 0:
        loaded_state.update({"play_key": _play_hook.key})
    if len(_estop_hook.key) > 0:
        loaded_state.update({"estop_key": _estop_hook.key})

    with open(CONFIG_PATH, "w") as fout:
        json.dump(loaded_state, fout)


def setOnTop(isOnTop):
    winInfo = pygame.display.get_wm_info()
    wndOrPointerORsomething_weird_depending_on_the_os = winInfo.get("window")
    if wndOrPointerORsomething_weird_depending_on_the_os:
        window = pwc.Window(wndOrPointerORsomething_weird_depending_on_the_os)
        if window:
            window.alwaysOnTop(isOnTop)
