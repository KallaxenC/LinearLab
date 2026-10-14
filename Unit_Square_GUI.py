from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from unit_square_animator import UnitSquareTransformation
from manim import config
from matrix_video_finder import find_matrix_video_2D
import os

app = QApplication()

loader = QUiLoader()

def get_video_quality():
    selected_quality = window.quality_buttonGroup.checkedButton()

    if not selected_quality:
        video_quality = "medium_quality"
    elif selected_quality.objectName() == "lowQuality_radiobox":
        video_quality = "low_quality"
    elif selected_quality.objectName() == "mediumQuality_radiobox":
        video_quality = "medium_quality"
    elif selected_quality.objectName() == "highQuality_radiobox":
        video_quality = "high_quality"
    else:
        video_quality = "medium_quality"

    return video_quality

def search_for_video(quality,a,b,c,d):
    result = find_matrix_video_2D(quality,a,b,c,d)
    return result

def visualise():
    a = float(window.a_value.text())
    b = float(window.b_value.text())
    c = float(window.c_value.text())
    d = float(window.d_value.text())
    
    matrix = [[a, b],
              [c, d]]

    if search_for_video(get_video_quality(),a,b,c,d):
        os.startfile(search_for_video(get_video_quality(),a,b,c,d))
        return
    
    QMessageBox.information(window, 'Video Generation', 'Visualising the transformation and generating video...')
    values = f"{str(a)}{str(b)}{str(c)}{str(d)}"
    print(f"Values: {values}")

    print("Processing...")

    config.preview = True                         
    config.quality = get_video_quality()             
    print(f"Output file name: matrix_animation_{values}")
    config.output_file = f"matrix_animation_{values}"   

    scene = UnitSquareTransformation(matrix=matrix)
        
    scene.render()


file = QFile('unit_square.ui')
file.open(QFile.ReadOnly)
window = loader.load(file)
file.close()
window.setWindowTitle('Matrix Visualiser')

window.visualiseButton.clicked.connect(visualise)

window.show()

app.exec()

