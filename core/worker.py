from PySide6.QtCore import QThread, Signal, QObject
from core.streaming_parser import StreamingParser
from models.log_entry import LogEntry

class AnalysisWorker(QThread):
    """
    Background thread for processing log files without blocking the UI.
    """
    progress_signal = Signal(int)  # Percentage or count
    entry_signal = Signal(object) # Emit LogEntry objects
    finished_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, file_paths):
        super().__init__()
        self.file_paths = file_paths
        self.is_running = True

    def run(self):
        try:
            total_lines_estimate = 0
            # Quick pre-scan for progress bar (optional, might be slow for huge files)
            # For now, just indefinite progress or emission based
            
            for file_path in self.file_paths:
                if not self.is_running:
                    break
                    
                parser = StreamingParser.parse_file(file_path)
                for entry in parser:
                    if not self.is_running:
                        break
                    self.entry_signal.emit(entry)
                    # self.progress_signal.emit(...) 
            
            self.finished_signal.emit()
            
        except Exception as e:
            self.error_signal.emit(str(e))

    def stop(self):
        self.is_running = False
