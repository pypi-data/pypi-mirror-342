"""Agent2Agent - A Python library for Agent-to-Agent communication"""

from agent2agent.server import A2AServer, TaskManager, InMemoryTaskManager
from agent2agent.client import A2AClient, A2ACardResolver
from agent2agent.utils import InMemoryCache, PushNotificationAuth
from agent2agent.types import (
    TaskState,
    Task,
    TaskStatus,
    Message,
    Part,
    TextPart,
    FilePart,
    DataPart,
    Artifact,
    AgentCard,
    AgentSkill,
    AgentProvider,
    AgentCapabilities,
    AgentAuthentication,
    PushNotificationConfig,
    TaskSendParams,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
    A2AClientError,
)

__version__ = "0.1.1"

__all__ = [
    "A2AServer",
    "TaskManager",
    "InMemoryTaskManager",
    "A2AClient",
    "A2ACardResolver",
    "InMemoryCache",
    "PushNotificationAuth",
    "TaskState",
    "Task",
    "TaskStatus",
    "Message",
    "Part",
    "TextPart",
    "FilePart",
    "DataPart",
    "Artifact",
    "AgentCard",
    "AgentSkill",
    "AgentProvider",
    "AgentCapabilities",
    "AgentAuthentication",
    "PushNotificationConfig",
    "TaskSendParams",
    "TaskStatusUpdateEvent",
    "TaskArtifactUpdateEvent",
    "A2AClientError",
] 