"""Internal state that maintains the list of registered tools."""

import typing

from claude_llm_tools import models


class State:
    _instance: 'State | None' = None

    def __init__(self) -> None:
        self.tools: list[models.Tool] = []

    @classmethod
    def get_instance(cls) -> 'State':
        if not cls._instance:
            cls._instance = cls()
        return cls._instance


def add_tool(tool: models.Tool) -> None:
    for value in get_tools():
        if value.name == tool.name:
            return
    State.get_instance().tools.append(tool)


def get_tool(name: str) -> models.Tool | None:
    state = State.get_instance()
    for tool in state.tools:
        if tool.name == name:
            return tool
    raise ValueError('Tool not found')


def get_tool_name(function: typing.Callable) -> str:
    for tool in get_tools():
        if tool.callable == function:
            return tool.name
    raise ValueError('Tool not found')


def get_tools() -> list[models.Tool]:
    """Return the list of registered tools."""
    return State.get_instance().tools
