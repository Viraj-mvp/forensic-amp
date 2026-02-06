import base64
import urllib.parse
import re

class Decoder:
    """
    Utility class for decoding obfuscated payloads.
    """
    
    @staticmethod
    def decode_safe(payload: str) -> str:
        """
        Attempts to decode a string using multiple methods (URL, Base64).
        Returns the most human-readable version found.
        """
        if not payload:
            return ""

        original = payload
        current = payload
        
        # 1. URL Decode (multiple passes)
        for _ in range(3):
            try:
                decoded = urllib.parse.unquote(current)
                if decoded == current:
                    break
                current = decoded
            except Exception:
                break
        
        # 2. Base64 Decode
        # Check if looks like base64 (alphanumeric + += /)
        if len(current) > 4 and re.match(r'^[A-Za-z0-9+/=]+$', current):
            try:
                # Add padding if missing
                missing_padding = len(current) % 4
                if missing_padding:
                    current += '=' * (4 - missing_padding)
                
                b64_decoded = base64.b64decode(current).decode('utf-8', errors='ignore')
                # If the result looks like garbage, discard it maybe? 
                # For now, we accept it if it decoded without error.
                if any(c.isprintable() for c in b64_decoded):
                     current = b64_decoded
            except Exception:
                pass

        return current

    @staticmethod
    def detect_encoding(content: str) -> str:
        # Placeholder for more advanced encoding detection
        return "utf-8"
