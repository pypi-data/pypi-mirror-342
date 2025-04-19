import json
import shutil
import traceback
from pathlib import Path
from typing import Any

from datamodel_code_generator import DataModelType, InputFileType, PythonVersion, generate
from jinja2 import Environment, FileSystemLoader

from .case import to_pascal_case, to_snake_case, to_title_case
from .logging import logger
from .schema import json_schema_to_annotation
from .specs import AppSpec, EndpointInfo
from .utils import get_source_dir, get_timestamp

SCHEMA_TYPE_MAPPING: dict[str, str] = {
    'null': 'None',
    'boolean': 'bool',
    'integer': 'int',
    'number': 'float',
    'string': 'str',
}
"""Mapping of OpenAPI schema types to Python types."""

TEMPLATES_DIR = get_source_dir() / '_internal' / 'templates'
"""Path to the templates directory."""

TEMPLATES_ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=False)  # noqa: S701
"""Jinja2 environment for rendering templates."""


def generate_mcp_file(
    output: Path,
    *,
    project_dir: Path | str | None,
    registry_dir: Path | str | None,
    server_name: str,
    overwrite: bool = False,
) -> None:
    """Generate an MCP server file.

    Args:
        output: Path to the output file.
        project_dir: Path to the project directory.
        registry_dir: Path to the registry directory.
        server_name: Name of the MCP server.
        overwrite: Whether to overwrite the output file if it exists.
    """
    logger.debug(f'Generating MCP server file to {output}')
    timestamp = get_timestamp()

    # Handle output
    if output.exists() and not overwrite:
        raise ValueError(f'Output path already exists: {output}')

    # Handle project directory
    project_dir = Path(project_dir) if project_dir else Path.cwd()
    registry_dir = Path(registry_dir) if registry_dir else get_source_dir()

    # Generate files
    template = TEMPLATES_ENV.get_template('server.j2')
    content = template.render(
        timestamp=timestamp,
        project_dir=project_dir.as_posix(),
        registry_dir=registry_dir.as_posix(),
        server_name=server_name,
    )
    content += '\n'
    output.write_text(content)

    logger.debug(f'Successfully generated MCP server file to {output}')


def generate_app_files(
    name: str,
    spec: AppSpec,
    base_dir: Path,
    *,
    overwrite: bool = False,
) -> None:
    """Generate files for the given application specification."""
    logger.debug(f'Generating files for {name!r}')
    timestamp = get_timestamp()

    # Handle output
    output_dir = base_dir / name
    if output_dir.exists() and not overwrite:
        raise ValueError(f'Output directory already exists: {output_dir}')
    shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Resolve template variables
    title = to_title_case(name)
    class_name = f'{to_pascal_case(name)}Client'

    # Generate files
    try:
        _generate_init_file(
            name,
            base_dir,
            uri=spec.uri,
            timestamp=timestamp,
            title=title,
            class_name=class_name,
        )

        _generate_client_file(
            name,
            base_dir,
            uri=spec.uri,
            timestamp=timestamp,
            title=title,
            class_name=class_name,
            base_url=spec.uri.rpartition('/')[0],
            endpoints=spec.lookup(),
        )

        _generate_models_file(
            name,
            base_dir,
            uri=spec.uri,
            timestamp=timestamp,
            title=title,
            data=spec.data,
        )

        logger.debug(f'Successfully generated files for {name!r}')

    except Exception as e:
        shutil.rmtree(output_dir, ignore_errors=True)
        raise e


def _generate_client_file(
    name: str,
    base_dir: Path,
    *,
    uri: str,
    timestamp: str,
    title: str,
    class_name: str,
    base_url: str,
    endpoints: list[EndpointInfo],
) -> None:
    """Generate client file."""
    logger.debug(f'Generating client file for {name!r}')
    output = base_dir / name / 'client.py'
    template = TEMPLATES_ENV.get_template('client.j2')
    content = template.render(
        name=name,
        uri=uri,
        timestamp=timestamp,
        title=title,
        class_name=class_name,
        endpoints=endpoints,
        base_url=base_url,
        get_path_params=_get_path_params,
        get_query_params=_get_query_params,
        resolve_param_annotation=_resolve_param_annotation,
        resolve_request_body_annotation=_resolve_request_body_annotation,
        resolve_response_annotation=_resolve_response_annotation,
        to_snake_case=to_snake_case,
    )
    content += '\n'
    output.write_text(content)


def _generate_init_file(
    name: str,
    base_dir: Path,
    *,
    uri: str,
    timestamp: str,
    title: str,
    class_name: str,
) -> None:
    """Generate init file."""
    logger.debug(f'Generating init file for {name!r}')
    output = base_dir / name / '__init__.py'
    template = TEMPLATES_ENV.get_template('__init__.j2')
    content = template.render(
        uri=uri,
        timestamp=timestamp,
        title=title,
        class_name=class_name,
    )
    content += '\n'
    output.write_text(content)


def _generate_models_file(
    name: str,
    base_dir: Path,
    *,
    uri: str,
    timestamp: str,
    title: str,
    data: dict[str, Any],
) -> None:
    """Generate models file using datamodel-code-generator."""
    logger.debug(f'Generating models file for {name!r}')
    output = base_dir / name / 'models.py'

    try:
        # Render models file header template
        template = TEMPLATES_ENV.get_template('models.j2')
        header = template.render(uri=uri, timestamp=timestamp, title=title)

        # Generate models using datamodel-code-generator
        generate(
            input_=json.dumps(data),
            input_file_type=InputFileType.OpenAPI,
            output=output,
            output_model_type=DataModelType.PydanticV2BaseModel,
            target_python_version=PythonVersion.PY_310,
            disable_appending_item_suffix=True,
            field_constraints=True,
            strict_nullable=True,
            use_annotated=True,
            use_schema_description=True,
            use_standard_collections=True,
            use_union_operator=True,
            custom_file_header=header,
        )

    except Exception as e:  # noqa: BLE001
        error = f'{e}\n{traceback.format_exc()}'
        logger.error(f'Error generating models file for {name!r}: {error}')
        template = TEMPLATES_ENV.get_template('models_error.j2')
        content = template.render(
            uri=uri,
            timestamp=timestamp,
            title=title,
            error=error,
        )
        content += '\n'
        output.write_text(content)


def _get_path_params(endpoint: EndpointInfo) -> list[dict[str, Any]]:
    """Get path parameters for the endpoint."""
    return [p for p in endpoint.parameters if p.get('in') == 'path']


def _get_query_params(endpoint: EndpointInfo) -> list[dict[str, Any]]:
    """Get query parameters for the endpoint."""
    return [p for p in endpoint.parameters if p.get('in') == 'query']


def _resolve_param_annotation(schema: dict[str, Any]) -> str:
    """Resolve parameter annotation from the provided OpenAPI schema."""
    definition = schema.get('schema', {})
    return json_schema_to_annotation(definition)


def _resolve_request_body_annotation(schema: dict[str, Any]) -> str:
    """Resolve request body annotation from the provided OpenAPI schema."""
    content = schema.get('content', {})
    definition = content.get('application/json', {}).get('schema', {})
    return json_schema_to_annotation(definition)


def _resolve_response_annotation(schema: dict[str, Any]) -> str:
    """Resolve response annotation from the provided OpenAPI schema."""
    content = schema.get('200', {}).get('content', {})
    definition = content.get('application/json', {}).get('schema', {})
    return json_schema_to_annotation(definition)
