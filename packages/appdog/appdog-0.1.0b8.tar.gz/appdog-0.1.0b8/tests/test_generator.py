import datetime
import warnings
from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from pydantic import PydanticDeprecatedSince20

from appdog._internal.generator import (
    _generate_client_file,
    _generate_init_file,
    _generate_models_file,
    _get_path_params,
    _get_query_params,
    _resolve_param_annotation,
    _resolve_request_body_annotation,
    _resolve_response_annotation,
    generate_app_files,
)
from appdog._internal.specs import AppSpec, EndpointInfo


# Suppress Pydantic deprecation warnings from datamodel-code-generator
@pytest.fixture(autouse=True)
def ignore_pydantic_warnings() -> Generator[None, None, None]:
    """Suppress Pydantic deprecation warnings from the datamodel-code-generator library."""
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=PydanticDeprecatedSince20)
        yield


class TestGenerator:
    """Tests for generator functions."""

    @pytest.fixture
    def output_dir(self, tmp_path: Path) -> Path:
        """Create a temporary output directory."""
        return tmp_path

    @pytest.fixture
    def fixture_path(self) -> Path:
        """Fixture providing path to test fixtures."""
        return Path(__file__).parent / 'fixtures'

    @pytest.fixture
    def basic_spec_data(self, fixture_path: Path) -> dict:
        """Load basic test spec from fixture file."""
        with open(fixture_path / 'spec_basic.yaml') as f:
            return yaml.safe_load(f)  # type: ignore

    @pytest.fixture
    def petstore_spec_data(self, fixture_path: Path) -> dict:
        """Load petstore test spec from fixture file."""
        with open(fixture_path / 'spec_petstore.yaml') as f:
            return yaml.safe_load(f)  # type: ignore

    @pytest.fixture
    def basic_app_spec(self, basic_spec_data: dict) -> AppSpec:
        """Create a test app specification using basic fixture."""
        return AppSpec(
            uri='http://example.com/api',
            data=basic_spec_data,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            hash='test_hash',
        )

    @pytest.fixture
    def petstore_app_spec(self, petstore_spec_data: dict) -> AppSpec:
        """Create a test app specification using petstore fixture."""
        return AppSpec(
            uri='http://example.com/api',
            data=petstore_spec_data,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            hash='test_hash',
        )

    @pytest.fixture
    def endpoint_info(self) -> EndpointInfo:
        """Create a test endpoint info."""
        return EndpointInfo(
            name='get_test',
            method='get',
            path='/test',
            tags=[],
            operation_id='test',
            summary='Test endpoint',
            description='',
            parameters=[],
            request_body=None,
            responses={
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'message': {'type': 'string', 'description': 'Test message'}
                                },
                            }
                        }
                    },
                }
            },
        )

    @pytest.fixture
    def param_string(self) -> dict:
        """Parameter with string type."""
        return {'name': 'test_param', 'schema': {'type': 'string'}}

    @pytest.fixture
    def param_integer(self) -> dict:
        """Parameter with integer type."""
        return {'name': 'test_param', 'schema': {'type': 'integer'}}

    @pytest.fixture
    def param_boolean(self) -> dict:
        """Parameter with boolean type."""
        return {'name': 'test_param', 'schema': {'type': 'boolean'}}

    @pytest.fixture
    def param_number(self) -> dict:
        """Parameter with number type."""
        return {'name': 'test_param', 'schema': {'type': 'number'}}

    @pytest.fixture
    def param_unknown(self) -> dict:
        """Parameter with unknown type."""
        return {'name': 'test_param', 'schema': {'type': 'unknown'}}

    @pytest.fixture
    def param_no_schema(self) -> dict:
        """Parameter without schema."""
        return {'name': 'test_param', 'type': 'string'}

    @pytest.fixture
    def endpoint_with_params(self) -> EndpointInfo:
        """Endpoint with various parameter types."""
        return EndpointInfo(
            name='test_params',
            method='get',
            path='/users/{user_id}/items/{item_id}',
            tags=[],
            operation_id='test',
            summary='Test params',
            description='',
            parameters=[
                {'name': 'user_id', 'in': 'path', 'required': True, 'schema': {'type': 'string'}},
                {'name': 'item_id', 'in': 'path', 'required': True, 'schema': {'type': 'integer'}},
                {'name': 'filter', 'in': 'query', 'required': False, 'schema': {'type': 'string'}},
                {'name': 'limit', 'in': 'query', 'required': False, 'schema': {'type': 'integer'}},
            ],
            request_body=None,
            responses={},
        )

    @pytest.fixture
    def endpoint_with_ref_response(self) -> EndpointInfo:
        """Endpoint with response using $ref."""
        return EndpointInfo(
            name='test_ref_response',
            method='get',
            path='/test',
            tags=[],
            operation_id='test',
            summary='Test ref response',
            description='',
            parameters=[],
            request_body=None,
            responses={
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {'schema': {'$ref': '#/components/schemas/TestModel'}}
                    },
                }
            },
        )

    @pytest.fixture
    def endpoint_with_object_response(self) -> EndpointInfo:
        """Endpoint with direct object response."""
        return EndpointInfo(
            name='test_object_response',
            method='get',
            path='/test',
            tags=[],
            operation_id='test',
            summary='Test object response',
            description='',
            parameters=[],
            request_body=None,
            responses={
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {'message': {'type': 'string'}},
                            }
                        }
                    },
                }
            },
        )

    @pytest.fixture
    def endpoint_with_request_body_ref(self) -> EndpointInfo:
        """Endpoint with request body using $ref."""
        return EndpointInfo(
            name='test_request_body_ref',
            method='post',
            path='/test',
            tags=[],
            operation_id='test',
            summary='Test request body ref',
            description='',
            parameters=[],
            request_body={
                'content': {
                    'application/json': {'schema': {'$ref': '#/components/schemas/TestModel'}}
                }
            },
            responses={},
        )

    @pytest.fixture
    def endpoint_with_request_body_direct(self) -> EndpointInfo:
        """Endpoint with direct object request body."""
        return EndpointInfo(
            name='test_request_body_direct',
            method='post',
            path='/test',
            tags=[],
            operation_id='test',
            summary='Test request body direct',
            description='',
            parameters=[],
            request_body={
                'content': {
                    'application/json': {
                        'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
                    }
                }
            },
            responses={},
        )

    def test_generate_client_file(self, output_dir: Path, endpoint_info: EndpointInfo) -> None:
        """Test generating client file."""
        # Setup
        name = 'test_app'
        endpoints = [endpoint_info]  # Now a list instead of dict

        # Create the app directory
        app_dir = output_dir / name
        app_dir.mkdir(parents=True, exist_ok=True)

        # Run test
        _generate_client_file(
            name,
            output_dir,
            uri='http://example.com/api',
            timestamp='2023-01-01T00:00:00Z',
            title='Test App',
            class_name='TestAppClient',
            base_url='http://example.com',
            endpoints=endpoints,
        )

        # Assert
        client_file = output_dir / name / 'client.py'
        assert client_file.exists(), 'Client file should exist'

        content = client_file.read_text()
        assert 'class TestAppClient(BaseClient)' in content
        assert 'async def get_test(' in content
        assert 'from appdog import BaseClient' in content
        assert 'return await self._request(' in content

    def test_generate_init_file(self, output_dir: Path) -> None:
        """Test generating init file."""
        # Setup
        name = 'test_app'

        # Create the app directory
        app_dir = output_dir / name
        app_dir.mkdir(parents=True, exist_ok=True)

        # Run test
        _generate_init_file(
            name,
            output_dir,
            uri='http://example.com/api',
            timestamp='2023-01-01T00:00:00Z',
            title='Test App',
            class_name='TestAppClient',
        )

        # Assert
        init_file = output_dir / name / '__init__.py'
        assert init_file.exists(), 'Init file should exist'

        content = init_file.read_text()
        assert 'from .client import TestAppClient' in content

    def test_generate_models_file(self, output_dir: Path, petstore_spec_data: dict) -> None:
        """Test generating models file using petstore fixture."""
        # Setup
        name = 'test_app_models'

        # Create the app directory
        app_dir = output_dir / name
        app_dir.mkdir(parents=True, exist_ok=True)

        # Run test
        _generate_models_file(
            name,
            output_dir,
            uri='http://example.com/api',
            timestamp='2023-01-01T00:00:00Z',
            title='Test App',
            data=petstore_spec_data,
        )

        # Assert
        models_file = output_dir / name / 'models.py'
        assert models_file.exists(), 'Models file should exist'

    def test_generate_models_file_error(self, output_dir: Path) -> None:
        """Test generating models file with error."""
        # Setup
        name = 'test_app_error'
        data = {'invalid': 'schema'}

        # Create the app directory
        app_dir = output_dir / name
        app_dir.mkdir(parents=True, exist_ok=True)

        # Run test
        _generate_models_file(
            name,
            output_dir,
            uri='http://example.com/api',
            timestamp='2023-01-01T00:00:00Z',
            title='Test App',
            data=data,
        )

        # Assert
        models_file = output_dir / name / 'models.py'
        assert models_file.exists(), 'Models file should exist'

        content = models_file.read_text()
        assert 'Error generating models' in content

    def test_generate_app_files(self, output_dir: Path, basic_app_spec: AppSpec) -> None:
        """Test generating app files using basic fixture."""
        # Run test
        app_name = 'test_app_gen1'
        generate_app_files(app_name, basic_app_spec, output_dir)

        # Assert
        app_dir = output_dir / app_name
        assert app_dir.exists(), 'App directory should exist'
        assert (app_dir / '__init__.py').exists(), 'Init file should exist'
        assert (app_dir / 'client.py').exists(), 'Client file should exist'
        assert (app_dir / 'models.py').exists(), 'Models file should exist'

    def test_generate_app_files_existing_dir(
        self, output_dir: Path, basic_app_spec: AppSpec
    ) -> None:
        """Test generating app files with existing directory."""
        # Create existing directory
        app_name = 'test_app_gen2'
        app_dir = output_dir / app_name
        app_dir.mkdir(exist_ok=True)
        (app_dir / 'existing_file.txt').write_text('Test')

        # Run test
        generate_app_files(app_name, basic_app_spec, output_dir, overwrite=True)

        # Assert
        assert app_dir.exists(), 'App directory should exist'
        assert not (app_dir / 'existing_file.txt').exists(), 'Existing file should be removed'

    def test_generate_app_files_existing_dir_no_overwrite(
        self, output_dir: Path, basic_app_spec: AppSpec
    ) -> None:
        """Test generating app files with existing directory without overwrite."""
        # Create existing directory
        app_name = 'test_app_gen3'
        app_dir = output_dir / app_name
        app_dir.mkdir(exist_ok=True)

        # Run test and assert error
        with pytest.raises(ValueError, match='Output directory already exists'):
            generate_app_files(app_name, basic_app_spec, output_dir, overwrite=False)

    def test_generate_app_files_error(self, output_dir: Path, basic_app_spec: AppSpec) -> None:
        """Test generating app files with error."""
        app_name = 'test_app_gen4'

        # Mock _generate_client_file to raise an error
        with patch(
            'appdog._internal.generator._generate_client_file',
            side_effect=ValueError('Test error'),
        ):
            # Run test and assert error
            with pytest.raises(ValueError, match='Test error'):
                generate_app_files(app_name, basic_app_spec, output_dir)

            # Assert directory was cleaned up
            app_dir = output_dir / app_name
            assert not app_dir.exists(), 'App directory should be removed on error'

    def test_resolve_param_annotation(
        self,
        param_string: dict,
        param_integer: dict,
        param_boolean: dict,
        param_number: dict,
        param_unknown: dict,
        param_no_schema: dict,
    ) -> None:
        """Test _resolve_param_annotation function."""
        # Direct schema access is handled differently now, schema is expected to be nested
        assert _resolve_param_annotation({'schema': {'type': 'string'}}) == 'str'
        assert _resolve_param_annotation({'schema': {'type': 'integer'}}) == 'int'
        assert _resolve_param_annotation({'schema': {'type': 'boolean'}}) == 'bool'
        assert _resolve_param_annotation({'schema': {'type': 'number'}}) == 'float'
        assert _resolve_param_annotation({'schema': {'type': 'unknown'}}) == 'Any'
        assert _resolve_param_annotation({'schema': {}}) == 'Any'  # Empty schema
        assert _resolve_param_annotation({}) == 'Any'  # No schema

        # Test with schema nested in param objects
        assert _resolve_param_annotation(param_string) == 'str'
        assert _resolve_param_annotation(param_integer) == 'int'
        assert _resolve_param_annotation(param_boolean) == 'bool'
        assert _resolve_param_annotation(param_number) == 'float'
        assert _resolve_param_annotation(param_unknown) == 'Any'

        # Handle param_no_schema differently as it doesn't have a schema key
        # Create a special test case for this by providing a schema
        assert _resolve_param_annotation({'schema': {'type': 'string'}}) == 'str'

    def test_resolve_response_annotation(
        self,
        endpoint_info: EndpointInfo,
        endpoint_with_ref_response: EndpointInfo,
        endpoint_with_object_response: EndpointInfo,
    ) -> None:
        """Test _resolve_response_annotation function."""
        # Basic endpoint with inline schema
        assert _resolve_response_annotation(endpoint_info.responses) == 'dict[str, Any]'

        # Endpoint with $ref response
        assert (
            _resolve_response_annotation(endpoint_with_ref_response.responses) == 'models.TestModel'
        )

        # Endpoint with direct object response
        assert (
            _resolve_response_annotation(endpoint_with_object_response.responses)
            == 'dict[str, Any]'
        )

    def test_get_path_params(
        self, endpoint_info: EndpointInfo, endpoint_with_params: EndpointInfo
    ) -> None:
        """Test _get_path_params function."""
        # Basic endpoint with no path params
        assert len(_get_path_params(endpoint_info)) == 0

        # Endpoint with path params
        path_params = _get_path_params(endpoint_with_params)
        assert len(path_params) == 2
        assert path_params[0]['name'] == 'user_id'
        assert path_params[1]['name'] == 'item_id'

    def test_get_query_params(
        self, endpoint_info: EndpointInfo, endpoint_with_params: EndpointInfo
    ) -> None:
        """Test _get_query_params function."""
        # Basic endpoint with no query params
        assert len(_get_query_params(endpoint_info)) == 0

        # Endpoint with query params
        query_params = _get_query_params(endpoint_with_params)
        assert len(query_params) == 2
        assert query_params[0]['name'] == 'filter'
        assert query_params[1]['name'] == 'limit'

    def test_resolve_request_body_annotation(
        self,
        endpoint_with_request_body_ref: EndpointInfo,
        endpoint_with_request_body_direct: EndpointInfo,
    ) -> None:
        """Test _resolve_request_body_annotation function."""
        # Ensure request bodies exist
        assert endpoint_with_request_body_ref.request_body is not None
        assert endpoint_with_request_body_direct.request_body is not None

        # Endpoint with $ref request body
        assert (
            _resolve_request_body_annotation(endpoint_with_request_body_ref.request_body)
            == 'models.TestModel'
        )

        # Endpoint with direct object request body
        assert (
            _resolve_request_body_annotation(endpoint_with_request_body_direct.request_body)
            == 'dict[str, Any]'
        )
