from diffprep.processors.json import prepare_json


class TestPrepareJson:
    def test_prepare_json_canonicalizes(self) -> None:
        data = b'{"b":2,"a":1}'

        result = prepare_json(data)

        assert result == b'{"a":1,"b":2}'
