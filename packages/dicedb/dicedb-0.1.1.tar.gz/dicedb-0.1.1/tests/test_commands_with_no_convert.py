"""These tests will run with `try_to_convert=False`."""

from dicedb import Dice

dice = Dice('localhost', 7379)
dice.flushdb()

def test_decr():
    dice.set('k', 43)
    dice.decr('k')

    assert dice.get('k') == '42'


def test_decrby():
    dice.set('k43', 43)
    dice.decrby('k43', 10)

    assert dice.get('k43') == '33'


def test_incr():
    dice.set('k-incr', 42)
    dice.incr('k-incr')

    assert dice.get('k-incr') == '43'


def test_incrby():
    dice.set('k-incr-by', 52)
    dice.incr_by('k-incr-by', 10)

    assert dice.get('k-incr-by') == '62'


def test_hget_all():
    dice.hset('k-hget-all-with-int-value', 'field1', 23, 'field2', 74)
    assert dice.hget_all('k-hget-all-with-int-value') == {'field1': '23', 'field2': '74'}