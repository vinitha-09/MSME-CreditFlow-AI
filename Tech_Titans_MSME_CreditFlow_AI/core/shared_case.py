from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
import uuid

@dataclass
class SharedCase:
    applicant: dict
    case_id: str = field(default_factory=lambda: "CF-" + uuid.uuid4().hex[:8].upper())
    results: dict = field(default_factory=dict)
    messages: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def add_result(self, agent: str, result: dict):
        self.results[agent] = result

    def send(self, sender: str, receiver: str, message_type: str, payload: dict):
        self.messages.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "sender": sender, "receiver": receiver,
            "type": message_type, "payload": payload
        })
