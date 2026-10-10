from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from unit_square_animator import UnitSquareTransformation
from manim import config
from matrix_video_finder import find_matrix_video
import os

app = QApplication()

loader = QUiLoader()

def search_for_video(a,b,c,d):
    result = find_matrix_video(a,b,c,d)
    return result

def visualise():
    a = float(window.a_value.text())
    b = float(window.b_value.text())
    c = float(window.c_value.text())
    d = float(window.d_value.text())
    
    matrix = [[a, b],
              [c, d]]

    if search_for_video(a,b,c,d):
        os.startfile(search_for_video(a,b,c,d))
        return
    
    QMessageBox.information(window, 'Video Generation', 'Visualising the transformation and generating video...')
    values = f"{str(a)}{str(b)}{str(c)}{str(d)}"
    print(f"Values: {values}")
    scene = UnitSquareTransformation(matrix)

    print("Processing...")

    config.preview = True                         
    config.quality = "medium_quality"                
    print(f"Output file name: matrix_animation_{values}")
    config.output_file = f"matrix_animation_{values}"   

    scene = UnitSquareTransformation(matrix=matrix)
        
    scene.render()


file = QFile('main.ui')
file.open(QFile.ReadOnly)
window = loader.load(file)
file.close()
window.setWindowTitle('Matrix Visualiser')

window.visualiseButton.clicked.connect(visualise)

window.show()

app.exec()

