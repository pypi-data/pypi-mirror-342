from contextlib import suppress
from io import BytesIO
from math import ceil
from operator import attrgetter
from pathlib import Path
from time import time
from typing import ClassVar

from construct import Int8ub, Int16ub, Int24ub, Int32ub, Int64ub, Struct
from kalib import Property, Who, json
from lz4 import block

from kashasa.base import Cache
from kashasa.compat import Sentinel, not_implemented

Header = Struct(
    'version' / Int16ub,
    'expire'  / Struct(
        'ttl'   / Int24ub,
        'stamp' / Int64ub,
    ),
    'size' / Struct(
        'meta' / Int24ub,
        'data' / Int32ub,
        'checksum' / Int8ub,
        'compressor' / Int8ub,
        'serializer' / Int8ub,
    ),
    'flags' / Int32ub,
)


class Meta(Cache.Meta):

    @property
    def stamp(self):
        return self.header.expire.stamp / 1000.0

    @property
    def ttl(self):
        return self.header.expire.ttl / 1000.0

    @property
    def version(self):
        return self.header.version

    @property
    def value(self):
        if self.payload and len(self.payload) == self.header.size.data:
            return self.payload
        return Sentinel

    @property
    def offset(self):
        size = self.header.size
        header = Header.sizeof()
        getter = attrgetter('compressor', 'serializer', 'checksum', 'meta')
        return sum(getter(size)) + header, size.data + header + 7


class Native(Cache):

    Meta   : ClassVar = Meta
    Header : ClassVar = Header

    class Behavior(Cache.Behavior):
        mode : int = 0o755

    @Property.Cached
    def root(self):
        path = (
            Path(self.path) / (
                f'{self.name or "cache"}.{Who.Name(self).lower()}'))

        path.resolve().parent.mkdir(
            mode = self.behavior.mode,
            parents  = True,
            exist_ok = True,
        )
        return path

    def __init__(self, *args, **kw):
        self.path = kw.pop('root', 'var')
        super().__init__(*args, **kw)

    @not_implemented
    def _get_meta_(self, zkey): ...

    def _meta_(self, zkey):
        with suppress(KeyError):
            header = self._get_meta_(zkey)
            return self._header_unpack_(header)
        return Sentinel

    # binary header with value metadata and payload

    def _header_pack_(self, zkey, checksum, serializer, compressor, zval, payload):

        ttl = ceil(self.expire.ttl * 1000)
        pay = block.compress(json.dumps(payload, bytes=True)) if payload else b''

        meta = {
            'flags'   : 0,
            'version' : self.version,

            'size': {
                'meta': len(pay),
                'data': len(zval),
                'checksum'  : len(checksum),
                'compressor': len(compressor),
                'serializer': len(serializer)},

            'expire': {
                'ttl'   : ttl,
                'stamp' : ceil(time() * 1000)}}

        value = BytesIO()
        header = self.Header.build(meta)

        list(map(value.write,
            (header, serializer, compressor, checksum, pay)))
        return value.getvalue()

    def _header_unpack_(self, raw):
        if not raw:
            return Sentinel

        # parse struct header with offsets

        meta = self.Header.parse(raw)
        order = (
            meta.size.serializer,
            meta.size.compressor,
            meta.size.checksum,
            meta.size.meta)
        result = [None, None, None, None, None]  # and last for zval

        # also read variable length data after header

        offset = self.Header.sizeof()
        for no, i in enumerate(order):
            result[no] = raw[offset: offset + i]
            offset += i

        # check what's after header and variable position

        header, recordsize = len(raw), offset + meta.size.data
        if header < recordsize:
            ...

        elif header > recordsize:
            result[-1] = raw[offset:]
            self.log.error(f'{header=} > {recordsize=}: {meta}')

        elif header == recordsize:
            result[-1] = raw[offset:]

        return self.Meta(meta, *result)
