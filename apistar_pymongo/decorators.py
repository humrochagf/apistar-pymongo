from bson.objectid import ObjectId

registered_collections = []


def collection(cls):
    """
    Decorator to register apistar custom Objects as mongodb collections
    """

    registered_collections.append({
        'collection': cls.__name__.lower(),
        'class': cls,
    })

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], dict):
            id = args[0].pop('_id', None)
        else:
            id = kwargs.pop('_id', None)

        if id:
            self['_id'] = id

        super(cls, self).__init__(*args, **kwargs)

    def __setitem__(self, index, value):
        if index == '_id':
            if type(value) is ObjectId:
                self.id = value
                value = str(value)
            else:
                self.id = ObjectId(value)

        super(cls, self).__setitem__(index, value)

    cls.__init__ = __init__
    cls.__setitem__ = __setitem__

    return cls
