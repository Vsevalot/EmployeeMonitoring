from abc import ABC, abstractmethod


class BaseView(ABC):
    @abstractmethod
    def initialize(self):
        pass
