# API Star Pymongo Backend

A API Star Backend to add suport to [MongoDB](https://www.mongodb.com/) through [pymongo](https://api.mongodb.com/python/current/) library.

To use this you first need to install `pymongo`.

```bash
$ pip install pymongo
```

## Settings

You then need to add the database config to your settings, and install the
additional components and commands for MongoDB:

* `NAME` - The MongoDB database name.
* `URL` - The [Database URL](https://docs.mongodb.com/manual/reference/connection-string/).

```python
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.backends import mongo_backend

# Configure database settings.
settings = {
    "DATABASE": {
        "NAME": "my_database",
        "URL": "mongodb://localhost:27017"
    }
}

app = App(
    routes=routes,
    settings=settings,
    commands=mongo_backend.commands,  # Install custom commands.
    components=mongo_backend.components  # Install custom components.
)
```

## Mapping collections

To mount the database collection mapping you just need to import the `collection`
decorator and add them to the typesystem classes:

```python
from apistar import typesystem
from apistar.backends.mongo_backend import collection

@collection
class Customer(typesystem.Object):
    properties = {
        "name": typesystem.string(max_length=255)
    }
```

## Interacting with the database

To interact with the database, use the `Session` component. This will expose the
database mapping to be accessed at the view:

```python
from apistar.backends.mongo_backend import Session

def create_customer(session: Session, customer: Customer):
    session.customer.insert_one(customer)
    return customer
```
