from collections.abc import Callable
from functools import cached_property
from pathlib import Path

import yaml
from pydantic import ConfigDict

from fitrequest.client_base import FitRequestBase
from fitrequest.generator import Generator
from fitrequest.method_config import MethodConfig
from fitrequest.method_config_group import MethodConfigGroup
from fitrequest.session import Session


class FitConfig(MethodConfigGroup):
    """
    Fitrequest configuration model.
    Describes all information needed to generate Fitrequest's class and methods.
    """

    class_name: str = 'FitRequest'
    """Name of the the generated class."""

    class_docstring: str = ''
    """Docstring of the generated class."""

    model_config = ConfigDict(extra='forbid', validate_default=True)

    @cached_property
    def session(self) -> Session:
        return Session(
            client_name=self.client_name,
            version=self.version,
            auth=self.auth,
        )

    @cached_property
    def fit_methods(self) -> dict[str, Callable]:
        """Returns FitConfig generated methods."""
        return {
            method_config.name: Generator.generate_method(self.session, method_config)
            for method_config in self.method_config_list
            if isinstance(method_config, MethodConfig)
        }

    @cached_property
    def fit_class(self) -> type:
        """Create new class from FitConfig."""

        # Expose the configuration used to create the `fit_request` methods.
        fit_config = self.model_dump(exclude_none=True)
        fit_config['method_config_list'] = sorted(fit_config['method_config_list'], key=lambda x: x['name'])

        fit_attrs = self.fit_methods | {
            'client_name': self.client_name,
            'version': self.version,
            'base_url': str(self.base_url),
            'fit_config': fit_config,
            'session': self.session,
        }
        new_class = type(self.class_name, (FitRequestBase,), fit_attrs)
        new_class.__doc__ = self.class_docstring

        return new_class

    @classmethod
    def from_json(cls, json_path: Path | str) -> type:
        """Generate a ``fitrequest`` class from a ``json`` file."""
        with open(str(json_path), encoding='utf-8') as json_file:
            return cls.model_validate_json(json_file.read()).fit_class

    @classmethod
    def from_yaml(cls, yaml_path: Path | str) -> type:
        """Generate a ``fitrequest`` class from a ``yaml`` file."""
        with open(str(yaml_path), encoding='utf-8') as yaml_file:
            return cls.model_validate(yaml.safe_load(yaml_file)).fit_class

    @classmethod
    def from_dict(cls, **kwargs) -> type:
        """Generate a ``fitrequest`` class from a keyword arguments."""
        return cls(**kwargs).fit_class
