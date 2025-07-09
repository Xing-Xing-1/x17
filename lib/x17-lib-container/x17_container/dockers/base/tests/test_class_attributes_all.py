from x17_container.dockers.base.attributes import Attributes

class TestAttributes:
    def test_from_dict_and_to_dict(self):
        data = {"id": "abc123", "scope": "local"}
        attr = Attributes.from_dict(data)
        assert attr.to_dict() == data

    def test_eq_and_ne(self):
        attr1 = Attributes(id="abc123", scope="local")
        attr2 = Attributes(id="abc123", scope="local")
        attr3 = Attributes(id="def456")
        assert attr1 == attr2
        assert attr1 != attr3
        assert attr1 == {"id": "abc123", "scope": "local"}
        assert attr1 != {"id": "xyz"}

    def test_dynamic_attributes(self):
        attr = Attributes(foo="bar", number=123)
        assert attr.foo == "bar"
        assert attr.number == 123
        assert attr.to_dict() == {"foo": "bar", "number": 123}