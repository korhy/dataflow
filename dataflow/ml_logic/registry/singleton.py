from abc import ABCMeta

class SingletonMeta(type):
    """A metaclass that creates a Singleton base class when called."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # Create a key based on class and critical parameters
        # For example, for LocalModelRegistry, we want different instances for different storage directories
        key = (cls,)
        if args:
            key += args
        if kwargs:
            # Sort kwargs for consistent key generation
            key += tuple(sorted(kwargs.items()))

        if key not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[key] = instance
        return cls._instances[key]


class SingletonABCMeta(ABCMeta, SingletonMeta):
    """A metaclass that combines ABC and Singleton functionality."""
    pass
