"""Configuration utilities."""

import copy
from typing import Any


def override_config(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    """Overrides a base configuration with update values.

    Supports special string formats for relative updates:
    - "+=X": Add X to the current value
    - "-=X": Subtract X from the current value
    - "*X": Multiply current value by X
    - "=X": Set value to X (same as providing X directly)

    Args:
        base: Base configuration dictionary to be updated.
        updates: Dictionary with values to override in the base configuration.

    Returns:
        Updated configuration dictionary.

    Raises:
        ValueError: If an override string has invalid format.
    """

    def _interpret(value: Any, current: float) -> Any:
        """Interprets update values, handling special string formats.

        Args:
            value: The update value, possibly containing special format strings.
            current: The current value that might be modified.

        Returns:
            The interpreted value after applying any operations.

        Raises:
            ValueError: If the string format is invalid.
        """
        if isinstance(value, int | float):
            return value
        if isinstance(value, str):
            try:
                if value.startswith("+="):
                    return current + float(value[2:])
                elif value.startswith("-="):
                    return current - float(value[2:])
                elif value.startswith("*"):
                    return current * float(value[1:])
                elif value.startswith("="):
                    return float(value[1:])
                return float(value)
            except ValueError as e:
                raise ValueError(f"Invalid override format: {value}") from e
        return value

    def _recursive_merge(
        base_dict: dict[str, Any], override_dict: dict[str, Any]
    ) -> dict[str, Any]:
        """Recursively merges two dictionaries, applying value interpretation.

        Args:
            base_dict: Base dictionary to merge into.
            override_dict: Dictionary with values to override in the base.

        Returns:
            Merged dictionary with interpreted values.

        Raises:
            KeyError: If trying to override a base key that doesn't exist.
        """
        result = copy.deepcopy(base_dict)
        for key, val in override_dict.items():
            if key not in result:
                raise KeyError(f"Cannot override non-existent key: {key}")

            if isinstance(val, dict) and isinstance(result[key], dict):
                result[key] = _recursive_merge(result[key], val)
            else:
                result[key] = _interpret(val, result[key])
        return result

    return _recursive_merge(base, updates)