import pychromecast
import logging
logger = logging.getLogger(__name__)

class Chromecast:
    def __init__(self, cast):
        self.cast = cast
        self.cast.register_status_listener(self)
        self.cast.socket_client.start()

    def new_cast_status(self, status):
        print(f"new cast status: {status}")
        self.status = status

    def is_active(self):
        if self.cast.status.is_stand_by != None:
            return not self.cast.status.is_stand_by
        else:
            return self.cast.status.app_id != None

    def playpause(self):
        if self.cast.media_controller.status.player_state == 'PLAYING':
            self.cast.media_controller.pause()
        else:
            self.cast.media_controller.play()

    def play_audio(self, url):
        self.cast.play_media(url, 'audio/mp3')

class ChromecastHandler:

    def __init__(self, app):
        self.app = app
        self.casts = []

    async def run_async(self):
        pychromecast.get_chromecasts(blocking=False, callback=self.found_chromecast)

    def found_chromecast(self, cast):
        self.casts.append(Chromecast(cast))

    def determine_status(self):
        for cast in self.casts:
            if cast.is_active():
                return 'active'
        
        return 'inactive'

    def find_active_chromecast(self):
        for cast in self.casts:
            if cast.is_active():
                return cast
        return None

    def find_primary_device(self):
        for cast in self.casts:
            if cast.cast.cast_type == 'audio':
                return cast
        return None