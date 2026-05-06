import sys
import os
import time
from PySide6.QtCore import QCoreApplication

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.worker import AnalysisWorker
from models.log_entry import LogEntry

def verify_headless():
    app = QCoreApplication(sys.argv)
    
    print("1. Initializing Worker...")
    worker = AnalysisWorker([os.path.abspath("tests/dummy.log")])
    
    entries = []
    
    def on_entry(entry):
        entries.append(entry)
        print(f" -> Processed: {entry.raw_content[:50]}... | Severity: {entry.severity}")

    def on_finished():
        print("2. Analysis Finished Signal Received")
        print(f"Total Entries: {len(entries)}")
        
        # Validation
        sqli = next((e for e in entries if "SQL Injection" in (e.attack_type or "")), None)
        if sqli:
            print(" [PASS] Detected SQL Injection")
        else:
            print(" [FAIL] Failed to detect SQL Injection")

        xss = next((e for e in entries if "XSS" in (e.attack_type or "")), None)
        if xss:
            print(" [PASS] Detected XSS")
        else:
            print(" [FAIL] Failed to detect XSS")
            
        app.quit()

    worker.entry_signal.connect(on_entry)
    worker.finished_signal.connect(on_finished)
    worker.error_signal.connect(lambda e: print(f"ERROR: {e}"))
    
    print("Starting Worker...")
    worker.start()
    
    # Run loop for max 5 seconds
    # QCoreApplication.exec() is blocking, so we rely on finished signal to quit
    sys.exit(app.exec())

if __name__ == "__main__":
    verify_headless()
