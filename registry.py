# transformer_registry.py


class TransformerRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, name):
        def wrapper(func):
            self._registry[name] = func
            return func
        return wrapper

    def get(self, name):
        return self._registry.get(name)
    
    def available_transformers(self):
        return self._registry


registry = TransformerRegistry()
