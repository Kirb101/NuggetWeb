import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QUrl
from PyQt5.QtGui import QIcon, QFont, QCursor, QPalette
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from win32mica import ApplyMica, MicaTheme, MicaStyle
from darkdetect import isDark
from PyQt5.QtMultimedia import QSoundEffect

class MoveWindowButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Move Window")
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("QPushButton { color: white; border-radius: 5px; }"
                           "QPushButton:hover { background-color: #00599e; }"
                           "QPushButton:checked { background-color: #00599e; }")
        self.setCheckable(True)
        self.setChecked(False)
        self.setCursor(Qt.ArrowCursor)
        self.window_drag_position = None
        self.setFixedSize(100, 25)

    def mousePressEvent(self, event):
        if self.isChecked():
            self.window_drag_position = event.globalPos() - self.parent().pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.isChecked() and event.buttons() == Qt.LeftButton:
            self.parent().move(event.globalPos() - self.window_drag_position)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NuggetWeb")
        self.setWindowIcon(QIcon("window.ico"))
        self.setGeometry(100, 100, 1500, 900)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")

        self.play_startup_sound()
        self.apply_mica_effect()
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)

        self.move_window_button = MoveWindowButton(self)
        self.move_window_button.clicked.connect(self.toggle_move_window)

        self.close_button = QPushButton("", self)
        self.close_button.setFont(QFont("Segoe Fluent Icons", 12))
        self.close_button.setFixedSize(25, 25)
        self.close_button.clicked.connect(self.animate_close)
        
        self.maximize_button = QPushButton("", self)
        self.maximize_button.setFont(QFont("Segoe Fluent Icons", 12))
        self.maximize_button.setFixedSize(25, 25)
        self.maximize_button.clicked.connect(self.showMaximized)

        self.minimize_button = QPushButton("", self)
        self.minimize_button.setFont(QFont("Segoe Fluent Icons", 12))
        self.minimize_button.setFixedSize(25, 25)
        self.minimize_button.clicked.connect(self.showMinimized)
        
        self.prev_page_button = QPushButton("", self)
        self.prev_page_button.setFont(QFont("Segoe Fluent Icons", 12))
        self.prev_page_button.setFixedSize(25, 25)
        self.prev_page_button.clicked.connect(self.go_to_prev_page)
        
        self.next_page_button = QPushButton("", self)
        self.next_page_button.setFont(QFont("Segoe Fluent Icons", 12))
        self.next_page_button.setFixedSize(25, 25)
        self.next_page_button.clicked.connect(self.go_to_next_page)
        
        self.url_line_edit = QLineEdit(self)
        self.url_line_edit.setPlaceholderText("Enter URL")
        self.url_line_edit.returnPressed.connect(self.load_url)
        self.url_line_edit.setFont(QFont("Segoe UI", 10))
        self.url_line_edit.setFixedHeight(25)
        self.url_line_edit.setStyleSheet("QLineEdit { border-radius: 5px; }")
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.move_window_button)
        bottom_layout.addWidget(self.close_button)
        bottom_layout.addWidget(self.maximize_button)
        bottom_layout.addWidget(self.minimize_button)
        bottom_layout.addWidget(self.url_line_edit, 2)
        bottom_layout.addWidget(self.prev_page_button)
        bottom_layout.addWidget(self.next_page_button)
        bottom_layout.setSpacing(10)
        bottom_layout.setContentsMargins(10, 0, 10, 0)
        
        main_layout = QVBoxLayout()
        
        self.webview = QWebEngineView()
        self.webview.load(QUrl.fromLocalFile("\Homepage.html"))
        
        main_layout.addWidget(self.webview)
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)

        self.set_button_color()

    def apply_mica_effect(self):
        hwnd = self.winId().__int__()

        if isDark():
            mode = MicaTheme.DARK
        else:
            mode = MicaTheme.LIGHT
        style = MicaStyle.DEFAULT
        
        ApplyMica(HWND=hwnd, Theme=mode, Style=style)
    
    def animate_close(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        current_rect = self.geometry()
        target_rect = QRect(current_rect.x(), current_rect.y() + current_rect.height(), current_rect.width(), current_rect.height())
        self.animation.setStartValue(current_rect)
        self.animation.setEndValue(target_rect)
        self.animation.finished.connect(self.close)
        self.animation.start()
    
    def toggle_move_window(self):
        if self.move_window_button.isChecked():
            self.setCursor(Qt.ClosedHandCursor)
            if not hasattr(self, 'window_drag_position'):
                self.window_drag_position = self.pos() - self.mapFromGlobal(QCursor.pos())
        else:
            self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if self.move_window_button.isChecked():
            self.window_drag_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.move_window_button.isChecked():
            self.move(event.globalPos() - self.window_drag_position)
    
    def load_url(self):
        url = self.url_line_edit.text()
        if url.startswith("http://") or url.startswith("https://"):
            self.webview.load(QUrl(url))
        else:
            self.webview.load(QUrl("http://" + url))
    
    def go_to_prev_page(self):
        self.webview.page().triggerAction(QWebEnginePage.Back)
    
    def go_to_next_page(self):
        self.webview.page().triggerAction(QWebEnginePage.Forward)
    
    def set_button_color(self):
        palette = self.palette()
        accent_color = palette.color(QPalette.Highlight)
        button_style = "QPushButton { color: white; border-radius: 5px; background-color: %s; }"
        button_stylesheet = button_style % accent_color.name()
        self.move_window_button.setStyleSheet(button_stylesheet)
        self.close_button.setStyleSheet(button_stylesheet)
        self.maximize_button.setStyleSheet(button_stylesheet)
        self.minimize_button.setStyleSheet(button_stylesheet)
        self.prev_page_button.setStyleSheet(button_stylesheet)
        self.next_page_button.setStyleSheet(button_stylesheet)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            if url.isLocalFile() and url.toLocalFile().endswith('.html'):
                self.webview.load(QUrl.fromLocalFile(url.toLocalFile()))

    def update_window_title(self, title):
        self.setWindowTitle(f"NuggetWeb - {title}")

    def play_startup_sound(self):
        sound_effect = QSoundEffect()
        sound_effect.setSource(QUrl.fromLocalFile(".\\startup.wav"))
        sound_effect.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
