from collections import namedtuple
from functools import wraps

from kalib import Logging, Who
from kalib.classes import Missing
from pydantic import BaseModel as Model

__all__ = (
    'Data',
    'Defaults',
    'Model',
    'Sentinel',
    'not_implemented',
)

Sentinel = Missing()
Data = namedtuple('Data', 'key meta value')


def not_implemented(func):
    @wraps(func)
    def wrapper(self, *args, **kw):
        msg = f'{Who(self)}.{Who.Name(func)}({Logging.Args(*args, **kw)})'
        raise NotImplementedError(msg)
    return wrapper


class Defaults:

    Dead = b'\xde\xad'
    Beef = b'\xbe\xef'

    checksum = 'xxhash.xxh32'
    hashfunc = 'xxhash.xxh128'

    keyview = 'hexdigest'
    serialization = b'pickle'
    compression   = b'zstd'
