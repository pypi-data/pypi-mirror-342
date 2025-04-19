from __future__ import annotations
from typing import Any, Optional, TypeVar, Generic

T = TypeVar("T")


class BaseModel(Generic[T]):
    """Base class for models with common functionality."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> T:
        """Create object from dictionary."""
        return cls(
            **{k: v for k, v in data.items() if k in cls.__init__.__code__.co_varnames}
        )

    @classmethod
    def from_dicts(cls, dicts: list[dict[str, Any]]) -> list[T]:
        """Create multiple objects from a list of dictionaries."""
        return [cls.from_dict(d) for d in dicts]


class StatusOption(BaseModel["StatusOption"]):
    """Represents a status option in a GitHub project field."""

    def __init__(self, name: str, color: str = "GRAY", description: str = ""):
        self.name = name
        self.color = color
        self.description = description

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "color": self.color, "description": self.description}


class IssueLabel(BaseModel["IssueLabel"]):
    """Represents a GitHub issue label that can be applied to repositories."""

    def __init__(self, name: str, color: str = "ededed", description: str = ""):
        self.name = name
        self.color = color
        self.description = description

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "color": self.color, "description": self.description}


class IssueMilestone(BaseModel["IssueMilestone"]):
    """Represents a GitHub milestone that can be applied to repositories."""

    def __init__(self, title: str, description: str = "", due_on: Optional[str] = None):
        self.title = title
        self.description = description
        self.due_on = due_on

    def to_dict(self) -> dict[str, Any]:
        data = {"title": self.title, "description": self.description}
        if self.due_on:
            data["due_on"] = self.due_on
        return data
