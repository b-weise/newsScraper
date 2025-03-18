import abc


class BaseStorageManager(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def store(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def retrieve(self, *args, **kwargs):
        pass
