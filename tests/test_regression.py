
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.streaming_parser import StreamingParser

def test_normal_log_parsing():
    # Standard Apache log line
    line = '192.168.1.1 - - [04/Jan/2026:10:00:00 +0000] "GET /index.php HTTP/1.1" 200 1234'
    
    entry = StreamingParser._parse_line(line)
    
    print(f"IP: {entry.source_ip}")
    print(f"URL: {entry.url}")
    print(f"Status: {entry.status_code}")
    
    if entry.source_ip == "192.168.1.1" and entry.status_code == 200:
        print("SUCCESS: Normal log parsed correctly.")
    else:
        print("FAILURE: Normal log parsing failed.")

if __name__ == "__main__":
    test_normal_log_parsing()
