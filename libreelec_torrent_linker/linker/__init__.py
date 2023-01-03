from abc import ABC, abstractmethod
import logging


class AbstractLinker(ABC):
    def __init__(self, new_path, scanner):
        super().__init__()
        self.new_path = new_path
        self.scanner = scanner
        self.logging = logging.getLogger(self.__class__.__name__)

    def link(self):
        for item in self.scanner.scan():
            self._link_item(item)

    @abstractmethod
    def _link_item(self, item):
        pass
