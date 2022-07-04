# author : Philippe Vo
# date   : Mon 04 Jul 2022 02:22:56 PM

# 3rd party imports
import logging
import pygame
from pathlib import Path
from os.path import exists

class Driver:

    class InputFileError(Exception):
        def __init__(self):
            super().__init__()
            logging.warning("file input error")

    def __init__(self):
        pass

    def verify(self, filePath: str):
        fileExists = exists(filePath)
        fileExt = Path(filePath).suffix
        if fileExt == ".mp3" and fileExists:
            return True
        else:
            raise Driver.InputFileError

    def run(self, filePath: str):
        if self.verify(filePath):

            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.load(filePath)
            song = pygame.mixer.Sound(filePath)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time = ((pygame.mixer.music.get_pos() / 1000) * 100) / song.get_length()
                print(time)
                pygame.time.Clock().tick(10)
