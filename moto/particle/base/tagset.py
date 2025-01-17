from moto.particle.base.tag import BaseTag

class BaseTagset:
	@classmethod
	def from_dict(cls, dict):
		return cls(
			tags = [
				BaseTag.from_dict({str(key): str(value)}) for key, value in dict.items()
			]
		)
	
	def from_list(cls, list):
		return cls(
			tags = [
				BaseTag.from_dict(tag) for tag in list
			]
		)

	# Init method
	def __init__(
			self,
			tags = [],
		):
		self.tags = tags
		self.book = self.__dict__()
	
	def __str__(self):
		return str(self.book)
	
	def __dict__(self):
		result = {}
		for tag in self.tags:
			result.update(tag.export())
		return result
	
	def export(self):
		return self.book

	def add(self, tag):

		self.tags.append(tag)
		self.book = self.__dict__()
	
	def remove(self, tag):
		if tag in self.tags:
			self.tags.remove(tag)
		self.book = self.__dict__()
	
	def get(self, key):
		for tag in self.tags:
			if tag.get_key() == key:
				return tag
		return None
	
	def update(self, key = None, value = None, tag = None):
		if (key and value):
			if key in self.book: self.remove(self.get(key))
			self.add(BaseTag(key = key, value = value))
		else:
			self.remove(tag)
			self.add(tag)
		self.book = self.__dict__()

		