import atexit, mouse, time, sys
from pygame_gui.elements import UIButton, UICheckBox, UITextEntryLine
from consts import *
from pygame.locals import *
from classes import *
import logging
from resources import THEMEPATH, APPICON

logging.basicConfig(level=logging.DEBUG)

pygame.init()

fpsClock = pygame.time.Clock()
pygame.display.set_caption('Auto Clicker by L :3')
pygame.display.set_icon(APPICON)
manager = pygame_gui.UIManager(get_size(), THEMEPATH)
atexit.register(keyboard.unhook_all)


# Sets up thread to click when main thread says it's ok
def click():
    while True:
        CLICK_EVENT.wait()
        mouse.click('left')
        if space.value > 0.1:
            time.sleep(space.value)
        elif space.value == 0:
            pass
        else:
            target = time.perf_counter_ns() + space.value * 1e9 - 2e4
            while time.perf_counter_ns() < target:
                pass


click_thread = Pointer(threading.Thread(target=click, daemon=True))
click_thread.value.start()


def on_start_hook(e: keyboard.KeyboardEvent):
    if (e.event_type == keyboard.KEY_DOWN):
        if not CLICK_EVENT.is_set():
            print("running")
            CLICK_EVENT.set()
        else:
            print("stopping")
            CLICK_EVENT.clear()


play_hook.callback = on_start_hook


def modify_global_hook(newKey: str):
    if newKey == estop_hook.key:  # cant be the same
        return
    play_hook.set(newKey)


def modify_estop_hook(newKey: str):
    if newKey == play_hook.key:
        return
    estop_hook.set(newKey)


# each has a button, a window, and a text box that gets modified by the callback
b = UIButton((25, 25, 150, 50), "Change ESTOP key")
get_estop = GetKeyWindow(Rect(100, 100, 250, 100), window_display_title="Choose an Emergency Stop Key", resizable=True,
                         draggable=True, visible=False, callback=modify_estop_hook)
estop_hook.set_text_area(UITextBox("", Rect(200, 25, 100, 50), manager))

b2 = UIButton(Rect(25, 100, 150, 50), "Change PLAY key")
get_play = GetKeyWindow(Rect(100, 100, 300, 100), window_display_title="Choose a key to start/stop the macro",
                        resizable=True, draggable=True, visible=False, callback=modify_global_hook)
play_hook.set_text_area(UITextBox("", Rect(200, 100, 100, 50), manager))

check_box = UICheckBox(Rect(25, 175, 25, 25), "Always on top window?", manager, initial_state=IS_ON_TOP.value)
onTopToggle.value = check_box

speed_label = UITextBox("Time Between Clicks (s): ", Rect(25, 250, 185, 35), object_id="#NoBorder")
speed_box = UITextEntryLine(Rect(200, 250, 100, 35), initial_text=str(space.value))
spaceLabel.value = speed_box


def main():
    # main "game" loop
    while running.value:
        delta_time = fpsClock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            manager.process_events(event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                set_size(event.size)
                manager.set_window_resolution(event.size)
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == b:
                    if get_estop.visible:
                        get_estop.hide()
                    else:
                        get_estop.show()
                if event.ui_element == b2:
                    if get_play.visible:
                        get_play.hide()
                    else:
                        get_play.show()
            elif event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == speed_box:
                    print(event)
                    try:
                        space.value = float(event.text)
                        print(f"valid: {space.value}")
                    except ValueError:
                        print(f"invalid: {space.value}")
            elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
                if event.ui_element == check_box:
                    IS_ON_TOP.value = True
                    setOnTop(True)
            elif event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                if event.ui_element == check_box:
                    IS_ON_TOP.value = False
                    setOnTop(False)

        manager.update(delta_time / 1000.0)
        manager.draw_ui(get_window())
        pygame.display.update()
        get_window().fill(BACKGROUND)


load_state()
atexit.register(save_state)
if __name__ == '__main__':
    main()
    pygame.quit()
