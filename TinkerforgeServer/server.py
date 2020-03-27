from flask import Flask


class Server:

    def __init__(self):
        self.application = Flask(__name__)
        self.object_store = {}

    def add(self, obj):
        self.object_store[obj.__class__.__name__] = obj

    def _register_routes(self):
        @self.application.route('/')
        def get_objects():
            return {'objects': list(self.object_store.keys())}, 200


        @self.application.route('/<object_name>')
        def get_object(object_name):
            try:
                obj = self.object_store[object_name]
            except KeyError:
                return {'msg': f'Could not find object {object_name}'}, 400
            return {obj.__class__.__name__: dir(obj)}, 200

        @self.application.route('/<object_name>/<attribute_name>')
        def get_attribute(object_name, attribute_name):
            try:
                obj = self.object_store[object_name]
            except KeyError:
                return {'msg': f'Could not find object {object_name}'}, 400
            if not getattr(obj, attribute_name):
                return {'msg': f'Could not find attr {attribute_name} for object {object_name}'}, 400
            if callable(getattr(obj, attribute_name)):
                return getattr(obj, attribute_name)(), 200
            else:
                return getattr(obj, attribute_name), 200

    def run(self, *args, **kwargs):
        self._register_routes()
        self.application.run(*args, **kwargs)