from datetime import datetime

from sqlalchemy.dialects.sqlite import DATETIME, INTEGER, TEXT
from sqlalchemy.orm import mapped_column

from source.classes.db_manager import DBManager


class MatchingArticles(DBManager.Base):
    __tablename__ = 'MatchingArticles'
    ID = mapped_column(INTEGER, primary_key=True)
    Keyword = mapped_column(TEXT, nullable=False)
    URL = mapped_column(TEXT, nullable=False)
    Title = mapped_column(TEXT)
    Date = mapped_column(DATETIME)
    Author = mapped_column(TEXT)
    ImageURL = mapped_column(TEXT)
    Body = mapped_column(TEXT)
    CreatedOn = mapped_column(DATETIME, default=datetime.now)
    UpdatedOn = mapped_column(DATETIME, default=datetime.now, onupdate=datetime.now)


class CachedUserAgents(DBManager.Base):
    __tablename__ = 'CachedUserAgents'
    ID = mapped_column(INTEGER, primary_key=True)
    UserAgent = mapped_column(TEXT, nullable=False)
    CreatedOn = mapped_column(DATETIME, default=datetime.now)
    UpdatedOn = mapped_column(DATETIME, default=datetime.now, onupdate=datetime.now)
