from x17_container.dockers.base.configuration import Configuration


class TestConfiguration:
    def test_from_dict_and_to_dict(self):
        data = {"driver": "bridge", "enable_ipv6": True}
        config = Configuration.from_dict(data)
        assert config.to_dict() == data

    def test_eq_and_ne(self):
        conf1 = Configuration(driver="bridge", enable_ipv6=True)
        conf2 = Configuration(driver="bridge", enable_ipv6=True)
        conf3 = Configuration(driver="host")
        assert conf1 == conf2
        assert conf1 != conf3
        assert conf1 == {"driver": "bridge", "enable_ipv6": True}
        assert conf1 != {"driver": "host"}

    def test_copy(self):
        conf1 = Configuration(driver="bridge", enable_ipv6=True)
        conf2 = conf1.copy(driver="host")
        assert conf2.driver == "host"
        assert conf2.enable_ipv6 is True
        assert conf1.driver == "bridge"
