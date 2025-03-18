import abc


class BaseStorageManager(metaclass=abc.ABCMeta):
    """
    Specifies abstract methods that subclasses must implement.
    """

    @abc.abstractmethod
    def store(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def retrieve(self, *args, **kwargs):
        pass
