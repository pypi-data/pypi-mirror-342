import sys
import time
import asyncio
import threading

import pywinauto


class COORDS:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y


class RECT():
    def __init__(self, left: int, top: int, right: int = None, bottom: int = None, width: int = None, height: int = None):
        self.left: int = left
        self.top: int = top

        if right is not None:
            self.right: int = right

        elif width is not None:
            self.right: int = self.left + width

        else:
            raise "Error, set at least right or width"

        if bottom is not None:
            self.bottom: int = bottom

        elif width is not None:
            self.bottom: int = self.top + height

        else:
            raise "Error, set at least bottom or width"

        self._width: int = width if width is not None else self.width()
        self._height: int = height if height is not None else self.height()
        self._middle: COORDS = self.mid_point()

    def width(self):
        return abs(self.right-self.left)

    def height(self):
        return abs(self.bottom-self.top)

    def mid_point(self):
        x: int = self.left + int(float(self._width) / 2.)
        y: int = self.top + int(float(self._height) / 2.)
        return COORDS(x, y)


class WinController:
    def __init__(self, main_process: str, process_name: str, input_per_sec: int = 1):
        self.main_process: str = main_process
        self.process_name: str = process_name

        self.input_per_sec: int = input_per_sec
        self._refresh: float = 1 / self.input_per_sec

        self._run: bool = False
        self._focus: bool = True

        self.test: str = "no"

        try:
            self.app = pywinauto.Application().connect(path=self.main_process)
            self.main_win = self.app[self.process_name]
        except Exception as e:
            sys.exit(e)

        self.actions: dict = {}
        self.last_buttons: list = [[], []]

        self.update_window()
        self.focus()

    def update_window(self):
        rect = self.main_win.rectangle()

        self.left, self.top, self.bottom, self.right, self.width, self.height, self.middle = rect.left, rect.top, rect.bottom, rect.right, rect.width(), rect.height(), rect.mid_point()
        self.windows = [self.left, self.top, self.width, self.height]
        self.rect = RECT(left=self.left, top=self.top, right=self.right, bottom=self.bottom, width=self.width, height=self.height)

    def to_image(self):
        return self.main_win.capture_as_image(self.main_win.rectangle())

    def stop(self):
        self._run: bool = False
        self.release_all()

    def focus(self):
        if self._focus:
            self.main_win.set_focus()

    def type_keys(self, keys: str, pause=None, with_spaces: bool = False, with_tabs: bool = False, with_newlines: bool = False, turn_off_numlock: bool = True, set_foreground: bool = True, vk_packet: bool = True):
        self.focus()
        self.main_win.type_keys(keys=keys, pause=pause, with_spaces=with_spaces, with_tabs=with_tabs, with_newlines=with_newlines, turn_off_numlock=turn_off_numlock, set_foreground=set_foreground, vk_packet=vk_packet)

    def press(self, button: str = None, action: str = None):
        if action is not None:
            button: str = self.get_button(action)

        if button == button.upper() or len(button) == 1:
            self.type_keys("{" + f"{button} down" + "}")

        else:
            self.type_keys(button)

    def release(self, button: str = None, action: str = None):
        if action is not None:
            button: str = self.get_button(action)

        if button == button.upper() or len(button) == 1:
            self.type_keys("{" + f"{button} up" + "}")

    def release_all(self):
        for v in self.actions.values():
            if "CLICK" in v:
                self.release_cursor(v.split("_")[-1].lower())
                continue

            self.release(v)

    def get_button(self, action: str):
        return self.actions.get(action.upper(), None)

    def move_cursor(self, x: int, y: int, key_pressed: str = ""):
        self.focus()
        self.main_win.move_mouse_input(coords=(x, y), pressed=key_pressed, absolute=False)

    def drag_cursor(self, x: int, y: int, button: str = "left", key_pressed: str = ""):
        self.focus()
        self.main_win.drag_mouse_input(dst=(x, y), button=button, pressed=key_pressed, absolute=False)

    def click(self, button: str = "left", double: bool = False, coords: tuple = (None, None)):
        self.focus()
        self.main_win.click_input(button=button, double=double, coords=coords)

    def press_cursor(self, button: str = "left", coords: tuple = (None, None), key_pressed: str = ""):
        self.focus()
        self.main_win.press_mouse_input(button=button, coords=coords, pressed=key_pressed, absolute=False)

    def release_cursor(self, button: str = "left", coords: tuple = (None, None), key_pressed: str = ""):
        self.focus()
        self.main_win.release_mouse_input(button=button, coords=coords, pressed=key_pressed, absolute=False)

    def do(self, actions: list = [], buttons: list = [], coords: tuple = (None, None)):
        self.last_buttons[1]: list = self.last_buttons[0]
        undo: list = []

        if actions == [] and buttons == []:
            return

        elif buttons != []:
            pass

        elif isinstance(actions, list):
            for action in actions:
                buttons.append(self.get_button(action))

        elif isinstance(actions, str):
            buttons.append(self.get_button(actions))
            actions: list = [actions]

        for button in self.last_buttons[1]:
            if button not in buttons:
                undo.append(button)

        self.undo(buttons=undo)

        self.last_buttons[0]: list = buttons.copy()

        for button in buttons:
            if button is None:
                continue

            if button in self.last_buttons[1]:
                continue

            if "CLICK" in button:
                button: str = button.split("_")[-1].lower()
                self.click(button=button, coords=coords)
                continue

            self.press(button)

        actions.clear()
        buttons.clear()

    def undo(self, actions: list = [], buttons: list = [], coords: tuple = (None, None)):
        if actions == [] and buttons == []:
            return

        elif buttons != []:
            pass

        elif isinstance(actions, list):
            for action in actions:
                buttons.append(self.get_button(action))

        elif isinstance(actions, str):
            buttons.append(self.get_button(actions))
            actions: list = [actions]

        for button in buttons:
            if button is None:
                continue

            if "CLICK" in button:
                button: str = button.split("_")[-1].lower()
                self.release_cursor(button=button, coords=coords)
                continue

            self.release(button)

            if button in self.last_buttons[1]:
                self.last_buttons[1].remove(button)

        actions.clear()
        buttons.clear()

    async def _run_async(self):
        await asyncio.sleep(.01)

        while self._run:
            await self._to_call()
            await asyncio.sleep(self._refresh)

    def _run_sync(self):
        time.sleep(.01)

        while self._run:
            self._to_call()
            time.sleep(self._refresh)

    def _check_run(self, run_async: bool = True):
        if not self._run:
            self._run: bool = True

            if run_async:
                self.start_async_thread(self._run_async())

            else:
                threading.Thread(target=self._run_sync).start()
                
    # https://gist.github.com/ultrafunkamsterdam/8be3d55ac45759aa1bd843ab64ce876d#file-python-3-6-asyncio-multiple-async-event-loops-in-multiple-threads-running-and-shutting-down-gracefully-py-L15
    def create_bg_loop(self):
        def to_bg(loop):
            asyncio.set_event_loop(loop)

            try:
                loop.run_forever()

            except asyncio.CancelledError as e:
                print('CANCELLEDERROR {}'.format(e))

            finally:
                for task in asyncio.Task.all_tasks():
                    task.cancel()

                loop.run_until_complete(loop.shutdown_asyncgens())
                loop.stop()
                loop.close()

        new_loop = asyncio.new_event_loop()
        t = threading.Thread(target=to_bg, args=(new_loop,))
        t.start()
        return new_loop


    def start_async_thread(self, awaitable):
        # old
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        threading.Thread(target=loop.run_forever).start()
        """
        # new
        loop = self.create_bg_loop()

        coro = asyncio.run_coroutine_threadsafe(awaitable, loop)
        return loop, coro

    def stop_async_thread(self, loop):
        loop.call_soon_threadsafe(loop.stop)

    def on_update(self, callback: callable = None):
        def add_debug(func):
            self._check_run(asyncio.iscoroutinefunction(func))
            self._to_call: callable = func
            return func

        if callable(callback):
            return add_debug(callback)

        return add_debug
