import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import castcontroller.core

STREAMS = [
    'http://live-icy.gss.dr.dk/A/A05H.mp3',
    'http://live-icy.gss.dr.dk/A/A10H.mp3',
    'http://live-icy.gss.dr.dk/A/A21H.mp3'
]


class Application:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.kb = castcontroller.core.KeyboardHandler(self)
        self.cast = castcontroller.core.ChromecastHandler(self)
        self.currentStream = 0

    def run(self):
        asyncio.ensure_future(self.kb.run_async(), loop=self.loop)
        asyncio.ensure_future(self.cast.run_async(), loop=self.loop)

        self.loop.run_forever()
    
    def handle_input(self, message):
        if message == 'playpause':
            stat = self.cast.determine_status()
            if stat == 'active':
                dev = self.cast.find_active_chromecast()
                dev.playpause()

            elif stat == 'inactive':
                dev = self.cast.find_primary_device()
                dev.play_audio(STREAMS[self.currentStream])

        elif message == 'home':
            stat = self.cast.determine_status()
            if stat == 'active':
                dev = self.cast.find_active_chromecast()
                dev.cast.quit_app()

        elif message == 'forward':
            self.currentStream += 1
            if self.currentStream > len(STREAMS) - 1: self.currentStream = 0

            stat = self.cast.determine_status()

            if stat == 'active':
                dev = self.cast.find_active_chromecast()
                dev.play_audio(STREAMS[self.currentStream])

        elif message == 'back':
            self.currentStream -= 1
            if self.currentStream < 0: self.currentStream = len(STREAMS) - 1

            stat = self.cast.determine_status()

            if stat == 'active':
                dev = self.cast.find_active_chromecast()
                dev.play_audio(STREAMS[self.currentStream])

