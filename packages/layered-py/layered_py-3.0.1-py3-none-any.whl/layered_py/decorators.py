import inspect
from functools import wraps
from inspect import isclass
from .di import Container

container = Container()

def register(key=None, singleton=False):
    def wrapper(provider):
        reg_key = key or provider.__name__
        if isclass(provider):
            container.register(reg_key, lambda: provider(), singleton=singleton)
        else:
            container.register(reg_key, provider, singleton=singleton)
        return provider
    return wrapper

def inject(func):
    sig = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind_partial(*args, **kwargs)

        for name, param in sig.parameters.items():
            if name not in bound.arguments:
                if param.annotation != inspect.Parameter.empty:
                    try:
                        kwargs[name] = container.resolve(param.annotation.__name__)
                    except KeyError:
                        pass
                if name not in kwargs:
                    kwargs[name] = container.resolve(name)
        return func(*args, **kwargs)
    return wrapper