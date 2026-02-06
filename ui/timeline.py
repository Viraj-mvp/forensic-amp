from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox
import pyqtgraph as pg
from datetime import datetime
import time

class TimelineWidget(QWidget):
    """
    Timeline visualization using PyQtGraph.
    Shows events over time, colored by severity.
    """
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.group = QGroupBox("TEMPORAL ANALYSIS")
        self.group_layout = QVBoxLayout()
        
        # Configure PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#000000')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setLabel('left', 'Severity')
        self.plot_widget.setLabel('bottom', 'Time')
        
        # Customizing axes to look "tech"
        self.plot_widget.getAxis('bottom').setPen('#00FF00')
        self.plot_widget.getAxis('left').setPen('#00FF00')
        
        self.scatter_item = pg.ScatterPlotItem(
            size=10, 
            pen=pg.mkPen(None), 
            brush=pg.mkBrush(0, 255, 0, 120)
        )
        self.plot_widget.addItem(self.scatter_item)
        
        self.group_layout.addWidget(self.plot_widget)
        self.group.setLayout(self.group_layout)
        self.layout.addWidget(self.group)

        self.timestamps = []
        self.severities = []
        self.brushes = []

    def add_point(self, timestamp: datetime, severity: int):
        try:
            ts_float = timestamp.timestamp()
            self.timestamps.append(ts_float)
            self.severities.append(severity)
            
            # Color coding based on severity
            if severity >= 80:
                self.brushes.append(pg.mkBrush(255, 0, 0, 200)) # Red
            elif severity >= 50:
                self.brushes.append(pg.mkBrush(255, 255, 0, 200)) # Yellow
            else:
                self.brushes.append(pg.mkBrush(0, 255, 0, 150)) # Green
            
            # Optimization: Don't replot on every single point for massive files
            # But for "streaming" feel, maybe every 10 or 50 points
            if len(self.timestamps) % 10 == 0:
                self.update_plot()
                
        except Exception:
            pass

    def update_plot(self):
        self.scatter_item.setData(
            x=self.timestamps, 
            y=self.severities, 
            brush=self.brushes
        )
