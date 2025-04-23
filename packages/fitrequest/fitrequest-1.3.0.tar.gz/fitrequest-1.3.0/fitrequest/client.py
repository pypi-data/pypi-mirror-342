from typing import ClassVar

from fitrequest.class_factory import ClassFactory
from fitrequest.client_base import FitRequestBase


# FitRequest Session initialized by the ClassFactory
class FitRequest(FitRequestBase, metaclass=ClassFactory):
    """
    This class serves as a configuration for declaring `fitrequest` methods,
    providing an alternative to directly using `FitConfig`.
    It allows you to use the `@fit` decorator to define these methods.
    Keep in mind that the attributes specified here (such as `auth`, `method_docstring`, and `method_config_list`) are
    solely for method generation purposes and are discarded by the `ClassFactory` during the final class generation.
    """

    auth: ClassVar[dict] = {}
    method_docstring: str = ''
    method_config_list: ClassVar[list[dict]] = []
