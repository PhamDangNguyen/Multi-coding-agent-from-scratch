from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class SessionStatus(str, Enum):
    RUNNING = "running"
    CANCELLED = "cancelled"


class ApprovalCancelled(RuntimeError):
    pass


@dataclass(frozen=True)
class ApprovalRequest:
    tool_name: str
    tool_args: dict[str, Any]
    reason: str


@dataclass
class ApprovalState:
    session_id: str = field(default_factory=lambda: uuid4().hex)
    status: SessionStatus = SessionStatus.RUNNING
    approvals: list[ApprovalRequest] = field(default_factory=list)
    denials: list[ApprovalRequest] = field(default_factory=list)


class ApprovalPolicy:
    SENSITIVE_TOOLS = {"run_background", "delete_file", "move_file", "git_commit", "git_checkout"}
    SENSITIVE_COMMANDS = (
        "rm ",
        "rm -",
        "sudo ",
        "chmod ",
        "chown ",
        "kill ",
        "pkill ",
        "reboot",
        "shutdown",
        "git reset",
        "git clean",
        "git checkout",
        "curl ",
        "wget ",
        "pip install",
        "uv add",
        "npm install",
    )

    @classmethod
    def inspect(cls, tool_name: str, tool_args: dict[str, Any]) -> ApprovalRequest | None:
        if tool_name in cls.SENSITIVE_TOOLS:
            return ApprovalRequest(tool_name, tool_args, f"sensitive tool: {tool_name}")

        command = str(tool_args.get("command", "")).lower()
        if tool_name in {"run_command", "bash_execution"}:
            for pattern in cls.SENSITIVE_COMMANDS:
                if pattern in command:
                    return ApprovalRequest(tool_name, tool_args, f"sensitive command: {pattern.strip()}")
        return None
