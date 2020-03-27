from flask import Flask
from flask import jsonify
from typing import Tuple, List


class ObjectServer:

    def __init__(self):
        self.application = Flask(__name__)
        self.objects = {}

    def add(self, obj: object):
        self.objects[obj.__class__.__name__] = obj

    def _get_attributes(self, obj: object) -> List[str]:
        attributes = []
        for entry in dir(obj):
            if not callable((getattr(obj, entry))):
                attributes.append(entry)
        return attributes

    def _get_methods(self, obj: object) -> List[str]:
        methods = []
        for entry in dir(obj):
            if callable((getattr(obj, entry))):
                methods.append(entry)
        return methods

    def _register_routes(self):
        @self.application.route('/')
        def get_objects() -> Tuple[dict, int]:
            return {'response': list(self.objects.keys())}, 200

        @self.application.route('/<string:object_name>')
        def get_object(object_name: str) -> Tuple[dict, int]:
            try:
                obj = self.objects[object_name]
                attributes = self._get_attributes(obj)
                methods = self._get_methods(obj)
                return {obj.__class__.__name__: {'attributes': attributes, 'methods': methods}}, 200
            except KeyError:
                return {'response': 'Could not find object {}'.format(object_name)}, 400


        @self.application.route('/<string:object_name>/<string:attribute_name>')
        def get_attribute(object_name: str, attribute_name: str) -> Tuple[dict, int]:
            try:
                obj = self.objects[object_name]
            except KeyError:
                return {'response': 'Could not find object {}'.format(object_name)}, 400
            if not getattr(obj, attribute_name):
                return {'response': 'Could not find attr {} for object {}'.format(attribute_name, object_name)}, 400
            if callable(getattr(obj, attribute_name)):
                response = getattr(obj, attribute_name)()
            else:
                response = getattr(obj, attribute_name)
            try:
                return {'response': response}, 200
            except TypeError:
                return {'response': str(response)}, 200

    def run(self, *args, **kwargs):
        self._register_routes()
        self.application.run(*args, **kwargs)