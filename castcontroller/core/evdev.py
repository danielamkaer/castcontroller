import evdev
import asyncio
import logging
logger = logging.getLogger(__name__)

KEYMAP = {
    evdev.ecodes.KEY_P: 'playpause',
    evdev.ecodes.KEY_F: 'forward',
    evdev.ecodes.KEY_B: 'back',
    evdev.ecodes.KEY_H: 'home',
    evdev.ecodes.KEY_M: 'menu',
    evdev.ecodes.KEY_R: 'return',
    evdev.ecodes.KEY_UP: 'up',
    evdev.ecodes.KEY_DOWN: 'down',
    evdev.ecodes.KEY_RIGHT: 'right',
    evdev.ecodes.KEY_LEFT: 'left',
}

class KeyboardHandler:
    def __init__(self, app):
        self.app = app
        self.device = evdev.InputDevice('/dev/input/event16')

    async def run_async(self):
        async for event in self.device.async_read_loop():
            if event.type == evdev.ecodes.EV_KEY and event.value == 0:
                if event.code in KEYMAP:
                    self.app.handle_input(KEYMAP[event.code])