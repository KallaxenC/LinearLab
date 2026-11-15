from PySide6.QtWidgets import QApplication, QMessageBox, QWidget, QDialog, QVBoxLayout, QPlainTextEdit
from PySide6.QtCore import QFile, QObject, Signal
from PySide6.QtUiTools import QUiLoader
import logging
import json
import os
import sys
import subprocess

active_sub_windows = []

class LogEmitter(QObject):
    message = Signal(str)

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
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"

    process = subprocess.Popen(
        [
            sys.executable,
            "-u",
            render_worker_path,
            json.dumps(request),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        cwd=render_base_directory,
        env=environment,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )

    for line in process.stdout:
        message = line.rstrip("\r\n")
        if message:
            log_emitter.message.emit(message)

    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"Manim worker exited with code {return_code}")


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
            print(f"Error: Could not find 'window' variable in {file_path}")
    except Exception as e:
        print(f"Error launching {display_name}: {e}")



app = QApplication([])

loader = QUiLoader()

file = QFile('main.ui')
file.open(QFile.ReadOnly)
window = loader.load(file)
file.close()
window.setWindowTitle('LinearLab')
render_base_directory = os.path.dirname(os.path.abspath(__file__))
render_worker_path = os.path.join(render_base_directory, "render_worker.py")

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

#Launch all the matrix apps on startup
launch_sub_ui('Unit_Square_GUI.py', 'Unit Square')
launch_sub_ui('Unit_Cube_GUI.py', 'Unit Cube')
launch_sub_ui('2D_Vector_GUI.py', '2D Vector')
launch_sub_ui('3D_Vector_GUI.py', '3D Vector')

if window.mainStackedWidget.count() > 0:
    window.mainStackedWidget.setCurrentIndex(0)
    window.mainStackedWidget.setCurrentIndex(0)
    window.modeComboBox.setCurrentIndex(0)
window.showMaximized()

app.exec()
