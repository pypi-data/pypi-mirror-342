from typing import Any

SCHEMA_TYPE_MAPPING = {
    'string': 'str',
    'number': 'float',
    'integer': 'int',
    'boolean': 'bool',
}
"""Mapping of OpenAPI JSON schema primitive types to Python types."""


def json_schema_to_annotation(schema: dict[str, Any], *, models_module: str = 'models') -> str:
    """Convert an OpenAPI JSON schema type definition to a Python annotation string representation.

    Args:
        schema: The OpenAPI JSON schema
        models_module: The name of the module where referenced models are defined

    Returns:
        A Python annotation string representation of the provided OpenAPI schema type definition
    """
    annotation = _resolve_annotation(schema, models_module)
    metadata = _collect_metadata(schema)
    if metadata:
        return f'Annotated[{annotation}, Field({", ".join(metadata)})]'
    else:
        return annotation


def _resolve_annotation(schema: dict[str, Any], models_module: str) -> str:  # noqa: C901
    """Resolve annotation from the provided OpenAPI schema."""
    # Handle empty schema
    if not schema:
        return 'Any'

    # Handle const annotation
    if 'const' in schema:
        annotation = _handle_const_annotation(schema)

    # Handle enum annotation
    elif 'enum' in schema:
        annotation = _handle_enum_annotation(schema)

    # Handle type annotation
    elif 'type' in schema:
        annotation = _handle_type_annotation(schema, models_module)

    # Handle composite annotations
    elif any(composite in schema for composite in ['allOf', 'anyOf', 'oneOf']):
        for composite in ['allOf', 'anyOf', 'oneOf']:
            if composite in schema:
                break
        annotation = _handle_composite_annotation(schema, composite, models_module)

    # Handle reference annotation
    elif '$ref' in schema:
        annotation = _handle_reference_annotation(schema, models_module)

    # Fallback to Any
    else:
        annotation = 'Any'

    # Handle nullable annotation
    if schema.get('nullable', False):
        annotation = f'{annotation} | None'

    return annotation


def _handle_composite_annotation(schema: dict[str, Any], composite: str, models_module: str) -> str:
    """Handle composite annotation formatting (allOf, anyOf, oneOf)."""
    annotations = []
    for value in schema[composite]:
        annotation = json_schema_to_annotation(value, models_module=models_module)
        if annotation not in annotations:
            annotations.append(annotation)
    if len(annotations) == 0:
        return 'Any'
    if len(annotations) == 1:
        return annotations[0]
    return ' | '.join(annotations)


def _handle_const_annotation(schema: dict[str, Any]) -> str:
    """Handle const annotation formatting."""
    value = schema['const']
    if isinstance(value, str):
        return f"Literal['{value}']"
    else:
        return f'Literal[{value}]'


def _handle_enum_annotation(schema: dict[str, Any]) -> str:
    """Handle enum annotation formatting."""
    formatted = []
    for value in schema['enum']:
        if isinstance(value, str):
            formatted.append(f"'{value}'")
        else:
            formatted.append(str(value))
    if formatted:
        return f'Literal[{", ".join(formatted)}]'
    return 'Any'


def _handle_reference_annotation(schema: dict[str, Any], models_module: str) -> str:
    """Handle reference annotation formatting."""
    value = schema['$ref'].split('/')[-1]
    return f'{models_module}.{value}'


def _handle_type_annotation(schema: dict[str, Any], models_module: str) -> str:
    """Handle type annotation formatting."""
    value = schema['type']
    # Handle array annotation
    if value == 'array':
        items = schema.get('items', {})
        annotation = json_schema_to_annotation(items, models_module=models_module)
        return f'list[{annotation}]'
    # Handle simple object annotation
    if value == 'object':
        additional_props = schema.get('additionalProperties', {})
        if additional_props and not isinstance(additional_props, bool):
            annotation = json_schema_to_annotation(additional_props, models_module=models_module)
            return f'dict[str, {annotation}]'
        return 'dict[str, Any]'
    # Handle primitive annotation
    return SCHEMA_TYPE_MAPPING.get(value, 'Any')


def _collect_metadata(schema: dict[str, Any]) -> list[str]:
    """Collect annotation metadata from the provided OpenAPI schema."""
    metadata = []
    metadata.extend(_collect_information_metadata(schema))
    metadata.extend(_collect_validation_metadata(schema))
    return metadata


def _collect_information_metadata(schema: dict[str, Any]) -> list[str]:
    """Collect information metadata from the provided OpenAPI schema."""
    metadata = []

    # Handle title
    if schema.get('title') is not None:
        metadata.append(f"title='{schema['title']}'")

    # Handle description
    if schema.get('description') is not None:
        metadata.append(f"description='{schema['description']}'")

    # Handle examples
    if schema.get('examples') is not None:
        examples = schema['examples']
        if isinstance(examples, list):
            examples_str = str(examples).replace("'", '"')
            metadata.append(f'examples={examples_str}')

    # Handle default
    if schema.get('default') is not None:
        default_value = schema['default']
        if isinstance(default_value, str):
            metadata.append(f"default='{default_value}'")
        else:
            metadata.append(f'default={default_value}')

    return metadata


def _collect_validation_metadata(schema: dict[str, Any]) -> list[str]:  # noqa: C901
    """Collect validation metadata from the provided OpenAPI schema."""
    metadata = []

    # Handle string
    if schema.get('minLength') is not None:
        metadata.append(f'min_length={schema["minLength"]}')
    if schema.get('maxLength') is not None:
        metadata.append(f'max_length={schema["maxLength"]}')
    if schema.get('pattern') is not None:
        metadata.append(f"pattern=r'{schema['pattern']}'")

    # Handle number
    if schema.get('minimum') is not None:
        metadata.append(f'ge={schema["minimum"]}')
    if schema.get('maximum') is not None:
        metadata.append(f'le={schema["maximum"]}')
    if schema.get('exclusiveMinimum') is not None:
        metadata.append(f'gt={schema["exclusiveMinimum"]}')
    if schema.get('exclusiveMaximum') is not None:
        metadata.append(f'lt={schema["exclusiveMaximum"]}')
    if schema.get('multipleOf') is not None:
        metadata.append(f'multiple_of={schema["multipleOf"]}')

    # Handle array
    if schema.get('minItems') is not None:
        metadata.append(f'min_length={schema["minItems"]}')
    if schema.get('maxItems') is not None:
        metadata.append(f'max_length={schema["maxItems"]}')
    if schema.get('uniqueItems') is True:
        metadata.append('unique_items=True')

    # Handle object
    if schema.get('minProperties') is not None:
        metadata.append(f'min_length={schema["minProperties"]}')
    if schema.get('maxProperties') is not None:
        metadata.append(f'max_length={schema["maxProperties"]}')

    return metadata
