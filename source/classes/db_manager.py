from collections.abc import Sequence
from pathlib import Path
from typing import Optional

import pandas
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import declarative_base, sessionmaker, InstrumentedAttribute

from source.classes.base_storage_manager import BaseStorageManager


class RecordsMismatchException(Exception):
    pass


class DBManager(BaseStorageManager):
    Base = declarative_base()

    def __init__(self, filepath: Path,
                 record_autofill_field_names: Sequence[str] = ('ID', 'CreatedOn', 'UpdatedOn')):
        self.__engine = None
        self.__session = None
        self.__record_autofill_field_names = record_autofill_field_names
        self.__initialize_connection(filepath)

    def __initialize_connection(self, filepath: Path):
        self.__engine = create_engine(f'sqlite:///{str(filepath)}')
        self.__session = sessionmaker(self.__engine)
        DBManager.Base.metadata.create_all(bind=self.__engine)
        pass

    def store(self, records: Sequence[Base]):
        def record_as_dict(record):
            record_dict = {col.name: getattr(record, col.name)
                           for col in record.__table__.columns}
            for autofill_field_name in self.__record_autofill_field_names:
                if autofill_field_name in record_dict:
                    del record_dict[autofill_field_name]
            return record_dict

        def type_check_contents(values: Sequence, expected_type: type) -> bool:
            if len(values) > 0 and all(map(lambda value: (isinstance(value, expected_type)), values)):
                return True
            else:
                return False

        if len(records) == 0:
            return

        table = records[0].__class__
        if not type_check_contents(values=records, expected_type=table):
            raise RecordsMismatchException('All records must belong to the same table.')

        with self.__session.begin() as session:
            record_dicts = list(map(record_as_dict, records))
            insert_stmt = insert(table).values(record_dicts)
            ignore_duplicates_stmt = insert_stmt.on_conflict_do_nothing()
            session.execute(ignore_duplicates_stmt)
            session.commit()

    def retrieve(self, columns: Optional[Sequence[InstrumentedAttribute]] = None,
                 table: Optional[Base] = None) -> DataFrame:
        query_object = columns or [table]
        with self.__session.begin() as session:
            query_result = session.query(*query_object)
            pandas_result = pandas.read_sql(sql=query_result.statement, con=self.__engine)
            return pandas_result

    def destroy(self):
        self.__engine.dispose()
