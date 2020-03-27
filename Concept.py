from flask import Flask


class Server:

    def __init__(self):
        self.application = Flask(__name__)
        self.object_store = {}

    def flaskify(self, obj):
        self.object_store[object.__class__.__name__] = obj

    def run(self, *args, **kwargs):
        @self.application.route('/<object_name>/<attribute_name>')
        def get(object_name, attribute_name):
            obj = self.object_store[object_name]
            if callable(getattr(obj, attribute_name)):
                return getattr(obj, attribute_name)()
            else:
                return getattr(obj, attribute_name)
        self.application.run(*args, **kwargs)


class TestObject:

    def __init__(self, t="Foo"):
        self.t = t

    def test(self):
        return 'Bar'


if __name__ == '__main__':
    test_obj = TestObject()
    server = Server()
    server.flaskify(test_obj)
    server.run(debug=True)