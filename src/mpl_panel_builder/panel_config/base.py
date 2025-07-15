"""Base classes for configuration system."""

from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any, TypeVar

T = TypeVar("T", bound="FrozenConfigBase")


class DotDict(dict[str, Any]):
    """A read-only dictionary that can be accessed as an object with dot notation.

    This class is used to provide dot access to non-mandatory custom
    configuration values. This allows for more flexible configuration, while
    still providing a consistent interface for all configuration values.
    """

    def __init__(self, d: dict[str, Any]) -> None:
        """Initializes the dictionary with the given values.

        Args:
            d: The dictionary to initialize the DotDict with.
        """
        super().__init__()
        for key, value in d.items():
            self[key] = self._wrap(value)

    def __getattr__(self, key: str) -> Any:
        """Returns the value for the given key.

        Args:
            key: The key to get the value for.
        """
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(f"Object has no attribute '{key}'") from e

    def __setattr__(self, key: str, value: Any) -> None:
        """Raises an error if the attribute is set.

        Args:
            key: The key to set the value for.
            value: The value to set.
        """
        raise AttributeError(f"Cannot modify read-only config attribute '{key}'")

    def __delattr__(self, key: str) -> None:
        """Raises an error if the attribute is deleted.

        Args:
            key: The key to delete.
        """
        raise AttributeError(f"Cannot delete read-only config attribute '{key}'")

    def _wrap(self, value: Any) -> Any:
        """Wraps the value in a DotDict if it is a dictionary.

        Args:
            value: The value to wrap.
        """
        if isinstance(value, dict):
            return DotDict(value)
        return value


@dataclass(frozen=True)
class FrozenConfigBase:
    """Base class for immutable config objects with dot access to extra fields.

    This class is used to create immutable config objects with dot access to extra
    fields. The extra fields are stored in the _extra attribute, which is a dictionary
    of key-value pairs.
    """

    _extra: dict[str, Any] = field(default_factory=dict, init=False, repr=False)

    def __getattr__(self, name: str) -> Any:
        """Returns the value for the given key.

        Args:
            name: The key to get the value for.
        """
        # Safely access _extra only if initialized
        extra = object.__getattribute__(self, "__dict__").get("_extra", {})
        if name in extra:
            return extra[name]
        raise AttributeError(f"Object has no attribute '{name}'")

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        """Creates a FrozenConfigBase instance from a dictionary.

        Args:
            data: The dictionary to create the instance from.

        Returns:
            The FrozenConfigBase instance.
        """
        field_names = {f.name for f in fields(cls)}
        declared = {}
        extra = {}

        for key, value in data.items():
            # If the key is a declared field, add it to the declared dictionary
            if key in field_names:
                field_type = next(f.type for f in fields(cls) if f.name == key)

                # If the field is a dataclass, convert the value to the dataclass type
                if is_dataclass(field_type) and isinstance(value, dict):
                    # The field_type has from_dict as it inherits from FrozenConfigBase
                    value = field_type.from_dict(value)  # type: ignore

                declared[key] = value

            # If the key is not a declared field, add it to the extra dictionary
            else:
                # Only wrap dictionaries with DotDict
                if isinstance(value, dict):
                    extra[key] = DotDict(value)
                else:
                    extra[key] = value

        # Create the frozen dataclass instance
        instance = cls(**declared)  # This triggers __post_init__ if defined

        # Inject _extra manually, bypassing frozen restriction
        object.__setattr__(instance, "_extra", extra)
        return instance