from flask import Flask
from TinkerforgeServer import Server


class TestObject:

    def __init__(self, t="Foo"):
        self.t = t

    def test(self):
        return 'Bar'


if __name__ == '__main__':
    test_obj = TestObject()
    server = Server()
    server.add(test_obj)
    server.run(debug=True)