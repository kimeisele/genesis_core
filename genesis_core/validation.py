"""
Validation - Genesis Core Module

⚠️ FROZEN CORE MODULE ⚠️

This module is part of the Genesis Core and MUST NOT be modified.

Core Principle: Defines and applies validation rules to entities.

If you need to:
- Add features → Create an extension in extensions/validation_extended.py
- Fix bugs → Create a wrapper in extensions/validation_patches.py
- Change behavior → Create an adapter in extensions/validation_adapters.py

DO NOT MODIFY THIS FILE.

Last Known Good State: 2025-11-11
"""

from typing import Callable
from dataclasses import dataclass

from . import entity as entity_module


@dataclass
class Rule:
    """Validation rule definition."""

    name: str
    condition: Callable[[entity_module.Entity], bool]


@dataclass
class ValidationResult:
    """Result of validation."""

    is_valid: bool
    errors: list[str]


# Registry of all rules
_rules: dict[str, Rule] = {}


def define_rule(name: str, condition: Callable[[entity_module.Entity], bool]) -> Rule:
    """
    Define named validation rule.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        name: Unique rule name
        condition: Function that takes Entity and returns True if valid

    Returns:
        Rule: The defined rule

    Raises:
        KeyError: If rule name already exists
    """
    if name in _rules:
        raise KeyError(f"Rule '{name}' already defined")

    rule = Rule(name=name, condition=condition)
    _rules[name] = rule
    return rule


def validate(entity: entity_module.Entity, rules: list[str]) -> ValidationResult:
    """
    Validate entity against list of rules.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        entity: Entity to validate
        rules: List of rule names to apply

    Returns:
        ValidationResult: Validation result with errors if any

    Raises:
        KeyError: If any rule does not exist
    """
    errors = []

    for rule_name in rules:
        rule = get_rule(rule_name)

        try:
            is_valid = rule.condition(entity)
            if not is_valid:
                errors.append(f"Rule '{rule_name}' failed")
        except Exception as e:
            errors.append(f"Rule '{rule_name}' raised error: {str(e)}")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)


def get_rule(name: str) -> Rule:
    """
    Retrieve rule definition.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Args:
        name: Rule name

    Returns:
        Rule: The rule definition

    Raises:
        KeyError: If rule does not exist
    """
    if name not in _rules:
        raise KeyError(f"Rule '{name}' not found")

    return _rules[name]


def list_rules() -> list[str]:
    """
    List all defined rules.

    ⚠️ FROZEN FUNCTION - DO NOT MODIFY ⚠️

    Returns:
        list[str]: Sorted list of rule names
    """
    return sorted(_rules.keys())
