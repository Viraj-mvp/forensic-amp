from typing import List, Dict
from models.log_entry import LogEntry

class Recommender:
    """
    Generates actionable security recommendations based on analysis findings.
    """
    
    RECOMMENDATIONS_DB = {
        'SQL Injection': [
            "Implement parameterized queries (Prepared Statements).",
            "Enable strict input validation and sanitization.",
            "Use a Web Application Firewall (WAF) rule for SQLi patterns."
        ],
        'XSS': [
            "Implement Content Security Policy (CSP) headers.",
            "Escape all user-generated content on output.",
            "Use context-sensitive encoding libraries."
        ],
        'Path Traversal': [
            "Validate file paths against a whitelist.",
            "Run application with least-privilege user permissions.",
            "Disable directory listing on the web server."
        ],
        'Command Injection': [
            "Avoid using system calls (exec, system, popen) with user input.",
            "Use language-specific APIs instead of shell commands.",
            "Sanitize input for shell metacharacters."
        ],
        'Brute Force': [
            "Implement rate limiting (e.g., Fail2Ban).",
            "Enforce strong password policies.",
            "Enable Multi-Factor Authentication (MFA)."
        ]
    }

    @staticmethod
    def get_recommendations(entries: List[LogEntry]) -> Dict[str, List[str]]:
        """
        Aggregates findings and returns a unique list of recommendations.
        """
        detected_attacks = set()
        for entry in entries:
            if entry.attack_type:
                attacks = entry.attack_type.split(", ")
                detected_attacks.update(attacks)
        
        report = {}
        for attack in detected_attacks:
            if attack in Recommender.RECOMMENDATIONS_DB:
                report[attack] = Recommender.RECOMMENDATIONS_DB[attack]
        
        return report
