from moto.particle.base.tag import Tag # type: ignore

def test_init_default():
	tag = Tag()
	assert tag.key == ''
	assert tag.value == ''

def test_init_with_key():
	tag = Tag(key = 'key')
	assert tag.key == 'key'
	assert tag.value == ''

def test_init_with_key_value():
	tag = Tag(key = 'key', value = 'value')
	assert tag.key == 'key'
	assert tag.value == 'value'

def test_str():
	tag = Tag(key = 'key', value = 'value')
	assert str(tag) == 'key: value'

def test_dict():
	tag = Tag(key = 'key', value = 'value')
	assert tag.__dict__() == {'key': 'value'}

def test_eq():
	tag1 = Tag(key = 'key', value = 'value')
	tag2 = Tag(key = 'key', value = 'value')
	assert tag1 == tag2

def test_ne():
	tag1 = Tag(key = 'key', value = 'value')
	tag2 = Tag(key = 'key', value = 'value')
	assert not tag1 != tag2

def test_update():
	tag = Tag(key = 'key', value = 'value')
	tag.update(key = 'new_key', value = 'new_value')
	assert tag.key == 'new_key'
	assert tag.value == 'new_value'

def test_get_key():
	tag = Tag(key = 'key', value = 'value')
	assert tag.get_key() == 'key'

def test_get_value():
	tag = Tag(key = 'key', value = 'value')
	assert tag.get_value() == 'value'

def test_export():
	tag = Tag(key = 'key', value = 'value')
	assert tag.export() == {'key': 'value'}
