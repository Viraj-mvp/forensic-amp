from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class LogEntry:
    """
    Represents a single parsed log line with forensic metadata.
    """
    timestamp: datetime
    raw_content: str
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    method: Optional[str] = None
    url: Optional[str] = None
    status_code: int = 0
    user_agent: Optional[str] = None
    decoded_payload: Optional[str] = None
    attack_type: Optional[str] = None  # e.g., 'SQLi', 'XSS', 'BruteForce'
    severity: int = 0  # 0-100 score
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        """Convert for UI/Export usage"""
        return {
            "timestamp": self.timestamp.isoformat() if self.timestamp else "",
            "severity": self.severity,
            "attack_type": self.attack_type or "Normal",
            "source_ip": self.source_ip or "N/A",
            "method": self.method or "",
            "url": self.decoded_payload or self.url or "",
            "status": self.status_code,
            "raw": self.raw_content
        }
