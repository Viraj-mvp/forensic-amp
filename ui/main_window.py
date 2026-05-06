from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QFrame, QLabel
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
import os
from ui.dashboard import Dashboard
from ui.timeline import TimelineWidget
from ui.findings import FindingsPanel

class MainWindow(QMainWindow):
    """
    Main Application Window holding the sidebar and stacked pages.
    """
    def __init__(self):
        super().__init__()
        
        # Set Window Icon
        logo_path = os.path.join(os.path.dirname(__file__), "logo_icon.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # --- Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(250)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(10)
        
        # Title
        # title = QLabel("FORENSIC\nAMP")
        # title.setStyleSheet("font-size: 24pt; font-weight: bold; color: #00FF00;")
        # title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.sidebar_layout.addWidget(title)
        
        # Title Header (Logo + Text)
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "logo_transparent.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Smaller logo for header
            scaled_pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        
        # Text
        title_label = QLabel("FORENSIC\nAMP")
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #00FF00;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.sidebar_layout.addWidget(header_widget)
        
        self.sidebar_layout.addSpacing(20)
        
        # Navigation Buttons
        self.btn_dashboard = self.create_nav_btn("DASHBOARD", 0)
        self.btn_timeline = self.create_nav_btn("TIMELINE", 1)
        self.btn_findings = self.create_nav_btn("FINDINGS", 2)
        
        self.sidebar_layout.addWidget(self.btn_dashboard)
        self.sidebar_layout.addWidget(self.btn_timeline)
        self.sidebar_layout.addWidget(self.btn_findings)
        
        self.sidebar_layout.addStretch()
        
        # Version
        version = QLabel("v1.0.0-IND")
        version.setStyleSheet("color: #005500;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(version)
        
        self.main_layout.addWidget(self.sidebar)
        
        # --- content Area ---
        self.stack = QStackedWidget()
        
        # Pages
        self.dashboard_page = Dashboard()
        self.timeline_page = TimelineWidget()
        self.findings_page = FindingsPanel()
        
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.timeline_page)
        self.stack.addWidget(self.findings_page)
        
        self.main_layout.addWidget(self.stack)
        
        # Connect Signals
        self.dashboard_page.entry_processed.connect(self.process_entry)
        self.dashboard_page.analysis_finished.connect(self.on_analysis_finished)
        
        # Default Page
        self.btn_dashboard.setChecked(True)

    def create_nav_btn(self, text, index):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self.switch_page(index, btn))
        return btn

    def switch_page(self, index, btn):
        self.stack.setCurrentIndex(index)
        # Uncheck others
        self.btn_dashboard.setChecked(False)
        self.btn_timeline.setChecked(False)
        self.btn_findings.setChecked(False)
        btn.setChecked(True)

    def process_entry(self, entry):
        """
        Distribute processed entry to other widgets.
        """
        self.findings_page.add_entry(entry)
        if entry.timestamp:
            self.timeline_page.add_point(entry.timestamp, entry.severity)

    def on_analysis_finished(self):
        """
        Finalize analysis.
        """
        self.timeline_page.update_plot()
        self.findings_page.update_recommendations()
        
        # Auto-switch to findings if something bad was found (optional UX)
        # self.switch_page(2, self.btn_findings)
