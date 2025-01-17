from moto.particle.base.tagset import Tagset
from moto.particle.base.tag import Tag
import pytest #type: ignore


@pytest.fixture
def tagset_empty_instance():
	return Tagset()

@pytest.fixture
def tagset_instance():
	return Tagset(
		tags = [
			Tag(key = 'name', value = 'peter'),
			Tag(key = 'age', value = '25'),
			Tag(key = 'gender', value = 'male'),
		]
	)
	
def test_init_default(tagset_empty_instance):
	assert tagset_empty_instance.tags == []
	assert tagset_empty_instance.book == {}

def test_init_with_tags(tagset_instance):
	assert tagset_instance.tags == [
		Tag(key = 'name', value = 'peter'),
		Tag(key = 'age', value = '25'),
		Tag(key = 'gender', value = 'male'),
	]

def test_empty_instance_str(tagset_empty_instance):
	assert str(tagset_empty_instance) == '{}'

def test_instance_str(tagset_instance):
	assert str(tagset_instance) == "{'name': 'peter', 'age': '25', 'gender': 'male'}"
	  	
def test_empty_instance_dict(tagset_empty_instance):
	assert tagset_empty_instance.__dict__() == {}

def test_instance_dict(tagset_instance):
	assert tagset_instance.__dict__() == {'name': 'peter', 'age': '25', 'gender': 'male'}
													  
def test_empty_instance_export(tagset_empty_instance):
	assert tagset_empty_instance.export() == {}

def test_instance_export(tagset_instance):
	assert tagset_instance.export() == {'name': 'peter', 'age': '25', 'gender': 'male'}

def test_add(tagset_instance):
	tagset_instance.add(Tag(key = 'name', value = 'peter'))
	assert Tag(key = 'name', value = 'peter') in tagset_instance.tags
	assert 'name' in tagset_instance.book
	assert tagset_instance.book['name'] == 'peter'

	tagset_instance.add(Tag(key = 'phone', value = '123123123'))
	assert Tag(key = 'phone', value = '123123123') in tagset_instance.tags
	assert 'phone' in tagset_instance.book
	assert tagset_instance.book['phone'] == '123123123'

def test_remove(tagset_instance):
	tagset_instance.add(Tag(key = 'phone', value = '123123123'))
	tagset_instance.remove(Tag(key = 'phone', value = '123123123'))
	assert 'phone' not in tagset_instance.book
	assert Tag(key = 'phone', value = '123123123') not in tagset_instance.tags

def test_get(tagset_instance):
	tagset_instance.add(Tag(key = 'phone', value = '123123123'))
	assert tagset_instance.get('phone') == Tag(key = 'phone', value = '123123123')
	assert tagset_instance.get('email') == None

def test_update(tagset_instance):
	tagset_instance.add(Tag(key = 'phone', value = '123123123'))
	tagset_instance.update(key = 'phone', value = '321321321')
	assert tagset_instance.get('phone') == Tag(key = 'phone', value = '321321321')

	tagset_instance.update(tag = Tag(key = 'email', value = '123123123@qq.com',))
	assert tagset_instance.get('phone') == Tag(key = 'phone', value = '321321321')
	assert tagset_instance.get('email') == Tag(key = 'email', value = '123123123@qq.com',)
	tagset_instance.update(key = 'address', value = 'abc street')
	assert tagset_instance.get('address') == Tag(key = 'address', value = 'abc street')

