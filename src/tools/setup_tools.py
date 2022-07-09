# author : Philippe Vo
# date   : Mon 02 May 2022 07:24:29 PM

# 3rd party imports
import logging
import os

logger = logging.getLogger(__name__)

def get_user_choice(options: list, msg: str):
    """show list of options for user and ask them to choose an option
    """
    validIdxs = []
    for idx, val in enumerate(options):
        print("{} : {}".format(idx, val))
        validIdxs.append(idx)

    validChoice = False
    while not validChoice:
        try:
            idxChoose = int(input(msg))
            logging.info("selected : {}".format(options[idxChoose]))
            validChoice = True

        except (ValueError, IndexError):
            logging.warning("invalid choice")

    return idxChoose
