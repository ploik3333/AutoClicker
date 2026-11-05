from typing import Callable

from pygame_gui.elements import UIWindow, UITextBox
from pygame import Rect
import keyboard, pygame_gui
import consts


class GetKeyWindow(UIWindow):
    def __init__(self, *args, callback=lambda e: None, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

        # global hook to get a key
        self._hook = None
        self.prior_hook_states = None

        # name of the key selected currently
        self.keypress = ""

        self.choose_key_popup_text = UITextBox("...", Rect(0, 0, self.relative_rect.width - 2,
                                                           self.relative_rect.height - 30), placeholder_text="...",
                                               container=self)
        self.set_blocking(True)

    def on_close_window_button_pressed(self):
        self.hide()

    def hide(self, hide_contents: bool = True):
        if self._hook is not None:
            keyboard.unhook(self._hook)
            self._hook = None

        consts.set_hooks_enabled_state(self.prior_hook_states)

        super().hide(hide_contents)

        if len(self.keypress) > 0:
            self.callback(self.keypress)

    def set_hook_result(self, e: keyboard.KeyboardEvent):
        if e.event_type == keyboard.KEY_DOWN:
            self.set_text(str(e.name))
            self.keypress = e.name

    def show(self, show_contents: bool = True):
        if self._hook is None:
            self._hook = keyboard.hook(callback=self.set_hook_result)

        consts.CLICK_EVENT.clear()

        self.prior_hook_states = consts.get_hooks_enabled_state()
        for h in consts.get_all_hooks():
            h.disable()
        super().show(show_contents)

    def set_text(self, string: str):
        self.choose_key_popup_text.set_text(string)

    def process_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame_gui.UI_WINDOW_RESIZED:
            if event.ui_element == self:
                self.choose_key_popup_text.set_dimensions(event.internal_size)

        return super().process_event(event)

    def __str__(self) -> str:
        return f"GetKeyWindow({repr(self.keypress)}, {self._hook})"


class Hook:
    def __init__(self, key="", callback=None):
        self.callback: Callable = callback
        self.key = ""

        self.set(key)

        self._hook = None
        self.enabled = False
        self.text_area = None

    def set(self, new_key):
        if new_key == self.key or new_key == "":
            return
        if self._hook:
            keyboard.unhook(self._hook)
        self.key = new_key
        if self.text_area:
            self.text_area.set_text(new_key)
        self._hook = keyboard.hook_key(self.key, self._callback)
        self.enable()

    def set_text_area(self, ta):
        self.text_area = ta

    def _callback(self, event: keyboard.KeyboardEvent):
        if event.event_type == keyboard.KEY_DOWN:
            if self.enabled and self.callback is not None:
                self.callback(event)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def set_enabled(self, v):
        self.enabled = v

    @property
    def value(self):
        raise Exception("NO :(")

class Pointer:
    def __init__(self, value = None):
        self.value = value