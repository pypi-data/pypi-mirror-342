from appdog._internal.schema import (
    _collect_information_metadata,
    _collect_metadata,
    _collect_validation_metadata,
    _handle_composite_annotation,
    _handle_const_annotation,
    _handle_enum_annotation,
    _handle_reference_annotation,
    _handle_type_annotation,
    json_schema_to_annotation,
)


class TestJsonSchemaToAnnotation:
    """Tests for json_schema_to_annotation function."""

    def test_primitive_types(self) -> None:
        """Test converting primitive types."""
        assert json_schema_to_annotation({'type': 'string'}) == 'str'
        assert json_schema_to_annotation({'type': 'integer'}) == 'int'
        assert json_schema_to_annotation({'type': 'boolean'}) == 'bool'
        assert json_schema_to_annotation({'type': 'number'}) == 'float'
        assert json_schema_to_annotation({'type': 'unknown'}) == 'Any'

    def test_array_types(self) -> None:
        """Test converting array types."""
        assert (
            json_schema_to_annotation({'type': 'array', 'items': {'type': 'string'}}) == 'list[str]'
        )
        assert (
            json_schema_to_annotation({'type': 'array', 'items': {'type': 'integer'}})
            == 'list[int]'
        )
        assert json_schema_to_annotation({'type': 'array', 'items': {}}) == 'list[Any]'

        # Nested arrays
        nested_array = {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'string'}}}
        assert json_schema_to_annotation(nested_array) == 'list[list[str]]'

    def test_complex_schemas(self) -> None:
        """Test converting complex schema types."""
        # Enum schema
        enum_schema = {'type': 'string', 'enum': ['pending', 'approved', 'rejected']}
        assert (
            json_schema_to_annotation(enum_schema) == "Literal['pending', 'approved', 'rejected']"
        )

        # Complex nested schema
        complex_schema = {
            'type': 'object',
            'additionalProperties': {
                'type': 'array',
                'items': {'$ref': '#/components/schemas/Item'},
            },
        }
        assert json_schema_to_annotation(complex_schema) == 'dict[str, list[models.Item]]'

        # With custom models module
        assert (
            json_schema_to_annotation(complex_schema, models_module='custom_models')
            == 'dict[str, list[custom_models.Item]]'
        )

        # Composite schema
        composite_schema = {
            'anyOf': [
                complex_schema,
                enum_schema,
                {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string', 'maxLength': 50},
                        'age': {'type': 'integer', 'minimum': 0},
                    },
                    'required': ['name'],
                },
            ]
        }
        composite_result = json_schema_to_annotation(composite_schema)
        assert (
            "dict[str, list[models.Item]] | Literal['pending', 'approved', 'rejected'] | dict[str, Any]"
            == composite_result
        )

    def test_object_types(self) -> None:
        """Test converting object types."""
        assert json_schema_to_annotation({'type': 'object'}) == 'dict[str, Any]'

        # Object with additionalProperties
        obj_with_props = {'type': 'object', 'additionalProperties': {'type': 'string'}}
        assert json_schema_to_annotation(obj_with_props) == 'dict[str, str]'

        # Boolean additionalProperties
        obj_with_bool_props = {'type': 'object', 'additionalProperties': True}
        assert json_schema_to_annotation(obj_with_bool_props) == 'dict[str, Any]'

    def test_reference_types(self) -> None:
        """Test converting reference types."""
        assert json_schema_to_annotation({'$ref': '#/components/schemas/Pet'}) == 'models.Pet'
        assert json_schema_to_annotation({'$ref': '#/components/schemas/Order'}) == 'models.Order'

        # With custom models module
        assert (
            json_schema_to_annotation(
                {'$ref': '#/components/schemas/Pet'}, models_module='petstore_models'
            )
            == 'petstore_models.Pet'
        )

    def test_enum_types(self) -> None:
        """Test converting enum types."""
        # String enum
        str_enum = {'enum': ['available', 'pending', 'sold']}
        assert json_schema_to_annotation(str_enum) == "Literal['available', 'pending', 'sold']"

        # Numeric enum
        num_enum = {'enum': [1, 2, 3]}
        assert json_schema_to_annotation(num_enum) == 'Literal[1, 2, 3]'

        # Mixed enum
        mixed_enum = {'enum': ['active', 1, True]}
        assert json_schema_to_annotation(mixed_enum) == "Literal['active', 1, True]"

        # Empty enum
        assert json_schema_to_annotation({'enum': []}) == 'Any'

    def test_const_types(self) -> None:
        """Test converting const types."""
        assert json_schema_to_annotation({'const': 'active'}) == "Literal['active']"
        assert json_schema_to_annotation({'const': 42}) == 'Literal[42]'
        assert json_schema_to_annotation({'const': True}) == 'Literal[True]'

    def test_composite_types(self) -> None:
        """Test converting composite types (oneOf, anyOf, allOf)."""
        # oneOf
        one_of = {'oneOf': [{'type': 'string'}, {'type': 'integer'}]}
        assert json_schema_to_annotation(one_of) == 'str | int'

        # anyOf
        any_of = {'anyOf': [{'type': 'boolean'}, {'type': 'number'}]}
        assert json_schema_to_annotation(any_of) == 'bool | float'

        # allOf (acts similar to union in this case)
        all_of = {'allOf': [{'type': 'string'}, {'type': 'array', 'items': {'type': 'integer'}}]}
        assert json_schema_to_annotation(all_of) == 'str | list[int]'

        # Empty composites
        assert json_schema_to_annotation({'oneOf': []}) == 'Any'
        assert json_schema_to_annotation({'anyOf': []}) == 'Any'
        assert json_schema_to_annotation({'allOf': []}) == 'Any'

        # Single item composites
        assert json_schema_to_annotation({'oneOf': [{'type': 'string'}]}) == 'str'

    def test_nullable_types(self) -> None:
        """Test converting nullable types."""
        assert json_schema_to_annotation({'type': 'string', 'nullable': True}) == 'str | None'

        assert (
            json_schema_to_annotation(
                {'type': 'array', 'items': {'type': 'integer'}, 'nullable': True}
            )
            == 'list[int] | None'
        )

    def test_with_metadata(self) -> None:
        """Test converting types with metadata."""
        # String with description
        str_with_desc = {'type': 'string', 'description': 'A string value'}
        result = json_schema_to_annotation(str_with_desc)
        assert result.startswith('Annotated[str, Field(')
        assert result.endswith(')]')
        assert "description='A string value'" in result

        # Integer with min/max
        int_with_validation = {'type': 'integer', 'minimum': 1, 'maximum': 100}
        result = json_schema_to_annotation(int_with_validation)
        assert result.startswith('Annotated[int, Field(')
        assert result.endswith(')]')
        assert 'ge=1' in result
        assert 'le=100' in result

        # Multiple metadata fields
        complex_schema = {
            'type': 'string',
            'description': 'Username',
            'minLength': 3,
            'maxLength': 50,
            'pattern': '^[a-zA-Z0-9_]+$',
            'default': 'user',
        }

        result = json_schema_to_annotation(complex_schema)
        assert result.startswith('Annotated[str, Field(')
        assert result.endswith(')]')
        assert "description='Username'" in result
        assert "default='user'" in result
        assert 'min_length=3' in result
        assert 'max_length=50' in result
        assert "pattern=r'^[a-zA-Z0-9_]+$'" in result

    def test_empty_schema(self) -> None:
        """Test converting empty schema."""
        assert json_schema_to_annotation({}) == 'Any'
        # Note: The implementation doesn't support None input


class TestHandlerFunctions:
    """Tests for handler functions."""

    def test_handle_const_annotation(self) -> None:
        """Test _handle_const_annotation function."""
        assert _handle_const_annotation({'const': 'active'}) == "Literal['active']"
        assert _handle_const_annotation({'const': 42}) == 'Literal[42]'
        assert _handle_const_annotation({'const': True}) == 'Literal[True]'

    def test_handle_enum_annotation(self) -> None:
        """Test _handle_enum_annotation function."""
        assert (
            _handle_enum_annotation({'enum': ['active', 'inactive']})
            == "Literal['active', 'inactive']"
        )
        assert _handle_enum_annotation({'enum': [1, 2, 3]}) == 'Literal[1, 2, 3]'
        assert _handle_enum_annotation({'enum': []}) == 'Any'

    def test_handle_reference_annotation(self) -> None:
        """Test _handle_reference_annotation function."""
        assert (
            _handle_reference_annotation(
                {'$ref': '#/components/schemas/Pet'}, models_module='models'
            )
            == 'models.Pet'
        )
        assert (
            _handle_reference_annotation(
                {'$ref': '#/components/schemas/Pet'}, models_module='custom_models'
            )
            == 'custom_models.Pet'
        )
        assert (
            _handle_reference_annotation(
                {'$ref': 'https://example.com/schemas/Pet'}, models_module='models'
            )
            == 'models.Pet'
        )

    def test_handle_type_annotation(self) -> None:
        """Test _handle_type_annotation function."""
        # Primitive types
        assert _handle_type_annotation({'type': 'string'}, models_module='models') == 'str'
        assert _handle_type_annotation({'type': 'integer'}, models_module='models') == 'int'
        assert _handle_type_annotation({'type': 'boolean'}, models_module='models') == 'bool'
        assert _handle_type_annotation({'type': 'number'}, models_module='models') == 'float'
        assert _handle_type_annotation({'type': 'unknown'}, models_module='models') == 'Any'

        # Array types
        assert (
            _handle_type_annotation(
                {'type': 'array', 'items': {'type': 'string'}}, models_module='models'
            )
            == 'list[str]'
        )

        # Object types
        assert (
            _handle_type_annotation({'type': 'object'}, models_module='models') == 'dict[str, Any]'
        )
        assert (
            _handle_type_annotation(
                {'type': 'object', 'additionalProperties': {'type': 'integer'}},
                models_module='models',
            )
            == 'dict[str, int]'
        )

    def test_handle_composite_annotation(self) -> None:
        """Test _handle_composite_annotation function."""
        # oneOf
        schema = {'oneOf': [{'type': 'string'}, {'type': 'integer'}]}
        assert _handle_composite_annotation(schema, 'oneOf', models_module='models') == 'str | int'

        # Empty composite
        assert _handle_composite_annotation({'oneOf': []}, 'oneOf', models_module='models') == 'Any'

        # Single item composite
        assert (
            _handle_composite_annotation(
                {'oneOf': [{'type': 'string'}]}, 'oneOf', models_module='models'
            )
            == 'str'
        )


class TestMetadataCollection:
    """Tests for metadata collection functions."""

    def test_collect_information_metadata(self) -> None:
        """Test _collect_information_metadata function."""
        # Title
        assert _collect_information_metadata({'title': 'Test Schema'}) == ["title='Test Schema'"]

        # Description
        assert _collect_information_metadata({'description': 'A test schema'}) == [
            "description='A test schema'"
        ]

        # Examples
        assert _collect_information_metadata({'examples': ['example1', 'example2']}) == [
            'examples=["example1", "example2"]'
        ]

        # Default (string)
        assert _collect_information_metadata({'default': 'default_value'}) == [
            "default='default_value'"
        ]

        # Default (numeric)
        assert _collect_information_metadata({'default': 42}) == ['default=42']

        # Multiple metadata
        schema = {'title': 'User', 'description': 'A user object', 'default': 'guest'}
        metadata = _collect_information_metadata(schema)
        assert len(metadata) == 3
        assert "title='User'" in metadata
        assert "description='A user object'" in metadata
        assert "default='guest'" in metadata

    def test_collect_validation_metadata(self) -> None:
        """Test _collect_validation_metadata function."""
        # String validations
        string_schema = {'minLength': 5, 'maxLength': 50, 'pattern': '^[a-z]+$'}
        string_metadata = _collect_validation_metadata(string_schema)
        assert 'min_length=5' in string_metadata
        assert 'max_length=50' in string_metadata
        assert "pattern=r'^[a-z]+$'" in string_metadata

        # Number validations
        number_schema = {
            'minimum': 1,
            'maximum': 100,
            'exclusiveMinimum': 0,
            'exclusiveMaximum': 101,
            'multipleOf': 2,
        }
        number_metadata = _collect_validation_metadata(number_schema)
        assert 'ge=1' in number_metadata
        assert 'le=100' in number_metadata
        assert 'gt=0' in number_metadata
        assert 'lt=101' in number_metadata
        assert 'multiple_of=2' in number_metadata

        # Array validations
        array_schema = {'minItems': 1, 'maxItems': 10, 'uniqueItems': True}
        array_metadata = _collect_validation_metadata(array_schema)
        assert 'min_length=1' in array_metadata
        assert 'max_length=10' in array_metadata
        assert 'unique_items=True' in array_metadata

        # Object validations
        object_schema = {'minProperties': 1, 'maxProperties': 5}
        object_metadata = _collect_validation_metadata(object_schema)
        assert 'min_length=1' in object_metadata
        assert 'max_length=5' in object_metadata

    def test_collect_metadata(self) -> None:
        """Test _collect_metadata function."""
        schema = {'title': 'User', 'description': 'A user object', 'minLength': 5, 'maxLength': 50}
        metadata = _collect_metadata(schema)
        assert len(metadata) == 4
        assert "title='User'" in metadata
        assert "description='A user object'" in metadata
        assert 'min_length=5' in metadata
        assert 'max_length=50' in metadata
