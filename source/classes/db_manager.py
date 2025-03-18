from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from source.classes.base_storage_manager import BaseStorageManager


class DBManager(BaseStorageManager):
    Base = declarative_base()

    def __init__(self, filepath: Path):
        self.__engine = None
        self.__session = None
        self.__initialize_connection(filepath)

    def __initialize_connection(self, filepath: Path):
        self.__engine = create_engine(f'sqlite:///{str(filepath)}')
        self.__session = sessionmaker(self.__engine)
        DBManager.Base.metadata.create_all(bind=self.__engine)

    def store(self):
        pass

    def retrieve(self):
        pass

    def destroy(self):
        self.__engine.dispose()
