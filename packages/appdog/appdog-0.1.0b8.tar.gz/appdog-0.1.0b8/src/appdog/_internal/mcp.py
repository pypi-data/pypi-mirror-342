import dataclasses
import functools
import importlib
import inspect
import re
from collections.abc import Callable
from typing import Any

from mcp.server.fastmcp import FastMCP

from .case import to_snake_case
from .logging import logger
from .specs import EndpointInfo


class MCPResolver:
    """MCP endpoint information resolver."""

    def resolve_name(self, info: EndpointInfo) -> str:
        """Resolve the name from an endpoint information object."""
        return info.name

    def resolve_description(self, info: EndpointInfo) -> str:
        """Resolve the description from an endpoint information object."""
        if info.summary:
            description = info.summary
            if info.description:
                description += f'\n\n{info.description}'
            return description
        elif info.description:
            return info.description
        return f'{info.method.upper()} {info.path}'

    def resolve_mime_type(self, info: EndpointInfo) -> str:
        """Resolve the MIME type from an endpoint information object."""
        for response in info.responses.values():
            if 'content' in response:
                content_types = list(response['content'].keys())
                if content_types:
                    return str(content_types[0])
        return 'application/json'

    def resolve_uri(self, info: EndpointInfo) -> str:
        """Resolve the URI from an endpoint information object."""
        # Get URI protocol and path
        protocol, _, path = info.path.lstrip('/').partition('/')
        if path is None:
            uri = f'{protocol}://'
            uri_params = set()
        else:
            uri = f'{protocol}://{to_snake_case(path)}'
            uri_params = set(re.findall(r'{(\w+)}', uri))
        # Add all parameters to the URI
        for param in info.parameters:
            uri_param = to_snake_case(param['name'])
            if uri_param in uri_params:
                continue
            uri_params.add(uri_param)
            if not uri.endswith('/'):
                uri += '/'
            uri += f'{{{uri_param}}}'
        return uri


class MCPStrategy:
    """MCP strategy for mounting endpoints."""

    def is_resource(self, info: EndpointInfo) -> bool:
        """Check if an endpoint information object is a resource."""
        if info.method.upper() == 'GET':
            return True
        return False

    def is_tool(self, info: EndpointInfo) -> bool:
        """Check if an endpoint information object is a tool."""
        if info.method.upper() != 'GET':
            return True
        return False


@dataclasses.dataclass(slots=True, kw_only=True)
class ResourceInfo:
    """Endpoint information for a MCP resource."""

    fn: Callable[..., Any] = dataclasses.field(kw_only=False)
    """The wrapped endpoint function to register as a MCP resource."""

    uri: str
    """The URI of the resource."""

    name: str | None = None
    """The name of the resource."""

    description: str | None = None
    """The description of the resource."""

    mime_type: str | None = None
    """The MIME type of the resource."""


@dataclasses.dataclass(slots=True, kw_only=True)
class ToolInfo:
    """Endpoint information for a MCP tool."""

    fn: Callable[..., Any] = dataclasses.field(kw_only=False)
    """The wrapped endpoint function to register as a MCP tool."""

    name: str | None = None
    """The name of the tool."""

    description: str | None = None
    """The description of the tool."""


def create_resource_info(
    fn: Callable[..., Any],
    info: EndpointInfo | None = None,
    *,
    uri: str | None = None,
    name: str | None = None,
    description: str | None = None,
    mime_type: str | None = None,
    resolver: MCPResolver | None = None,
) -> ResourceInfo:
    """Create an MCP resource information object from a function.

    Args:
        fn: The function to wrap as an MCP resource
        info: Optional endpoint information to infer properties from
        uri: Optional URI to override the resolved URI
        name: Optional name to override the resolved name
        description: Optional description to override the resolved description
        mime_type: Optional MIME type to override the resolved MIME type
        resolver: Optional custom MCP information resolver (defaults to base resolver)

    Returns:
        An MCP resource information object
    """
    resolver = resolver or MCPResolver()
    uri = uri or resolver.resolve_uri(info) if info else None
    name = name or resolver.resolve_name(info) if info else None
    description = description or resolver.resolve_description(info) if info else None
    mime_type = mime_type or resolver.resolve_mime_type(info) if info else None

    if uri is None:
        raise ValueError('URI is required')

    wrapped_fn = _wrap_uri_params(fn, uri)

    return ResourceInfo(
        wrapped_fn,
        uri=uri,
        name=name,
        description=description,
        mime_type=mime_type,
    )


def create_tool_info(
    fn: Callable[..., Any],
    info: EndpointInfo | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
    resolver: MCPResolver | None = None,
) -> ToolInfo:
    """Create an MCP tool information object from a function.

    Args:
        fn: The function to wrap as an MCP tool
        info: Optional endpoint information to infer properties from
        name: Optional name to override the resolved name
        description: Optional description to override the resolved description
        resolver: Optional custom MCP information resolver (defaults to base resolver)

    Returns:
        An MCP tool information object
    """
    resolver = resolver or MCPResolver()
    name = name or resolver.resolve_name(info) if info else None
    description = description or resolver.resolve_description(info) if info else None

    return ToolInfo(fn=fn, name=name, description=description)


def add_to_fastmcp(server: FastMCP, *infos: ToolInfo | ResourceInfo) -> None:
    """Add tool and resource information to a FastMCP server.

    Args:
        server: The FastMCP server to register with
        *infos: List of tool and resource information
    """
    for info in infos:
        if isinstance(info, ToolInfo):
            server.tool(name=info.name, description=info.description)(info.fn)
            continue
        if isinstance(info, ResourceInfo):
            server.resource(
                uri=info.uri,
                name=info.name,
                description=info.description,
                mime_type=info.mime_type,
            )(info.fn)
            continue
        raise TypeError(f'Unsupported information object type: {type(info)}')


def mount_to_fastmcp(
    server: FastMCP,
    endpoints: dict[str, list[EndpointInfo]],
    resolver: MCPResolver | None = None,
    strategy: MCPStrategy | None = None,
) -> None:
    """Register endpoint information with a FastMCP server.

    Args:
        server: The FastMCP server to register with
        endpoints: Dictionary mapping app names to lists of endpoint information
        resolver: Optional custom resolver for properties
        strategy: Optional custom strategy for determining resource/tool status
    """
    resolver = resolver or MCPResolver()
    strategy = strategy or MCPStrategy()
    infos: list[ToolInfo | ResourceInfo] = []

    for app_name, app_endpoints in endpoints.items():
        try:
            module = importlib.import_module(f'appdog.{app_name}')
            client = module.client
        except ImportError:
            logger.error(f'Failed to import client module for {app_name!r} application')
            continue

        for app_endpoint in app_endpoints:
            fn_name = app_endpoint.name
            try:
                if not hasattr(client, fn_name):
                    raise ValueError('Failed to find client endpoint function')
                fn = getattr(client, fn_name)
                if strategy.is_tool(app_endpoint):
                    infos.append(create_tool_info(fn, app_endpoint, resolver=resolver))
                elif strategy.is_resource(app_endpoint):
                    infos.append(create_resource_info(fn, app_endpoint, resolver=resolver))
            except ValueError as e:
                logger.warning(f'Failed to mount endpoint {fn_name!r} from {app_name!r}: {e}')

    add_to_fastmcp(server, *infos)


def _wrap_uri_params(fn: Callable[..., Any], uri: str) -> Callable[..., Any]:
    """Wrap a function to remove parameters from signature that are not in the URI."""
    signature = inspect.signature(fn)
    fn_params = []
    uri_params = set(re.findall(r'{(\w+)}', uri))
    if uri_params:
        for param_name in uri_params:
            if param_name not in signature.parameters:
                raise ValueError(f'Parameter {param_name!r} not found in function signature')
            fn_params.append(signature.parameters[param_name])

    @functools.wraps(fn)
    async def wrapper(**kwargs: Any) -> Any:
        return await fn(**kwargs)  # type: ignore

    setattr(wrapper, '__signature__', signature.replace(parameters=fn_params))  # noqa: B010
    return wrapper  # type: ignore
