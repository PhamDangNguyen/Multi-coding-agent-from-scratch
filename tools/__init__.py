"""
tools/__init__.py

Auto-discovers tất cả các tool class (subclass của BaseTool) từ các
subpackage (bash/, git/, search/, ...), đăng ký vào ToolRegistry,
và export:

    TOOL_REGISTRY   – ToolRegistry instance
    TOOLS_DICT      – dict[name, description]
    TOOLS_INSTANCE  – dict[name, tool_instance]
"""

import importlib
import inspect
from pathlib import Path

from tools.base import BaseTool
from tools.registry import ToolRegistry

TOOL_REGISTRY = ToolRegistry()
TOOLS_INSTANCE: dict[str, BaseTool] = {}

_tools_dir = Path(__file__).parent

# Scan tools/*
for subdir in sorted(_tools_dir.iterdir()):
    if not subdir.is_dir() or subdir.name.startswith("_"):
        continue

    pkg_name = f"tools.{subdir.name}"

    for py_file in sorted(subdir.glob("*.py")):
        if py_file.name.startswith("_"):
            continue

        module_name = f"{pkg_name}.{py_file.stem}"
        module = importlib.import_module(module_name)

        # Find BaseTool subclasses
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, BaseTool)
                and obj is not BaseTool
                and obj.name
            ):
                instance = obj()

                # register in registry
                TOOL_REGISTRY.register(instance)

                # store instance
                TOOLS_INSTANCE[obj.name] = instance


# metadata dict
TOOLS_DICT: dict[str, str] = {
    schema["name"]: schema["description"]
    for schema in TOOL_REGISTRY.list_tools()
}