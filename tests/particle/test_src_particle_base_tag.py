#!/usr/bin/python
# -*- coding: utf-8 -*-
from moto.particle.base.tag import BaseTag # type: ignore

def test_init_default():
	tag = BaseTag()
	assert tag.key == ''
	assert tag.value == ''

def test_init_with_key():
	tag = BaseTag(key = 'key')
	assert tag.key == 'key'
	assert tag.value == ''

def test_init_with_key_value():
	tag = BaseTag(key = 'key', value = 'value')
	assert tag.key == 'key'
	assert tag.value == 'value'

def test_str():
	tag = BaseTag(key = 'key', value = 'value')
	assert str(tag) == 'key: value'

def test_dict():
	tag = BaseTag(key = 'key', value = 'value')
	assert tag.__dict__() == {'key': 'value'}

def test_eq():
	tag1 = BaseTag(key = 'key', value = 'value')
	tag2 = BaseTag(key = 'key', value = 'value')
	assert tag1 == tag2

def test_ne():
	tag1 = BaseTag(key = 'key', value = 'value')
	tag2 = BaseTag(key = 'key', value = 'value')
	assert not tag1 != tag2

def test_update():
	tag = BaseTag(key = 'key', value = 'value')
	tag.update(key = 'new_key', value = 'new_value')
	assert tag.key == 'new_key'
	assert tag.value == 'new_value'

def test_get_key():
	tag = BaseTag(key = 'key', value = 'value')
	assert tag.get_key() == 'key'

def test_get_value():
	tag = BaseTag(key = 'key', value = 'value')
	assert tag.get_value() == 'value'

def test_export():
	tag = BaseTag(key = 'key', value = 'value')
	assert tag.export() == {'key': 'value'}
