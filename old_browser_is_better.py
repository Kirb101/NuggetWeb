import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QStatusBar, QFrame, QWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage
from win32mica import ApplyMica, MicaTheme, MicaStyle

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IceX")
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet("background-color: #333; color: white;")
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.settings = QWebEngineSettings.globalSettings()
        self.settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        main_layout = QVBoxLayout()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        main_layout.addWidget(frame)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        self.move_button = QPushButton("Move Window")
        self.move_button.setStyleSheet("color: white;")
        self.move_button.setCheckable(True)
        self.move_button.toggled.connect(self.toggle_move_window)
        self.status_bar.addWidget(self.move_button)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL here")
        self.url_bar.returnPressed.connect(self.navigate)
        self.status_bar.addWidget(self.url_bar)

        self.back_button = QPushButton("←")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setFixedSize(25, 25)
        self.status_bar.addWidget(self.back_button)

        self.forward_button = QPushButton("→")
        self.forward_button.clicked.connect(self.go_forward)
        self.forward_button.setFixedSize(25, 25)
        self.status_bar.addWidget(self.forward_button)

        self.refresh_button = QPushButton("")
        self.refresh_button.setStyleSheet("font-family: Segoe MDL2 Assets; color: white;")
        self.refresh_button.clicked.connect(self.refresh)
        self.refresh_button.setFixedSize(25, 25)
        self.status_bar.addWidget(self.refresh_button)

        self.close_button = QPushButton("")
        self.close_button.setStyleSheet("font-family: Segoe MDL2 Assets; color: white;")
        self.close_button.setFixedSize(25, 25)
        self.close_button.clicked.connect(self.close)
        self.status_bar.addPermanentWidget(self.close_button)

        self.maximize_button = QPushButton("")
        self.maximize_button.setStyleSheet("font-family: Segoe MDL2 Assets; color: white;")
        self.maximize_button.setFixedSize(25, 25)
        self.maximize_button.clicked.connect(self.showMaximized)
        self.status_bar.addPermanentWidget(self.maximize_button)

        self.minimize_button = QPushButton("")
        self.minimize_button.setStyleSheet("font-family: Segoe MDL2 Assets; color: white;")
        self.minimize_button.setFixedSize(25, 25)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.status_bar.addPermanentWidget(self.minimize_button)

        self.web_view = QWebEngineView()
        frame_layout.addWidget(self.web_view)

        self.load_default_homepage()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.show()

        window_hwnd = self.winId().__int__()
        status_bar_hwnd = self.status_bar.winId().__int__()
        mode = MicaTheme.DARK
        style = MicaStyle.DEFAULT

        ApplyMica(HWND=window_hwnd, Theme=mode, Style=style)
        ApplyMica(HWND=status_bar_hwnd, Theme=mode, Style=style)

    def load_default_homepage(self):
        self.web_view.load(QUrl.fromLocalFile("\Homepage.html"))

    def navigate(self):
        url = self.url_bar.text()
        if url:
            if not url.startswith("https://"):
                url = "https://" + url
            self.web_view.load(QUrl(url))

    def go_back(self):
        self.web_view.back()

    def go_forward(self):
        self.web_view.forward()

    def refresh(self):
        self.web_view.reload()

    def toggle_move_window(self, checked):
        if checked:
            self.setCursor(Qt.ClosedHandCursor)
            if not hasattr(self, 'window_drag_position'):
                self.window_drag_position = self.pos() - self.mapFromGlobal(QCursor.pos())
        else:
            self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if self.move_button.isChecked():
            self.window_drag_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.move_button.isChecked():
            self.move(event.globalPos() - self.window_drag_position)

    def keyPressEvent(self, event):
        if event.modifiers() == (Qt.ControlModifier | Qt.AltModifier | Qt.ShiftModifier) and event.key() == Qt.Key_A:
            self.show_popup()

    def show_popup(self):
        QMessageBox.information(self, "", "Version: IceX Binary (0.0.1)")

def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
