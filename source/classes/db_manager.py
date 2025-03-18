from collections.abc import Sequence
from pathlib import Path

import pandas
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, InstrumentedAttribute

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
        pass

    def store(self):
        pass

    def retrieve(self, columns: Sequence[InstrumentedAttribute]) -> DataFrame:
        with self.__session.begin() as session:
            query_result = session.query(*columns)
            pandas_result = pandas.read_sql(sql=query_result.statement, con=self.__engine)
            return pandas_result

    def destroy(self):
        self.__engine.dispose()
