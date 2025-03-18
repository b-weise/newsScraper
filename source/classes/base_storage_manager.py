import abc


class BaseStorageManager(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def store(self):
        pass

    @abc.abstractmethod
    def retrieve(self):
        pass
