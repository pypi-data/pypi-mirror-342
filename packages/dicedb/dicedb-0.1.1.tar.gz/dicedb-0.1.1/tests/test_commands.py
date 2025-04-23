"""These tests will run with `try_to_convert=True`."""
from dicedb import Dice

dice = Dice('localhost', 7379, try_to_convert=True)
dice.flushdb()

def test_decr():
    dice.set('k', 43)
    dice.decr('k')

    assert dice.get('k') == 42


def test_decrby():
    dice.set('k43', 43)
    dice.decrby('k43', 10)

    assert dice.get('k43') == 33

def test_delete():
    dice.set('k1', 'v1')
    dice.set('k2', 'v2')

    assert dice.delete('k1', 'k2', 'k3') == 2

def test_echo():
    assert dice.echo('hello') == 'hello'

def test_exists():
    dice.set('k11', 'v1')
    dice.set('k22', 'v2')

    assert dice.exists(['k11', 'k22', 'k33']) == 2

def test_expire_time():
    assert dice.expire_time('k-non-exists') == -2

def test_flushdb():
    dice.set('k-flushdb', 'v-flushdb')
    dice.set('k-flushdb-1', 'v-flushdb-2')
    dice.flushdb()

    assert dice.get('k-flushdb') == ''
    assert dice.get('k-flushdb-1') == ''


def test_get():
    dice.set('k-get', 'v-get')

    assert dice.get('k-get') == 'v-get'
    assert dice.get('k-get-non-exists') is ''

def test_get_del():
    dice.set('k-get-del', 'v-get-del')

    assert dice.get_del('k-get-del') == 'v-get-del'
    assert dice.get('k-get-del') == ''

def test_hget():
    dice.hset('k-hget', 'field1', 'value1')

    assert dice.hget('k-hget', 'field1') == 'value1'
    assert dice.hget('k-hget', 'field2') == ''

def test_hget_all():
    dice.hset('k-hget-all', 'field1', 'value1', 'field2', 'value2')

    assert dice.hget_all('k-hget-all') == {'field1': 'value1', 'field2': 'value2'}
    assert dice.hget_all('k-non-exists') == {}

    dice.hset('k-hget-all-with-int-value', 'field1', 23, 'field2', 74)
    assert dice.hget_all('k-hget-all-with-int-value') == {'field1': 23, 'field2': 74}


def test_incr():
    dice.set('k-incr', 42)
    dice.incr('k-incr')

    assert dice.get('k-incr') == 43


def test_incrby():
    dice.set('k-incr-by', 52)
    dice.incr_by('k-incr-by', 10)

    assert dice.get('k-incr-by') == 62

def test_ping():
    assert dice.ping() == 'PONG'
    assert dice.ping('hello') == 'PONG hello'

def test_type():
    dice.set('k-type', 'v-type')
    dice.set('k-type-int', 45)

    assert dice.typeof('k-type') == 'string'
    assert dice.typeof('k-type-int') == 'int'
    assert dice.typeof('k-non-exists') == 'none'

def test_ttl():
    dice.set('k-ttl', 'v-ttl')
    assert dice.ttl('k-ttl') == -1


def test_expire():
    dice.set('k-expire', 'v-expire')
    assert 1 == dice.expire('k-expire', 10)
    dice.set('k-expire2', 'v-expire2')
    assert 1 == dice.expire('k-expire2', 10, 'NX')
    assert 1 == dice.expire('k-expire2', 20, 'XX')
    assert 0 == dice.expire('k-expire2', 20, 'NX')

def test_expire_at():
    dice.set('k-expire-at', 'v-expire-at')
    assert 1 == dice.expire_at('k-expire-at', 1740829942)
    assert 0 == dice.expire_at('k-expire-at', 1740829942, 'NX')
    assert 0 == dice.expire_at('k-expire-at', 1740829942, 'XX')
    assert 0 == dice.expire_at('k-expire-at', 1740829943, 'GT')

def test_get_ex():
    dice.set('k-get-ex', 'v-get-ex')
    assert 'v-get-ex' == dice.get_ex('k-get-ex', ex=1000)
    assert dice.ttl('k-get-ex') < 1000
    assert 'v-get-ex' == dice.get_ex('k-get-ex', px=200000)
    assert 'v-get-ex' == dice.get_ex('k-get-ex', exat=1772377267)
    assert 'v-get-ex' == dice.get_ex('k-get-ex', pxat=1772377267000)
    assert 'v-get-ex' == dice.get_ex('k-get-ex', persist=True)


def test_set():
    assert dice.set('k-set', 'v-set') is None
    assert dice.set('k-set', 'v-set', ex=10) is None
    assert dice.set('k-set', 'v-set', px=10000) is None
    assert dice.set('k-set', 'v-set', exat=1772377267) is None
    assert dice.set('k-set', 'v-set', pxat=1772377267000) is None
    assert dice.set('k-set', 'v-set', nx=True) is None
    assert dice.set('k-set', 'v-set', xx=True) is None
    assert dice.set('k-set', 'v-set', keep_ttl=True) is None