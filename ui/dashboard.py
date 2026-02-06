import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QFileDialog, QProgressBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from core.uploader import Uploader
from core.worker import AnalysisWorker

class DragDropWidget(QFrame):
    files_dropped = Signal(list)

    def __init__(self):
        super().__init__()
        self.setObjectName("DropZone")
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout(self)
        
        self.label = QLabel("DRAG & DROP LOG FILES HERE\n[ OR CLICK TO BROWSE ]")
        self.label.setObjectName("DropLabel")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

    def mousePressEvent(self, event):
        file_dialog = QFileDialog()
        files, _ = file_dialog.getOpenFileNames(
            self, "Select Logs", "", "Log Files (*.log *.txt *.csv *.json)"
        )
        if files:
            self.files_dropped.emit(files)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if Uploader.is_valid_file(file_path):
                files.append(file_path)
        
        if files:
            self.files_dropped.emit(files)


class Dashboard(QWidget):
    """
    Main entry view. Handles file upload and processing status.
    """
    analysis_finished = Signal()
    entry_processed = Signal(object) # LogEntry

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # Header
        self.header = QLabel("FORENSIC-AMP // SYSTEM READY")
        self.header.setStyleSheet("font-size: 18pt; font-weight: bold; color: #00FF00;")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.header)
        
        # Drag & Drop
        self.drop_zone = DragDropWidget()
        self.drop_zone.files_dropped.connect(self.start_analysis)
        self.layout.addWidget(self.drop_zone)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #005500;
                border-radius: 5px;
                text-align: center;
                color: #00FF00;
            }
            QProgressBar::chunk {
                background-color: #00AA00;
            }
        """)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setRange(0, 0) # Inderminate for now
        self.progress_bar.hide()
        self.layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Waiting for input...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)

        self.worker = None

    def start_analysis(self, files):
        if self.worker and self.worker.isRunning():
            return

        self.header.setText("SYSTEM PROCESSING...")
        self.status_label.setText(f"Processing {len(files)} file(s)...")
        self.progress_bar.show()
        
        self.worker = AnalysisWorker(files)
        self.worker.entry_signal.connect(self.entry_processed)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.error_signal.connect(self.on_error)
        self.worker.start()

    def on_finished(self):
        self.header.setText("ANALYSIS COMPLETE")
        self.status_label.setText("Data ready for review.")
        self.progress_bar.hide()
        self.analysis_finished.emit()

    def on_error(self, err):
        self.header.setText("SYSTEM ERROR")
        self.status_label.setText(f"Error: {err}")
        self.progress_bar.hide()
