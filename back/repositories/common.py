class StorageError(Exception):
    ...


class NotFoundError(StorageError):
    ...


class AlreadyInUse(StorageError):
    ...
