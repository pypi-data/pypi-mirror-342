"""
Tool module initialization
"""
from functools import wraps
from typing import Callable, Dict, Any, Optional, Type


TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {}
_TOOL_FUNCTIONS: Dict[str, Callable] = {}


def register_tool(name: str, description: str, model_class: Type):
    """
    Unified tool registration decorator

    Usage:
    @register_tool("tool_name", "Tool description", ModelClass)
    async def tool_function(args: dict) -> list[types.TextContent]:
        ...

    Args:
        name: Tool name
        description: Tool description
        model_class: Parameter validation model class
    """
    def decorator(func: Callable):
        TOOL_REGISTRY[name] = {
            "name": name,
            "description": description,
            "model": model_class,
        }

        _TOOL_FUNCTIONS[name] = func

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def get_tool_function(name: str) -> Optional[Callable]:
    """
    Get the corresponding tool function based on the tool name

    Args:
        name: Tool name

    Returns:
        The corresponding tool function, or None if it does not exist
    """
    return _TOOL_FUNCTIONS.get(name)


def is_tool_registered(name: str) -> bool:
    """
    Check if the tool is registered

    Args:
        name: Tool name

    Returns:
        Whether the tool is registered
    """
    return name in TOOL_REGISTRY and name in _TOOL_FUNCTIONS
