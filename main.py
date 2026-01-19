import sys
import os
import signal
import json
from PyQt5.QtCore import Qt, QUrl, QEvent, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

# --- 配置区 ---
# 设置默认启动时加载的模型
INITIAL_MODEL_NAME = "lafei_4"
# --- 配置区 ---

# 允许读取本地文件 (对于某些系统仍然需要)
signal.signal(signal.SIGINT, signal.SIG_DFL)
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-web-security --allow-file-access-from-files"

class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, line, sourceID):
        print(f"[JS Log] {message} (Line: {line}, Source: {sourceID})")

class Live2DDesktop(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.model_name = INITIAL_MODEL_NAME
        self.character_data = None
        self.load_character_data()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(500, 800)

        self.browser = QWebEngineView()
        self.page = WebEnginePage(self.browser)
        self.browser.setPage(self.page)
        self.browser.page().setBackgroundColor(Qt.transparent)
        
        self.browser.page().titleChanged.connect(self.handle_title_change)
        self.browser.loadFinished.connect(self.on_load_finished)
        
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)
        
        current_dir = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/')
        self.browser.load(QUrl.fromLocalFile(f"{current_dir}/index2.html"))
        self.setCentralWidget(self.browser)
        
        self.browser.installEventFilter(self)
        if self.browser.focusProxy():
            self.browser.focusProxy().installEventFilter(self)
        self.old_pos = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_eyes)
        self.timer.start(30)

    def load_character_data(self):
        """根据 self.model_name 加载角色数据"""
        try:
            with open(f"{self.model_name}/character_data.json", "r", encoding="utf-8") as f:
                self.character_data = json.load(f)
            print(f"[Info] Loaded data for model: {self.model_name}")
            return True
        except FileNotFoundError:
            QMessageBox.critical(self, "错误", f"模型配置 '{self.model_name}/character_data.json' 未找到！")
            return False
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载或解析 '{self.model_name}/character_data.json' 失败: {e}")
            return False

    def on_load_finished(self, success):
        """页面加载或模型切换后，将Python中的数据注入到JS环境中。"""
        if not success:
            print("[Error] Page failed to load!")
            return
            
        print("[Info] Page ready. Injecting data from Python...")
        
        self.browser.page().runJavaScript("window.isDesktop = true;")
        
        if self.character_data:
            json_data_string = json.dumps(self.character_data)
            js_code = f"window.initialize('{self.model_name}', {json_data_string});"
            self.browser.page().runJavaScript(js_code)
            print(f"[Info] Injected data for model: {self.model_name}")

    def handle_title_change(self, title):
        """处理来自JS的指令"""
        if title == "CMD:QUIT":
            self.quit_app()
        elif title.startswith("CMD:RELOAD:"):
            new_model_name = title.split(":", 2)[2]
            print(f"[Info] Received switch command for model: {new_model_name}")
            self.model_name = new_model_name
            if self.load_character_data():
                # 重新调用 on_load_finished 来注入新模型的数据
                self.on_load_finished(True)

    def update_eyes(self):
        cursor = QCursor.pos()
        local_pos = self.mapFromGlobal(cursor)
        dx = local_pos.x() - self.width() // 2
        dy = local_pos.y() - self.height() // 2
        js = f"if(window.updateFocus) window.updateFocus({dx * 1.2}, {dy * 1.2});"
        self.browser.page().runJavaScript(js)
    
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
        elif event.type() == QEvent.MouseMove and self.old_pos is not None:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()
        elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            self.old_pos = None
        elif event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.quit_app()
                return True
            if event.key() == Qt.Key_Space:
                self.browser.page().runJavaScript("if(window.model) window.playMotionWithVoice('TapBody');")
                return True
                
        return super().eventFilter(source, event)

    def quit_app(self):
        print("正在退出...")
        self.timer.stop()
        self.browser.stop()
        self.close()
        QApplication.instance().quit()

    def closeEvent(self, event):
        self.quit_app()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Live2DDesktop()
    window.show()
    sys.exit(app.exec_())