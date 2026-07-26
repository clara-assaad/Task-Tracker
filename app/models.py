from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def normalize_tags(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError("tags must be a list of strings")

    normalized_tags: list[str] = []
    seen_tags: set[str] = set()
    for tag in value:
        if not isinstance(tag, str):
            raise TypeError("tags must be a list of strings")

        trimmed_tag = tag.strip()
        if not trimmed_tag:
            continue

        tag_key = trimmed_tag.lower()
        if tag_key in seen_tags:
            continue

        seen_tags.add(tag_key)
        normalized_tags.append(trimmed_tag)

    return normalized_tags


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: object) -> object:
        if value is None:
            return value
        if not isinstance(value, str):
            raise TypeError("title must be a string")

        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("title cannot be blank")
        if len(stripped_value) > 200:
            raise ValueError("title cannot exceed 200 characters")
        return stripped_value

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, value: object) -> object:
        if value is None:
            return value
        return normalize_tags(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: object) -> object:
        if value is None:
            return value
        if not isinstance(value, str):
            raise TypeError("title must be a string")

        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("title cannot be blank")
        if len(stripped_value) > 200:
            raise ValueError("title cannot exceed 200 characters")
        return stripped_value

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, value: object) -> object:
        if value is None:
            return value
        return normalize_tags(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
