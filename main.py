# author : Philippe Vo
# date   : Mon 04 Jul 2022 02:22:56 PM

# user imports
from src.core.driver import Driver

songFilePath = input("song file [drag & drop file] : ").strip()
driver = Driver()
driver.run(songFilePath)
