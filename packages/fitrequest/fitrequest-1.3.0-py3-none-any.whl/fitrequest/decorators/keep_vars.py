from collections.abc import Callable
from functools import update_wrapper


def keep_vars(decorator: Callable) -> Callable:
    """
    A decorator for decorators that ensures the original function's metadata
    and custom attributes are preserved after decoration.

    This decorator is compatible with instance methods, static methods, and class methods.

    **Example:**

    .. code-block:: python

       def my_decorator(func):
           @wraps(func)
           def wrapped(*args, **kwargs):
               print("Running!")
               return func(*args, **kwargs)
           return wrapped

       @keep_vars(my_decorator)
       def greet():
           '''Say hello'''
           pass

       greet.custom_flag = True
       assert greet.__doc__ == "Say hello"
       assert greet.custom_flag is True

    .. note::

        - This uses :func:`functools.update_wrapper` for metadata preservation.
        - It also copies custom attributes from the original function using ``vars()``.
        - For static and class methods, it unwraps the function before decoration
          and rewraps it after.

    """

    def wrapper(func: Callable) -> Callable:
        original_func = func
        method_type = None

        # Unwrap staticmethod or classmethod
        if isinstance(func, staticmethod):
            original_func = func.__func__
            method_type = staticmethod
        elif isinstance(func, classmethod):
            original_func = func.__func__
            method_type = classmethod

        decorated_func = decorator(original_func)

        if decorated_func is original_func:
            return decorated_func

        update_wrapper(decorated_func, original_func)

        for attr_name, attr_val in vars(original_func).items():
            setattr(decorated_func, attr_name, attr_val)

        # Re-wrap in original method type if needed
        if method_type:
            decorated_func = method_type(decorated_func)

        return decorated_func

    return wrapper
