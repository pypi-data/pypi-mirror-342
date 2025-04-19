import typing
from typing import Any

from pydantic import GetCoreSchemaHandler, SerializationInfo
from pydantic_core import CoreSchema, core_schema
from typing_extensions import Self

CHAR_MARK = '\ue000'
"""A special character used as a placeholder for string transformations."""

CHAR_SEP = '\ue001'
"""A special character used as a separator for string transformations."""


@typing.final
class UndefinedType:
    """A type used as a sentinel for undefined values."""

    instance: Self | None = None

    def __new__(cls) -> Self:
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        __source: type[Any],
        __handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        def serialize(value: Any, info: SerializationInfo) -> Any:
            return CHAR_MARK if info.mode == 'json' else value

        return core_schema.json_or_python_schema(
            json_schema=core_schema.no_info_after_validator_function(
                lambda _: cls(),
                core_schema.str_schema(pattern=rf'^{CHAR_MARK}$'),
            ),
            python_schema=core_schema.is_instance_schema(cls),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize,
                info_arg=True,
            ),
        )

    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self, memo: Any) -> Self:
        return self

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return 'Undefined'


Undefined: Any = UndefinedType()
"""The undefined singleton instance."""
