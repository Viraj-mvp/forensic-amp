from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QHeaderView, QLabel, QGroupBox, QSplitter, QApplication,
    QTextEdit, QFrame, QHBoxLayout, QPushButton, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from typing import List
import csv
from models.log_entry import LogEntry
from core.recommender import Recommender

class FindingsPanel(QWidget):
    """
    Displays decoded payloads, detected attacks, and security recommendations.
    """
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # Splitter to show Findings (Top) and Recommendations (Bottom)
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # --- Findings Table ---
        self.findings_group = QGroupBox("DETECTED ANOMALIES")
        self.findings_layout = QVBoxLayout()
        
        # Toolbar
        self.toolbar_layout = QHBoxLayout()
        
        self.btn_copy_all = QPushButton("COPY ALL TO CLIPBOARD")
        self.btn_copy_all.clicked.connect(self.copy_all_to_clipboard)
        
        self.btn_export_csv = QPushButton("EXPORT TO CSV")
        self.btn_export_csv.clicked.connect(self.export_to_csv)
        
        self.toolbar_layout.addWidget(self.btn_copy_all)
        self.toolbar_layout.addWidget(self.btn_export_csv)
        self.toolbar_layout.addStretch()
        
        self.findings_layout.addLayout(self.toolbar_layout)

        self.findings_table = QTableWidget()
        self.findings_table.setColumnCount(5)
        self.findings_table.setHorizontalHeaderLabels(["Timestamp", "Severity", "Attack Type", "Valid Payload (Decoded)", "Source IP"])
        self.findings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.findings_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Payload wider
        self.findings_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.findings_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.findings_table.setSortingEnabled(True)
        
        # Increase default row height for better payload visibility
        self.findings_table.verticalHeader().setDefaultSectionSize(60)

        # Enable Copy (Ctrl+C)
        self.copy_shortcut = QShortcut(QKeySequence.Copy, self.findings_table)
        self.copy_shortcut.activated.connect(self.copy_to_clipboard)
        
        self.findings_layout.addWidget(self.findings_table)
        self.findings_group.setLayout(self.findings_layout)
        
        # --- Recommendations ---
        self.rec_group = QGroupBox("HARDENING RECOMMENDATIONS")
        self.rec_layout = QVBoxLayout()
        self.rec_label = QLabel("No active threats detected. System secure.")
        self.rec_label.setWordWrap(True)
        self.rec_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.rec_layout.addWidget(self.rec_label)
        self.rec_group.setLayout(self.rec_layout)
        
        splitter.addWidget(self.findings_group)
        splitter.addWidget(self.rec_group)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        self.layout.addWidget(splitter)
        
        self.all_entries = []

    def copy_to_clipboard(self):
        """
        Copies selected rows to the clipboard in tab-separated format.
        """
        selection = self.findings_table.selectedRanges()
        if not selection:
            return
            
        rows = sorted(set(index.row() for index in self.findings_table.selectedIndexes()))
        
        text_data = []
        for row in rows:
            row_data = []
            for col in range(self.findings_table.columnCount()):
                item = self.findings_table.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            text_data.append("\t".join(row_data))
            
        QApplication.clipboard().setText("\n".join(text_data))

    def add_entry(self, entry: LogEntry):
        """
        Adds a single entry to the table if it has security relevance.
        Handles large datasets by limiting the number of displayed 'Normal' entries.
        """
        # Configuration
        MAX_NORMAL_ENTRIES = 1000
        
        is_suspicious = entry.severity > 0 or entry.decoded_payload
        
        # If normal entry and we have enough, skip adding to UI (optimization)
        if not is_suspicious:
            # We can just count it or ignore it for the visual table
            # Check current row count to estimate (rough heuristic)
            # Actually, let's track how many normal entries we have added
            # But simpler: if table has > 2000 rows and this is normal, ignore.
            if self.findings_table.rowCount() > 2000:
                return

        # self.all_entries.append(entry) # Don't store everything in memory forever if it's huge
        if is_suspicious:
             self.all_entries.append(entry)
        
        row = self.findings_table.rowCount()
        self.findings_table.insertRow(row)
            
        # Timestamp
        self.findings_table.setItem(row, 0, QTableWidgetItem(str(entry.timestamp)))
        
        # Severity
        sev_item = QTableWidgetItem(str(entry.severity))
        if entry.severity >= 80:
            sev_item.setForeground(Qt.GlobalColor.red)
            sev_item.setBackground(Qt.GlobalColor.darkRed)
        elif entry.severity >= 50:
            sev_item.setForeground(Qt.GlobalColor.yellow)
        self.findings_table.setItem(row, 1, sev_item)
        
        # Attack Type
        self.findings_table.setItem(row, 2, QTableWidgetItem(entry.attack_type or ("Suspicious" if is_suspicious else "Info")))
        
        # Payload
        payload_text = entry.decoded_payload if entry.decoded_payload else entry.url
        # Set item for sorting/data purposes
        payload_item = QTableWidgetItem(payload_text)
        payload_item.setToolTip(payload_text) # Show full text on hover
        self.findings_table.setItem(row, 3, payload_item)
        
        # Removed QTextEdit for performance (thousands of widgets cause crashes/lag)
        # Users can use the "Copy" button or double-click to view details (to be implemented if needed)
        
        # Source IP
        self.findings_table.setItem(row, 4, QTableWidgetItem(entry.source_ip))

        # Scroll to bottom
        self.findings_table.scrollToBottom()

    def update_recommendations(self):
        """
        Refreshes the recommendation panel based on aggregated findings.
        """
        recommendations = Recommender.get_recommendations(self.all_entries)
        if not recommendations:
            return

        text = "<h2>ACTION REQUIRED</h2><ul>"
        for attack, steps in recommendations.items():
            text += f"<li><b>{attack}</b>:<ul>"
            for step in steps:
                text += f"<li>{step}</li>"
            text += "</ul></li><br>"
        text += "</ul>"
        
        self.rec_label.setText(text)

    def copy_all_to_clipboard(self):
        """
        Copies all findings to the clipboard.
        """
        if not self.all_entries:
            return

        text_data = []
        headers = ["Timestamp", "Severity", "Attack Type", "Valid Payload (Decoded)", "Source IP"]
        text_data.append("\t".join(headers))

        for entry in self.all_entries:
            row_data = [
                str(entry.timestamp),
                str(entry.severity),
                entry.attack_type or "Suspicious",
                entry.decoded_payload if entry.decoded_payload else entry.url,
                entry.source_ip or ""
            ]
            text_data.append("\t".join(row_data))

        QApplication.clipboard().setText("\n".join(text_data))
        
    def export_to_csv(self):
        """
        Exports all findings to a CSV file.
        """
        if not self.all_entries:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Findings", "findings.csv", "CSV Files (*.csv)"
        )
        
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Header
                writer.writerow(["Timestamp", "Severity", "Attack Type", "Payload", "Source IP"])
                
                # Data
                for entry in self.all_entries:
                    writer.writerow([
                        entry.timestamp,
                        entry.severity,
                        entry.attack_type or "Suspicious",
                        entry.decoded_payload if entry.decoded_payload else entry.url,
                        entry.source_ip
                    ])
            
            QMessageBox.information(self, "Export Successful", f"Findings exported to {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export findings:\n{str(e)}")
