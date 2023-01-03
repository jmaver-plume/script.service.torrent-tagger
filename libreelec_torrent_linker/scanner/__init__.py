import logging


class Scanner:
    def __init__(self, path):
        self.path = path
        self.logging = logging.getLogger(self.__class__.__name__)
