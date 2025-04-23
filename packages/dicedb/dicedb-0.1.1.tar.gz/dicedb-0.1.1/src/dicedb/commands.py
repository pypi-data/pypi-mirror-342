"""Commands module for DiceDB client."""

import uuid
from typing import Any, Literal, Protocol
from typing import Union, Iterable

from . import const
from .exceptions import DiceParamError


class _CommandsProtocol(Protocol):
    def _fire(self, cmd: str, *args) -> Any: ...


class DiceCommands(_CommandsProtocol):
    """DiceCommands class provides a set of methods to interact with the DiceDB server."""

    def decrby(self, key: str, delta: int = 1) -> Union[int, str]:
        return self._fire('DECRBY', key, delta)

    decr = decrby

    def delete(self, *keys: Iterable[str]) -> int:
        return self._fire('DEL', *keys)

    def echo(self, message: str):
        return self._fire('ECHO', message)

    def exists(self, keys: Iterable[str]) -> int:
        return self._fire('EXISTS', *keys)

    def expire(
        self, key: str, seconds: int, option: Literal['NX', 'XX'] = None
    ) -> int:
        if option is not None:
            if option not in const.EXPIRE_OPTIONS:
                raise ValueError(f'Invalid expire option: {option}')
            return self._fire('EXPIRE', key, seconds, option)
        return self._fire('EXPIRE', key, seconds)

    def expire_at(
        self,
        key: str,
        timestamp: int,
        option: Literal['NX', 'XX', 'GT', 'LT'] = None,
    ) -> int:
        if option is not None:
            if option not in const.EXPIRE_AT_OPTIONS:
                raise ValueError(f'Invalid expire_at option: {option}')
            return self._fire('EXPIREAT', key, timestamp, option)
        return self._fire('EXPIREAT', key, timestamp)

    def expire_time(self, key: str) -> int:
        return self._fire('EXPIRETIME', key)

    def flushdb(self):
        return self._fire('FLUSHDB')

    def get(self, key: str) -> Any:
        return self._fire('GET', key)

    def get_del(self, key: str) -> Any:
        return self._fire('GETDEL', key)

    def get_ex(
        self,
        key: str,
        *,
        ex: int = None,
        px: int = None,
        exat: int = None,
        pxat: int = None,
        persist: bool = False,
    ) -> Any:
        opset = {ex, px, exat, pxat}
        if len(opset) > 2 or len(opset) > 1 and persist:
            raise DiceParamError(
                '``ex``, ``px``, ``exat``, ``pxat``, '
                'and ``persist`` are mutually exclusive.'
            )
        args = []
        if ex is not None:
            args.extend(['EX', ex])
        if px is not None:
            args.extend(['PX', px])
        if exat is not None:
            args.extend(['EXAT', exat])
        if pxat is not None:
            args.extend(['PXAT', pxat])
        if persist:
            args.append('PERSIST')
        return self._fire('GETEX', key, *args)

    def get_watch(self, key: str):
        raise NotImplementedError()

    def hget(self, key: str, filed: str) -> Union[str, None]:
        return self._fire('HGET', key, filed)

    def hget_all(self, key: str):
        return self._fire('HGETALL', key)

    def hget_all_watch(self):
        raise NotImplementedError()

    def hset(self, key: str, *args, **kwargs) -> Union[int, None]:
        if len(args) % 2 != 0:
            raise ValueError(
                'Positional args must be even-length (field1, val1, field2, val2...)'
            )
        merged_args = [key]
        merged_args.extend(args)

        for field, value in kwargs.items():
            merged_args.extend([field, value])

        return self._fire('HSET', *merged_args)

    def incr_by(self, key: str, delta: int = 1):
        return self._fire('INCRBY', key, delta)

    incr = incr_by

    def ping(self, message: str = None) -> str:
        if message is not None:
            return self._fire('PING', message)
        return self._fire('PING')

    def ttl(self, key: str) -> int:
        return self._fire('TTL', key)

    def typeof(self, key: str):
        return self._fire('TYPE', key)

    def set(
        self,
        key: str,
        value,
        *,
        ex: int = None,
        px: int = None,
        exat: int = None,
        pxat: int = None,
        xx: bool = False,
        nx: bool = False,
        keep_ttl: bool = False,
    ) -> Union[int, str]:
        pieces = [key, value]
        if ex is not None:
            pieces.extend(['EX', ex])
        if px is not None:
            pieces.extend(['PX', px])
        if exat is not None:
            pieces.extend(['EXAT', exat])
        if pxat is not None:
            pieces.extend(['PXAT', pxat])
        if keep_ttl:
            pieces.append('KEEPTTL')

        if nx:
            pieces.append('NX')
        if xx:
            pieces.append('XX')


        return self._fire('SET', *pieces)

    def _handshake(self, client_id: str):
        return self._fire('HANDSHAKE', client_id, 'command')

    def unwatch(self, fingerprint: str):
        return self._fire('UNWATCH', fingerprint)

    def zadd(self):
        raise NotImplementedError()

    def zcard(self, key: str) -> int:
        return self._fire('ZADD', key)

    def zcount(self, key: str, min_score: int, max_score: int) -> int:
        return self._fire('ZCOUNT', key, min_score, max_score)

    def zpopmax(self, key: str, count: Union[int, None] = None):
        args = (count is not None) and [count] or []
        return self._fire('ZPOPMAX', key, *args)

    def zpopmin(self, key: str, count: Union[int, None] = None):
        args = (count is not None) and [count] or []
        return self._fire('ZPOPMIN', key, *args)

    def zrange(self, key: str, start: int, end: int):
        return self._fire('ZRANGE', key, start, end)

    def zrank(self, key: str, member: str):
        return self._fire('ZRANK', key, member)

    def zrem(self, key: str, *args):
        return self._fire('ZREM', key, *args)