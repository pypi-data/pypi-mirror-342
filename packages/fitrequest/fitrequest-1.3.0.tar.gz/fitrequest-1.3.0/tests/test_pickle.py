import pickle
from typing import Any
from unittest.mock import patch

import httpx
import pytest
import respx
from joblib import Parallel, delayed

from fitrequest.fit_config import FitConfig
from tests.demo import (
    pickable_client_default,
    pickable_client_from_dict,
    pickable_client_from_json,
    pickable_client_from_yaml,
)
from tests.demo_custom_init_session import (
    client_default_custom_init_session,
    client_from_dict_custom_init_session,
    client_from_json_custom_init_session,
    client_from_yaml_custom_init_session,
    client_with_specific_args_custom_init_session,
)
from tests.demo_decorator import client_decorated
from tests.demo_lazy_config import client_lazy_config
from tests.demo_mix import client_mix
from tests.fixtures import ConfigWithBasicCredentials


class AuthenticatedClient(ConfigWithBasicCredentials().fit_class): ...


authenticated_client = AuthenticatedClient()


@pytest.mark.parametrize(
    'client',
    [
        pickable_client_default,
        pickable_client_from_json,
        pickable_client_from_yaml,
        pickable_client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
        authenticated_client,
        client_default_custom_init_session,
        client_from_dict_custom_init_session,
        client_from_json_custom_init_session,
        client_from_yaml_custom_init_session,
        client_with_specific_args_custom_init_session,
    ],
)
def test_pickle(client):
    data = pickle.dumps(client)
    restored_client = pickle.loads(data)  # noqa: S301

    assert restored_client.fit_config == client.fit_config
    assert restored_client.client_name == client.client_name
    assert restored_client.version == client.version
    assert restored_client.base_url == client.base_url
    assert vars(restored_client) == vars(client)

    for method_config in restored_client.fit_config['method_config_list']:
        assert hasattr(restored_client, method_config['name'])

    assert restored_client.session.raw_auth == client.session.raw_auth


@pytest.mark.parametrize(
    'client',
    [
        pickable_client_default,
        pickable_client_from_json,
        pickable_client_from_yaml,
        pickable_client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
        authenticated_client,
        client_default_custom_init_session,
        client_from_dict_custom_init_session,
        client_from_json_custom_init_session,
        client_from_yaml_custom_init_session,
        client_with_specific_args_custom_init_session,
    ],
)
def test_fit_config(client):
    assert client.fit_config == FitConfig.from_dict(**client.fit_config).fit_config


@pytest.mark.parametrize(
    'client',
    [
        pickable_client_default,
        pickable_client_from_json,
        pickable_client_from_yaml,
        pickable_client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
    ],
)
def test_parallel_call(client):
    nb_workers = 3

    def mock_call(item_id: int) -> dict:
        with respx.mock:
            expected = {'item_id': item_id, 'item_name': f'ball{item_id}'}
            respx.get(f'https://test.skillcorner.fr/items/{item_id}').mock(
                return_value=httpx.Response(200, json=expected)
            )
            return client.get_item(item_id)

    results = Parallel(n_jobs=-1)(delayed(mock_call)(item_id) for item_id in range(nb_workers))
    assert results == [{'item_id': item_id, 'item_name': f'ball{item_id}'} for item_id in range(nb_workers)]


@pytest.mark.parametrize(
    'client',
    [
        pickable_client_default,
        pickable_client_from_json,
        pickable_client_from_yaml,
        pickable_client_from_dict,
        client_lazy_config,
        client_decorated,
        client_mix,
    ],
)
def test_parallel_call_with_client_arg(client):
    nb_workers = 3

    def mock_call(client_arg: Any, item_id: int) -> dict:
        with respx.mock:
            expected = {'item_id': item_id, 'item_name': f'ball{item_id}'}
            respx.get(f'https://test.skillcorner.fr/items/{item_id}').mock(
                return_value=httpx.Response(200, json=expected)
            )
            return client_arg.get_item(item_id)

    results = Parallel(n_jobs=-1)(delayed(mock_call)(client, item_id) for item_id in range(nb_workers))
    assert results == [{'item_id': item_id, 'item_name': f'ball{item_id}'} for item_id in range(nb_workers)]
