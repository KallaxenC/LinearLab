from PySide6.QtWidgets import QApplication, QMessageBox, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
import sys
import subprocess

active_sub_windows = []

def launch_sub_ui(file_path, display_name):
    try:
        with open(file_path, 'r') as file:
            sub_app_code = file.read()

        context = {}

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


while window.mainStackedWidget.count() > 0:
    window.mainStackedWidget.removeWidget(window.mainStackedWidget.widget(0))

window.modeComboBox.currentIndexChanged.connect(window.mainStackedWidget.setCurrentIndex)

#Launch all the matrix apps on startup
launch_sub_ui('Unit_Square_GUI.py', 'Unit Square')
launch_sub_ui('Unit_Cube_GUI.py', 'Unit Cube')
launch_sub_ui('2D_Vector_GUI.py', '2D Vector')
launch_sub_ui('3D_Vector_GUI.py', '3D Vector')

if window.mainStackedWidget.count() > 0:
    window.mainStackedWidget.setCurrentIndex(0)
    window.mainStackedWidget.setCurrentIndex(0)
    window.modeComboBox.setCurrentIndex(0)
window.show()

app.exec()
