import hashlib
from hashlib import _hashlib

from moto.particle.constant import (
    HASH_ALGORITHMS,
    STORAGE_UNIT_TABLE,
    TIME_UNIT_TABLE,
    TIMEZONE_TABLE,
)


def test_attribute_time_unit_table():
    assert TIME_UNIT_TABLE["second"] == 1
    assert TIME_UNIT_TABLE["minute"] == 60
    assert TIME_UNIT_TABLE["hour"] == 3600
    assert TIME_UNIT_TABLE["day"] == 86400
    assert TIME_UNIT_TABLE["week"] == 604800
    assert TIME_UNIT_TABLE["month"] == 2592000
    assert TIME_UNIT_TABLE["year"] == 31536000


def test_attribute_storage_unit_table():
    assert STORAGE_UNIT_TABLE["b"] == 1
    assert STORAGE_UNIT_TABLE["byte"] == 1
    assert STORAGE_UNIT_TABLE["kb"] == 1024
    assert STORAGE_UNIT_TABLE["kilobyte"] == 1024
    assert STORAGE_UNIT_TABLE["mb"] == 1048576
    assert STORAGE_UNIT_TABLE["megabyte"] == 1048576
    assert STORAGE_UNIT_TABLE["gb"] == 1073741824
    assert STORAGE_UNIT_TABLE["gigabyte"] == 1073741824
    assert STORAGE_UNIT_TABLE["tb"] == 1099511627776
    assert STORAGE_UNIT_TABLE["terabyte"] == 1099511627776
    assert STORAGE_UNIT_TABLE["pb"] == 1125899906842624
    assert STORAGE_UNIT_TABLE["petabyte"] == 1125899906842624


def test_attribute_timezone_table():
    assert TIMEZONE_TABLE["Australia/Sydney"] == 11
    assert TIMEZONE_TABLE["Australia/Melbourne"] == 11
    assert TIMEZONE_TABLE["Australia/Perth"] == 8
    assert TIMEZONE_TABLE["Australia/Brisbane"] == 10
    assert TIMEZONE_TABLE["Australia/Adelaide"] == 10
    assert TIMEZONE_TABLE["Australia/Darwin"] == 9
    assert TIMEZONE_TABLE["Australia/Hobart"] == 11
    assert TIMEZONE_TABLE["Australia/Canberra"] == 11
    assert TIMEZONE_TABLE["Australia/Melbourne"] == 11
    assert TIMEZONE_TABLE["Australia/Sydney"] == 11
    assert TIMEZONE_TABLE["Australia/Broken_Hill"] == 10
    assert TIMEZONE_TABLE["Australia/Lord_Howe"] == 11
    assert TIMEZONE_TABLE["Australia/Lindeman"] == 10
    assert TIMEZONE_TABLE["Australia/Currie"] == 11
    assert TIMEZONE_TABLE["Australia/Eucla"] == 8
    assert TIMEZONE_TABLE["Australia/ACT"] == 11
    assert TIMEZONE_TABLE["Australia/Yancowinna"] == 10
    assert TIMEZONE_TABLE["Australia/North"] == 9
    assert TIMEZONE_TABLE["Australia/South"] == 10
    assert TIMEZONE_TABLE["Australia/Tasmania"] == 11
    assert TIMEZONE_TABLE["Australia/Victoria"] == 11
    assert TIMEZONE_TABLE["Australia/West"] == 8
    assert TIMEZONE_TABLE["Australia/Yancowinna"] == 10
    assert TIMEZONE_TABLE["Australia/Canberra"] == 11
    assert TIMEZONE_TABLE["Australia/Lord_Howe"] == 11
    assert TIMEZONE_TABLE["Australia/Melbourne"] == 11
    assert TIMEZONE_TABLE["Australia/Sydney"] == 11
    assert TIMEZONE_TABLE["Australia/Broken_Hill"] == 10
    assert TIMEZONE_TABLE["Australia/Lindeman"] == 10
    assert TIMEZONE_TABLE["Australia/Currie"] == 11
    assert TIMEZONE_TABLE["Australia/Eucla"] == 8
    assert TIMEZONE_TABLE["Australia/ACT"] == 11
    assert TIMEZONE_TABLE["Australia/Yancowinna"] == 10
    assert TIMEZONE_TABLE["Australia/North"] == 9


def test_attribute_hash_algorithms():
    for key in HASH_ALGORITHMS.keys():
        assert key in hashlib.algorithms_available
        assert HASH_ALGORITHMS[key].name == key
        assert HASH_ALGORITHMS[key].digest_size == hashlib.new(key).digest_size
        assert HASH_ALGORITHMS[key].block_size == hashlib.new(key).block_size
