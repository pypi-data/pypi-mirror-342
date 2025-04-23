"""Tracks event resource."""

from datetime import datetime
from typing import Literal, TypedDict

from httpx import AsyncClient, Client


class Event(TypedDict):
    """Tracks event."""

    author: str
    author_anonymous: bool
    author_ip: str | None
    author_role: str | None
    author_user_agent: str | None
    session_id: str | None
    action: Literal["CREATE", "READ", "UPDATE", "DELETE"]
    date: datetime
    mechanism: Literal[
        "API",
        "FORCES",
        "JIRA",
        "MELTS",
        "MIGRATION",
        "RETRIEVES",
        "SCHEDULER",
        "TASK",
        "WEB",
    ]
    metadata: dict[str, object]
    object: str
    object_id: str


class EventResource:
    """Tracks event resource."""

    def __init__(self, client: Client) -> None:
        """Initialize the event resource."""
        self.client = client

    def create(self, event: Event) -> None:
        """Create an event."""
        self.client.post("/event", json=event)


class AsyncEventResource:
    """Tracks event resource."""

    def __init__(self, client: AsyncClient) -> None:
        """Initialize the event resource."""
        self.client = client

    async def create(self, event: Event) -> None:
        """Create an event."""
        await self.client.post("/event", json=event)
