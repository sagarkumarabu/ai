# net_speed_tray.py
# Shows live network speed (bytes/sec) in a tiny transparent always-on-top window
# placed near the bottom-right (taskbar area). Refresh interval = 1s.
#
# Requirements: psutil, PyQt5
# pip install psutil PyQt5

import sys
import psutil
from PyQt5 import QtCore, QtGui, QtWidgets

class NetSpeedWidget(QtWidgets.QWidget):
    UPDATE_INTERVAL_MS = 1000

    def __init__(self, offset_x=10, offset_y=10):
        super().__init__(flags=QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # Transparent window
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # Optional: allow mouse clicks to pass through (click-through)
        # NOTE: click-through may prevent interacting with the window (no context menu).
        # Uncomment the next line if you want the window to be non-interactive:
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        # Remove from task switcher (optional)
        self.setWindowFlag(QtCore.Qt.Tool)
        self.setWindowTitle("NetSpeed")

        # Display label
        self.label = QtWidgets.QLabel("-- B/s", self)
        font = QtGui.QFont("Consolas", 11, QtGui.QFont.Bold)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # White text with slight drop shadow effect for readability
        self.label.setStyleSheet("""
            color: white;
        """)

        # Effect: drop shadow to make text readable on different backgrounds
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(0, 0)
        shadow.setColor(QtGui.QColor(0, 0, 0, 200))
        self.label.setGraphicsEffect(shadow)

        # margin padding so text isn't flush to edges
        self.label.setContentsMargins(8, 6, 8, 6)

        # layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        # set fixed size based on label metrics
        self.resize(150, 34)

        # position near bottom-right
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.reposition()

        # network counters
        self.prev_bytes = self.get_total_bytes()
        # timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(self.UPDATE_INTERVAL_MS)

        # allow dragging if not click-through (optional)
        self._drag_pos = None

    def reposition(self):
        screen = QtWidgets.QApplication.primaryScreen()
        rect = screen.availableGeometry()  # excludes taskbar on many systems
        # If availableGeometry excludes taskbar, we can anchor to rect.bottom()
        x = rect.right() - self.width() - self.offset_x
        y = rect.bottom() - self.height() - self.offset_y
        self.move(x, y)

    def get_total_bytes(self):
        net = psutil.net_io_counters(pernic=False)
        return (net.bytes_sent or 0) + (net.bytes_recv or 0)

    def human_readable(self, b):
        # returns "123 B/s" or "1.2 KB/s" etc. Here user requested **bytes**, but human readable is helpful.
        # If you really want raw bytes, return f"{int(b)} B/s"
        unit = ["B/s", "KB/s", "MB/s", "GB/s"]
        val = float(b)
        i = 0
        while val >= 1024 and i < len(unit)-1:
            val /= 1024.0
            i += 1
        if i == 0:
            return f"{int(val)} {unit[i]}"
        else:
            return f"{val:.1f} {unit[i]}"

    def update_speed(self):
        cur = self.get_total_bytes()
        diff = cur - self.prev_bytes
        self.prev_bytes = cur
        # diff is bytes per UPDATE_INTERVAL_MS (i.e., per second here)
        if diff < 0:
            diff = 0
        # Show raw bytes/sec as integer:
        # text = f"{int(diff)} B/s"
        # Or nicer human readable:
        text = self.human_readable(diff)
        self.label.setText(text)
        # optionally resize widget to fit new text
        self.adjustSize()
        self.reposition()

    # Optional: allow dragging the widget if WA_TransparentForMouseEvents is off
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    # High DPI scaling
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    w = NetSpeedWidget(offset_x=12, offset_y=10)  # adjust offsets if needed
    w.show()
    # Keep on top and no taskbar icon
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
