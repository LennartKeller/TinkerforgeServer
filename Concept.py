from flask import Flask
from TinkerforgeServer import ObjectServer


class TestObject:

    def __init__(self, t="Foo"):
        self.t = t

    def test(self):
        return 'Bar'

    def upper(self, s: str = "Bus"):
        return s.upper()

    def test_method(self, *args, **kwargs):
        return [args, kwargs]


if __name__ == '__main__':
    test_obj = TestObject()
    server = ObjectServer()
    server.register(test_obj)
    server.run(debug=True)