from inspect import signature
from typing import Tuple, List

from flask import Flask, request


class ObjectServer:

    def __init__(self, name: str = None, filter_privates: bool = False):
        if name:
            self.application = Flask(name)
        else:
            self.application = Flask(__name__)
        self.objects = {}
        self.filter_privates = filter_privates

    def register(self, obj: object):
        self.objects[obj.__class__.__name__] = obj

    def _get_attributes(self, obj: object) -> List[str]:
        attributes = []
        for entry in dir(obj):
            if not callable(getattr(obj, entry)):
                if self.filter_privates:
                    if not self.is_private(entry):
                        attributes.append(entry)
                else:
                    attributes.append(entry)
        return attributes

    def _get_methods(self, obj: object) -> List[str]:
        methods = []
        for entry in dir(obj):
            if callable(getattr(obj, entry)):
                if self.filter_privates:
                    if not self.is_private(entry):
                        methods.append(entry)
                else:
                    methods.append(entry)
        return methods

    @staticmethod
    def is_private(method_name: str) -> bool:
        return method_name.startswith('_')

    @staticmethod
    def _get_method_signature(obj: object, method_name: str) -> str:
        # TODO return dict instead of string representation
        return str(signature(getattr(obj, method_name)))

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

        @self.application.route('/<obj_name>/<string:attribute_name>', methods=['GET', 'POST'])
        def get_attribute_or_method(obj_name: str, attribute_name: str) -> Tuple[dict, int]:
            # Universal validation
            try:
                obj = self.objects[obj_name]
            except KeyError:
                return {'response': 'Could not find object {}'.format(obj_name)}, 400
            if not getattr(obj, attribute_name):
                return {'response': 'Could not find attr {} for object {}'.format(attribute_name, obj_name)}, 400

            # GET requests are used to call attributes or methods with no params
            if request.method == 'GET':

                if attribute_name in self._get_methods(obj):
                    try:
                        response = getattr(obj, attribute_name)()
                    except Exception as e:
                        return {'response': str(e)}, 400
                else:
                    response = getattr(obj, attribute_name)

                try:
                    return {'response': response}, 200
                except TypeError:
                    return {'response': str(response)}, 200

            # POST requests are used for calling methods with params
            if request.method == 'POST':

                if attribute_name not in self._get_methods(obj):
                    return {'respsonse': '{} is not a method'}, 400
                args = request.json.get('args', [])
                kwargs = request.json.get('kwargs', {})

                try:
                    response = getattr(obj, attribute_name)(*args, **kwargs)
                except Exception as e:
                    return {'response': str(e)}, 400

                try:
                    return {'response': response}, 200
                except TypeError:
                    return {'response': str(response)}, 200

        @self.application.route('/<obj_name>/<string:method_name>/signature')
        def get_method_signature(obj_name, method_name):
            try:
                obj = self.objects[obj_name]
            except KeyError:
                return {'response': 'Could not find object {}'.format(obj_name)}, 400
            if method_name not in self._get_methods(obj):
                return {'response': 'Object {} has no method {}'.format(obj_name, method_name)}, 400
            return {'response': self._get_method_signature(obj, method_name)}, 200

    def run(self, *args, **kwargs):
        self._register_routes()
        self.application.run(*args, **kwargs)
