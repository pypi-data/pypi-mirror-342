# PyWinController

## Overview
PyWinController is a Python module that provides an interface for interacting with Windows applications using `pywinauto`. It enables window manipulation, keyboard inputs, and mouse interactions.

## Requirements
- Python 3.x
- `pywinauto` library

## Installation
```sh
pip install pywincontroller
```

## Classes

### `COORDS`
Represents a coordinate with `x` and `y` values.
#### Attributes:
- `x` (int): X-coordinate.
- `y` (int): Y-coordinate.

### `RECT`
Represents a rectangular area in a window.
#### Attributes:
- `left`, `top`, `right`, `bottom` (int): Define the position and boundaries.
- `width`, `height` (int): Computed if not explicitly set.
- `middle` (COORDS): Midpoint of the rectangle.
#### Methods:
- `width()`: Returns the rectangle's width.
- `height()`: Returns the rectangle's height.
- `mid_point()`: Computes the midpoint coordinates.

### `WinController`
Controls a Windows application window.
#### Attributes:
- `main_process` (str): Path of the main executable.
- `process_name` (str): Name of the window process.
- `input_per_sec` (int): Amount of inputs per second / refresh rate between 2 actions.
- `actions` (dict): Mapping of action names to key bindings.

#### Methods:
- `update_window()`: Updates window dimensions.
- `to_image()`: Captures a screenshot.
- `stop()`: Stops interactions and the frame update.
- `focus()`: Sets focus to the application window.
- `type_keys(keys, ...)`: Simulates keyboard input.
- `press(button, action)`: Simulates key press.
- `release(button, action)`: Releases a key.
- `release_all()`: Releases all pressed keys.
- `move_cursor(x, y, key_pressed)`: Moves the cursor.
- `drag_cursor(x, y, button, key_pressed)`: Drags the cursor.
- `click(button, double)`: Clicks the mouse button.
- `press_cursor(button, coords, key_pressed)`: Presses a mouse button at given coordinates.
- `release_cursor(button, coords, key_pressed)`: Releases a mouse button at given coordinates.
- `do(actions, buttons)`: Performs a series of actions.
- `undo(actions, buttons)`: Reverts performed actions.

#### Callback / Decorator :
- `on_update(callback)`: Registers an update callback function.


## Usage Example
```python
from pywincontroller import WinController, RECT


class MarioBros(WinController):
    def __init__(self, input_per_sec: int = 3):
        WinController.__init__(self, main_process="Mesen", process_name="Mesen - Super Mario Bros. (Europe) (Rev A)", input_per_sec=input_per_sec)

        self.actions: dict = {
            "JUMP": "k",
            "FIRE": "j",

            "START": "i",
            "SELECT": "u",

            "UP": "z",
            "DOWN": "s",
            "LEFT": "q",
            "RIGHT": "d",
        }

    def to_image(self):
        top_crop: int = 120
        return self.main_win.capture_as_image(RECT(left=self.left+10, top=self.top+top_crop, width=self.width-30, height=self.height-top_crop-20))

    def get_timer(self):
        return self.main_win.capture_as_image(RECT(left=self.left+422, top=self.top+101, width=50, height=18))

    def get_score(self):
        return self.main_win.capture_as_image(RECT(left=self.left+52, top=self.top+101, width=102, height=18))

    def get_coins(self):
        return self.main_win.capture_as_image(RECT(left=self.left+212, top=self.top+101, width=38, height=18))



mb = MarioBros(input_per_sec=3)
mb.focus()
iter = 0


@mb.on_update()
async def main():
    global iter

    if iter % 5:
        # to do an action
        mb.do(["JUMP"])

    else:
        # to do nothing
        mb.do("")

    iter += 1

    if iter >= 100:
        mb.stop()

    print(iter)
```
