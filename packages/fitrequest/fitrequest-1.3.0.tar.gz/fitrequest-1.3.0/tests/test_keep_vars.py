from collections.abc import Callable
from functools import wraps
from typing import Any

from fitrequest.decorators import keep_vars


def basic_decorator(func) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)

    return wrapper


@keep_vars(basic_decorator)
def decorated_func() -> str:
    """This is a test function."""
    return 'hello'


decorated_func.custom_attr = 123
decorated_func.__annotations__ = {'return': str}


def test_preserves_name_doc_and_annotations():
    assert decorated_func.__name__ == 'decorated_func'
    assert decorated_func.__doc__ == 'This is a test function.'
    assert decorated_func.__annotations__ == {'return': str}


def test_preserves_custom_attributes():
    assert getattr(decorated_func, 'custom_attr', None) == 123


def test_keeps_return_value():
    assert decorated_func() == 'hello'


def test_works_with_staticmethod():
    class Foo:
        @keep_vars(basic_decorator)
        @staticmethod
        def static() -> str:
            return 'static'

    assert isinstance(Foo.__dict__['static'], staticmethod)
    assert Foo.static() == 'static'


def test_works_with_classmethod():
    class Foo:
        @keep_vars(basic_decorator)
        @classmethod
        def cls_method(cls) -> str:
            return cls.__name__

    assert isinstance(Foo.__dict__['cls_method'], classmethod)
    assert Foo.cls_method() == 'Foo'


def test_works_with_instancemethod():
    class Foo:
        @keep_vars(basic_decorator)
        def inst(self) -> str:
            return 'instance'

    f = Foo()
    assert f.inst() == 'instance'


def test_works_with_stack_of_decorators():
    def upper(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs).upper()

        return wrapper

    @keep_vars(upper)
    @keep_vars(basic_decorator)
    def shout() -> str:
        """yell it"""
        return 'quiet'

    shout.meta = True
    assert shout() == 'QUIET'
    assert shout.__doc__ == 'yell it'
    assert shout.meta is True


def test_without_wraps_loses_metadata():
    def bad_decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)

        return wrapper

    @keep_vars(bad_decorator)
    def test_func() -> bool:
        """Meta lost"""
        return True

    assert test_func.__doc__ == 'Meta lost'  # Still preserved by keep_vars
    assert test_func() is True


def test_static_classmethod_identity_not_lost():
    """
    Confirm that after decoration with keep_vars, the function is still recognized
    as staticmethod or classmethod in class dictionary (needed for correct binding).
    """

    class Bar:
        @keep_vars(basic_decorator)
        @staticmethod
        def stat() -> None:
            pass

        @keep_vars(basic_decorator)
        @classmethod
        def clsm(cls) -> None:
            pass

    assert isinstance(Bar.__dict__['stat'], staticmethod)
    assert isinstance(Bar.__dict__['clsm'], classmethod)


def test_function_dict_not_overwritten():
    def attr_decorator(func: Callable) -> Callable:
        f = wraps(func)(lambda *args, **kwargs: func(*args, **kwargs))
        f.new_attr = 99
        return f

    @keep_vars(attr_decorator)
    def f() -> None:
        pass

    f.my_own = 42
    assert f.new_attr == 99
    assert f.my_own == 42
