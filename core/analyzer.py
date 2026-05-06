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

    # Severity scores based on CVSS v3.0 ratings (scaled to 0-100)
    # Critical (90-100), High (70-89), Medium (40-69), Low (1-39)
    ATTACK_SEVERITY = {
        'Command Injection': 100, # Critical - CVSS ~9.0-10.0
        'SQL Injection': 95,      # Critical - CVSS ~8.0-9.8
        'Path Traversal': 85,     # High     - CVSS ~7.5-8.6
        'XSS': 75,                # High     - CVSS ~6.1-8.0
        'Brute Force': 80         # High     - Context dependent
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
                    # Use specific severity for the attack, default to 70 (High) if not listed
                    severity_score = Analyzer.ATTACK_SEVERITY.get(attack_name, 70)
                    max_severity = max(max_severity, severity_score)
                    # Continue searching to find potentially higher severity attacks
        
        # 2. Status Code Analysis
        # Note: Standalone status codes (404, 403, 500) without signatures are treated as 
        # Informational (Severity 0) to reduce noise, unless an attack was already detected.
        if entry.status_code >= 500:
            # If we already detected an attack, a 500 implies successful exploitation
            if max_severity > 0:
                max_severity = min(max_severity + 10, 100) # Bump severity for server error during attack

        # 3. Update Entry
        entry.severity = max_severity
        entry.attack_type = ", ".join(list(set(detected_attacks))) if detected_attacks else None
        
        return entry
