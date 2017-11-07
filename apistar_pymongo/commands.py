from apistar import Command

from .components import MongoBackend


def drop_database(backend: MongoBackend) -> None:
    """
    Drop the mongodb database from defined at settings
    """
    backend.drop_database()


commands = [
    Command('drop_database', drop_database),
]
