import os
import shutil
import logging


class Utils:
    logging = logging.getLogger("Utils")

    @staticmethod
    def init_directories(*directories):
        for directory in directories:
            Utils.init_directory(directory)

    @staticmethod
    def init_directory(directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)
            Utils.logging.debug(f"Deleted {directory}.")

        while os.path.exists(directory):
            pass

        os.makedirs(directory)
        Utils.logging.debug(f"Created {directory}.")
