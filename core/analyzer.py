import re
from models.log_entry import LogEntry

class Analyzer:
    """
    Forensic analysis engine to detect attacks and score severity.
    """
    
    # Simple regex signatures for common attacks
    SIGNATURES = {
        'SQL Injection': [
            r"UNION SELECT", r"OR 1=1", r"content-type:", r"information_schema",
            r"benchmark\(", r"sleep\(" 
        ],
        'XSS': [
            r"<script>", r"javascript:", r"onerror=", r"onload="
        ],
        'Path Traversal': [
            r"\.\./", r"\.\.\\", r"/etc/passwd", r"boot.ini"
        ],
        'Command Injection': [
            r"; cat ", r"| dir", r"| ls", r"$(whoami)"
        ]
    }

    @staticmethod
    def analyze(entry: LogEntry) -> LogEntry:
        """
        Analyzes a log entry for IOcs and updates its metadata.
        """
        content_to_scan = f"{entry.raw_content} {entry.decoded_payload or ''}".lower()
        
        max_severity = 0
        detected_attacks = []

        # 1. Signature Matching
        for attack_name, patterns in Analyzer.SIGNATURES.items():
            for pattern in patterns:
                if re.search(pattern, content_to_scan, re.IGNORECASE):
                    detected_attacks.append(attack_name)
                    max_severity = max(max_severity, 80) # High severity for signature match
                    break
        
        # 2. Status Code Analysis
        if entry.status_code == 404:
            # High volume of 404s (context needed) but single entry:
            pass
        elif entry.status_code == 500:
            # 500 errors often indicate successful exploits or fuzzing
            if max_severity > 0:
                max_severity = 95 # Critical: Exploit attempt causing error
            else:
                max_severity = max(max_severity, 30)

        # 3. Update Entry
        entry.severity = max_severity
        entry.attack_type = ", ".join(list(set(detected_attacks))) if detected_attacks else None
        
        return entry
