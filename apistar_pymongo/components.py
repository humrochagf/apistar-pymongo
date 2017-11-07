import contextlib
import typing

from apistar import Component, Settings
from pymongo import MongoClient

from .decorators import registered_collections


class MongoBackend(object):
    def __init__(self, settings: Settings) -> None:
        """
        Configure MongoDB database backend.

        Args:
            settings: The application settings dictionary.
        """

        self.config = settings.get('DATABASE', {})
        self.url = self.config.get('URL', '')
        self.database_name = self.config.get('NAME', '')
        self.client = None

    def connect(self) -> None:
        self.client = MongoClient(self.url)

    def close(self) -> None:
        if self.client:
            self.client.close()

        self.client = None

    def drop_database(self) -> None:
        self.connect()
        self.client.drop_database(self.database_name)
        self.close()


class Session(object):
    """
    Class responsible to hold a mongodb session instance
    """
    def __init__(self, backend: MongoBackend) -> None:
        self.db = backend.client[backend.database_name]
        for model in registered_collections:
            setattr(self, model['collection'], self.db[model['collection']])


@contextlib.contextmanager
def get_session(backend: MongoBackend) -> typing.Generator[Session,
                                                           None, None]:
    """
    Create a new context-managed database session for mongodb
    """
    backend.connect()

    yield Session(backend)

    backend.close()


components = [
    Component(MongoBackend),
    Component(Session, init=get_session, preload=False),
]
