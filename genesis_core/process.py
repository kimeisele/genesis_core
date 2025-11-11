"""
Process - Genesis Core Module

⚠️ FROZEN CORE MODULE ⚠️

This module is part of the Genesis Core and MUST NOT be modified.

Core Principle: Defines and executes multi-step processes/workflows.

If you need to:
- Add features → Create an extension in extensions/process_extended.py
- Fix bugs → Create a wrapper in extensions/process_patches.py
- Change behavior → Create an adapter in extensions/process_adapters.py

DO NOT MODIFY THIS FILE.

Last Known Good State: 2025-11-11
"""

from typing import Callable
from dataclasses import dataclass

from . import entity as entity_module


@dataclass
class Process:
    """Process definition with ordered steps."""
    name: str
    steps: list[str]


# Registry of all processes
_processes: dict[str, Process] = {}

# Registry of step handlers
_step_handlers: dict[str, Callable[[entity_module.Entity], entity_module.Entity]] = {}


def define_process(name: str, steps: list[str]) -> Process:
    """
    Define named process with ordered steps.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        name: Unique process name
        steps: Ordered list of step names

    Returns:
        Process: The defined process

    Raises:
        KeyError: If process name already exists
    """
    if name in _processes:
        raise KeyError(f"Process '{name}' already defined")

    process = Process(name=name, steps=steps)
    _processes[name] = process
    return process


def register_step_handler(
    step_name: str,
    handler: Callable[[entity_module.Entity], entity_module.Entity]
) -> None:
    """
    Register handler function for a step.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        step_name: Name of the step
        handler: Function that takes Entity and returns Entity

    Returns:
        None

    Raises:
        KeyError: If step handler already registered
    """
    if step_name in _step_handlers:
        raise KeyError(f"Step handler '{step_name}' already registered")

    _step_handlers[step_name] = handler


def execute_process(process_name: str, entity: entity_module.Entity) -> entity_module.Entity:
    """
    Execute process on entity.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        process_name: Name of process to execute
        entity: Entity to process

    Returns:
        Entity: The processed entity

    Raises:
        KeyError: If process does not exist or step handler not found
    """
    process = get_process(process_name)

    current_entity = entity

    # Execute each step in order
    for step_name in process.steps:
        if step_name not in _step_handlers:
            raise KeyError(f"No handler registered for step '{step_name}'")

        handler = _step_handlers[step_name]
        current_entity = handler(current_entity)

    return current_entity


def get_process(name: str) -> Process:
    """
    Retrieve process definition.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        name: Process name

    Returns:
        Process: The process definition

    Raises:
        KeyError: If process does not exist
    """
    if name not in _processes:
        raise KeyError(f"Process '{name}' not found")

    return _processes[name]


def list_processes() -> list[str]:
    """
    List all defined processes.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Returns:
        list[str]: Sorted list of process names
    """
    return sorted(_processes.keys())
