import logging
import sys
import threading
import traceback

from resources import (
    app_data_path,
    configure_frozen_stdio,
    resource_path,
)

configure_frozen_stdio()

from PySide6.QtWidgets import QApplication, QMessageBox, QWidget, QDialog, QVBoxLayout, QPlainTextEdit
from PySide6.QtCore import QFile, QObject, Signal
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
import icon_resources_rc

def report_unhandled_exception(exc_type, exc_value, exc_traceback):
    error_text = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )
    log_path = app_data_path() / "startup.log"
    log_path.write_text(error_text, encoding="utf-8")

    if QApplication.instance() is not None:
        QMessageBox.critical(
            None,
            "LinearLab startup error",
            f"LinearLab could not start.\n\nDetails were written to:\n{log_path}",
        )


sys.excepthook = report_unhandled_exception

active_sub_windows = []

#Used further down to report command line outputs and stuff
class LogEmitter(QObject):
    message = Signal(str)


class QtLogStream:
    encoding = "utf-8"

    def __init__(self, message_signal):
        self._emit_message = message_signal.emit
        self._buffer = ""
        self._lock = threading.Lock()

    def write(self, text):
        if not isinstance(text, str):
            text = str(text)

        messages = []
        with self._lock:
            for character in text:
                if character in "\r\n":
                    if self._buffer.strip():
                        messages.append(self._buffer)
                    self._buffer = ""
                else:
                    self._buffer += character

        for message in messages:
            self._emit_message(message)
        return len(text)

    def flush(self):
        with self._lock:
            message = self._buffer
            self._buffer = ""

        if message.strip():
            self._emit_message(message)

    def isatty(self):
        return False

    def writable(self):
        return True


class QtLogHandler(logging.Handler):
    def __init__(self, emitter):
        super().__init__()
        self.emitter = emitter

    def emit(self, record):
        try:
            self.emitter.message.emit(self.format(record))
        except Exception:
            self.handleError(record)


def run_manim_worker(request):
    from render_worker import render_manim_request

    render_manim_request(request)


def show_functions_info():
    from menuBar_texts import functions_text
    QMessageBox.information( 
        window,
        'Functions Information', 
        functions_text()
        )

def launch_sub_ui(file_path, display_name):
    try:
        with open(file_path, 'r') as file:
            sub_app_code = file.read()

        context = {"run_manim_worker": run_manim_worker}

        exec(sub_app_code, context)

        sub_window_widget = context.get("sub_window")

        if sub_window_widget:
            active_sub_windows.append(sub_window_widget)

            from PySide6.QtCore import Qt
            sub_window_widget.setWindowFlags(Qt.Widget)
            new_index = window.mainStackedWidget.addWidget(sub_window_widget)
            window.modeComboBox.addItem(display_name)

            window.mainStackedWidget.setCurrentIndex(new_index)

        else:
            print(f"Could not find the file: {file_path}. Have you deleted it by accident?")
    except Exception as e:
        print(f"Error launching {display_name}: {e}")



app = QApplication([])

loader = QUiLoader()

file = QFile(str(resource_path('main.ui')))
file.open(QFile.ReadOnly)
window = loader.load(file)
file.close()
window.setWindowIcon(QIcon(":/icons/linearlab.png"))
window.setWindowTitle('LinearLab')

log_dialog = QDialog(window)
log_dialog.setMinimumWidth(500)
log_dialog.setMinimumHeight(300)
log_dialog.setWindowTitle("Video Progress Log")
log_dialog.setModal(False)

log_output = QPlainTextEdit(log_dialog)
log_output.setReadOnly(True)
log_output.setMaximumBlockCount(300)

layout = QVBoxLayout(log_dialog)
layout.addWidget(log_output)

#Calling the log class that im pretty sure pyside 6 handles
log_emitter = LogEmitter(window)
log_emitter.message.connect(log_output.appendPlainText)
if getattr(sys, "frozen", False):
    log_stream = QtLogStream(log_emitter.message)
    sys.stdout = log_stream
    sys.stderr = log_stream

manim_handler = QtLogHandler(log_emitter)
manim_handler.setLevel(logging.INFO)
manim_handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(message)s")
)

logging.getLogger("manim").addHandler(manim_handler)

window.openProgressLogAction.triggered.connect(log_dialog.show)

while window.mainStackedWidget.count() > 0:
    window.mainStackedWidget.removeWidget(window.mainStackedWidget.widget(0))

window.modeComboBox.currentIndexChanged.connect(window.mainStackedWidget.setCurrentIndex)
window.functionsAction.triggered.connect(show_functions_info)

#Launch all the matrix apps on startup, list any new files / sub apps I create here
launch_sub_ui(resource_path('Unit_Square_GUI.py'), 'Unit Square')
launch_sub_ui(resource_path('Unit_Cube_GUI.py'), 'Unit Cube')
launch_sub_ui(resource_path('2D_Vector_GUI.py'), '2D Vector')
launch_sub_ui(resource_path('3D_Vector_GUI.py'), '3D Vector')

if window.mainStackedWidget.count() > 0:
    window.mainStackedWidget.setCurrentIndex(0)
    window.mainStackedWidget.setCurrentIndex(0)
    window.modeComboBox.setCurrentIndex(0)
window.showMaximized()

app.exec()
