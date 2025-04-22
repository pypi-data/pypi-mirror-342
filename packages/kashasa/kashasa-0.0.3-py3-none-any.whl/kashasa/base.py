from collections import namedtuple
from contextlib import suppress
from copy import deepcopy
from functools import partial
from operator import methodcaller
from re import compile  # noqa: A004
from struct import pack
from time import time
from typing import Any, ClassVar

from kalib import (
    Is,
    Logging,
    Property,
    Who,
    is_class,
    json,
    required,
    to_ascii,
    to_bytes,
)
from kalib.signals import Exit
from lz4 import block

from kashasa.compat import Data, Defaults, Model, Sentinel, not_implemented


class Meta(namedtuple(
    'Meta',
    'header serializer compressor checksum embedded payload',
)):
    __slots__ = ()

    @property
    def as_dict(self):
        return self._asdict()

    @property
    def expired(self):
        return (ttl := self.ttl) and ttl + self.stamp < time()

    @property
    def data(self):
        if data := self.embedded:
            return json.loads(block.decompress(data))

    #

    @property
    @not_implemented
    def stamp(self): ...

    @property
    @not_implemented
    def ttl(self): ...

    @property
    @not_implemented
    def version(self): ...

    @property
    @not_implemented
    def value(self): ...

    @property
    @not_implemented
    def offset(self): ...



class Cache(Logging.Mixin):

    Meta: ClassVar = Meta

    class Behavior(Model):

        noloads   : bool = False  # always KeyError
        nostore   : bool = False  # ignore set/del
        nocache   : bool = False  # noloads + nostore

        overwrite : bool = True   # update TTL on set same value
        version   : bool = False  # 0 by default, when False - skip check
        raw       : bool = False  # return Meta object with .value field
        discard_on_missing : bool = False  # force call deleter with key expired

    class Flow(Model):

        # importable with .compress / .decompress
        compress : bytes = Defaults.compression
        level    : int = 3        # compression level
        minsize  : int = 2 ** 8   # minimal size to compress

        # importable with .loads / .dumps
        marshall : bytes = Defaults.serialization

        # importable with .digest
        checksum : str = Defaults.checksum
        hashfunc : str = Defaults.hashfunc

    class Expire(Model):

        # force record time to live
        ttl : float | int = 0.0

        # expiration check callbacks
        func : Any | list[Any] | None = None  # callable or callables

    class Settings(Model): ...

        # custom settings for backend

    # used models configuration

    @Property.Class.Cached
    def Models(cls):  # noqa: N802
        result = []
        for key in dir(cls):
            if key == 'Models' or key.startswith('_') or key != key.capitalize():
                continue

            node = getattr(cls, key)
            if not is_class(node) or not issubclass(node, Model):
                continue

            result.append((Who.Name(node).lower(), node, frozenset(node.model_fields)))

        return tuple(result)

    def fill_config(self, **kw):
        for name, model, keys in self.Models:
            setattr(
                self, name,
                model(**{key: kw.pop(key) for key in sorted(keys & set(kw))}))
        return kw

    def __call__(self, /, **kw):
        new = set(kw)
        i = deepcopy(self)

        for name, model, _ in self.Models:
            src = getattr(self, name).model_dump()
            if set(src) & new:
                setattr(
                    i, name,
                    model(**(src | {k: kw[k] for k in set(src) & new})) )
        return i

    def __enter__(self):
        return self

    def __exit__(self, *args, **kw):
        return self

    # backend instances interface

    @Property.Class.Cached
    def teardown_hook(cls):

        def close():
            for pool in cls.connectors.values():
                try:
                    cls.teardown(pool)
                except Exception as e:  # noqa: PERF203
                    cls.log.exception('teardown exception occurred', exc_info=e)

        Exit.schedule(close)
        return close

    @classmethod
    def teardown(cls, pool): ...

    @not_implemented
    def connector(self, key): ...

    @Property.Class.Cached
    def connectors(cls):
        try:
            return cls.__dict__['__connectors']

        except KeyError:
            cache = {}
            setattr(cls, '__connectors', cache)
            cls.teardown_hook  # noqa: B018 once for each class attach teardown callback
            return cache

    @property
    def pool(self):
        key = self.hash(**self.config)
        cache = self.connectors

        try:
            return cache[key]
        except KeyError:
            cache[key] = pool = self.connector(key)
            return pool

    def __init__(self, *args, **extra):
        self.extra = self.fill_config(**extra)
        self.name = self.extra.pop('name', None)
        super().__init__(*args)

    # primary key and metadata

    @Property.Class.Cached
    def serialize_key(cls):
        return partial(json.dumps, bytes=True)

    def _key_(self, key):
        return to_ascii(self.hash(key))

    @not_implemented
    def _meta_(self, zkey): ...

    def meta(self, key):
        if self.behavior.noloads is True:
            raise KeyError
        return self._meta_(self._key_(key))

    # crup operations

    def __getitem__(self, key):
        def missing_key(msg, discard=True, log=None):
            if log:
                self.log.warning(msg)

            if discard and self.behavior.discard_on_missing:
                self.__delitem__(key)

            return KeyError(msg)

        if self.behavior.noloads is True:
            raise missing_key('noloads enabled, skip getter', discard=False)

        zkey = self._key_(key)
        if not (meta := self._meta_(zkey)):
            raise missing_key(f"{zkey} metadata isn't exists")

        if meta.version < self.version:
            raise missing_key(
                f'{zkey} expired by {meta.version=} < {self.version}')

        if ttl := self.expire.ttl:
            if meta.expired:
                raise missing_key(f'{zkey} expired by document ttl')

            if time() - meta.stamp > ttl:
                raise missing_key(f'{zkey} expired by {ttl=}')

        if funcs := self.expire.func:
            if not Is.iterable(funcs):
                funcs = [funcs]

            if any(func(meta) for func in funcs):
                raise missing_key(f'{zkey} expired by callback')

        data = self._get_(zkey, meta)
        if data is Sentinel:
            raise missing_key(
                f"{zkey} data isn't exists, but {meta=}", log=True)

        data = self.decompress(meta, data)
        data = self.deserialize(meta, data)

        return Data(zkey, meta, data) if self.behavior.raw else data

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key, data, **extra):
        if self.behavior.nostore is True:
            return

        elif data is Sentinel:
            raise ValueError(f'tried to set {Who.Is(Sentinel)} as value')

        zkey = self._key_(key)
        serializer, zval = self.serialize(data)

        checksum = self.checksum(zval)
        with suppress(KeyError):
            if (
                not self.behavior.overwrite and
                (meta := self._meta_(zkey)) and (
                    meta.ttl == 0 or
                    meta.checksum == checksum or
                    meta.stamp + meta.ttl > time()
                )
            ):
                return

        return self._set_(
            zkey, checksum, serializer,
            *self.compress(zval), payload=extra)

    def __delitem__(self, key):
        if self.behavior.nostore is True:
            return
        return self._del_(self._key_(key))

    # other high-level interface

    @not_implemented
    def __len__(self): ...

    @not_implemented
    def __bool__(self): ...

    @not_implemented
    def __contains__(self, key): ...

    # shortcuts

    @Property.Cached
    def serialize(self):
        name = to_bytes(self.flow.marshall)
        func = required(self.flow.marshall).dumps

        if name == Defaults.serialization:
            name = Defaults.Dead

        def dumps(data):
            return name, func(data)
        return dumps

    @Property.Cached
    def compress(self):
        name = to_bytes(self.flow.compress)
        func = required(self.flow.compress).compress

        if name == Defaults.compression:
            name = Defaults.Beef

        level = self.flow.level
        def compress(data):
            data = to_bytes(data)

            if len(data) <= self.flow.minsize:
                zval = block.compress(data)
                if len(zval) >= len(data):
                    return b'', data
                return b'lz4', zval

            return name, func(data, level)
        return compress

    @Property.Cached
    def decompress(self):
        def decompress(meta, data):
            name = meta.compressor

            if not name:
                return data

            elif name == Defaults.Beef:
                name = Defaults.compression

            elif name == b'lz4':
                name = b'lz4.block'

            return required(name).decompress(data)
        return decompress

    @Property.Cached
    def deserialize(self):
        def loads(meta, data):
            serializer = meta.serializer

            if not serializer:
                return data

            elif serializer == Defaults.Dead:
                serializer = Defaults.serialization

            return required(serializer).loads(data)
        return loads

    #

    @Property.Cached
    def checksum(self):
        entity = required(self.flow.checksum)
        def checksum(data):
            return entity(to_bytes(data)).digest()
        return checksum

    @Property.Cached
    def key_sample(self):
        key = Defaults.Dead + Defaults.Beef
        return methodcaller(Defaults.keyview)(required(self.flow.hashfunc)(key))

    @Property.Cached
    def is_hash(self):
        return compile(r'(?i)^([0-9a-f]{%i})$' % len(self.key_sample)).match  # noqa: UP031

    @Property.Cached
    def hash(self):

        is_hash = self.is_hash
        serialize = self.serialize_key

        entity   = required(self.flow.hashfunc)
        epilogue = methodcaller(Defaults.keyview)
        floating = partial(pack, '!d')

        def to_hash(x):
            return epilogue(entity(x))

        def from_primitive(x):
            if isinstance(x, bytes | str):
                if is_hash(x):
                    return x
                value = to_bytes(x)

            elif isinstance(x, bool | int):
                value = x.to_bytes(
                    (x.bit_length() + 7) // 8,
                    byteorder='big', signed=True)

            elif isinstance(x, float):
                value = floating(x)

            elif isinstance(x, complex):
                value = floating(x.real) + floating(x.imag)

            else:
                return Sentinel

            return to_hash(value)

        def key(*args, **kw):
            if not kw:
                if (
                    len(args) == 1 and
                    Is.primitive(args[0]) and
                    (value := from_primitive(args[0])) is not Sentinel
                ):
                    return value

                return to_hash(serialize(args))

            elif not args:
                return to_hash(serialize(kw))

            return to_hash(serialize(args) + serialize(kw))

        key.__qualname__ = f'{Who(self)}.hash.{key.__name__}'
        return key

    #

    @Property.Cached
    def version(self):
        return self.behavior.version or 0
