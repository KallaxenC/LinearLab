from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
import os

app = QApplication()

loader = QUiLoader()

def open_Unit_Square_GUI():
    os.startfile("Unit_Square_GUI.py")
def open_Unit_Cube_GUI():
    os.startfile("Unit_Cube_GUI.py")
def open_2D_Vector_GUI():
    os.startfile("2D_Vector_GUI.py")
def open_3D_Vector_GUI():
    os.startfile("3D_Vector_GUI.py")

file = QFile('main.ui')
file.open(QFile.ReadOnly)
window = loader.load(file)
file.close()
window.setWindowTitle('Matrix Visualiser')

window.unitSquare_Button.clicked.connect(open_Unit_Square_GUI)
window.unitCube_Button.clicked.connect(open_Unit_Cube_GUI)
window.twoDVector_Button.clicked.connect(open_2D_Vector_GUI)
window.threeDVector_Button.clicked.connect(open_3D_Vector_GUI)

window.show()

app.exec()

