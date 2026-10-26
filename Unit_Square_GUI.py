from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from unit_square_animator import UnitSquareTransformation
from manim import config
from matrix_video_finder import find_matrix_video
import os
from maths_syntaxer import interpretInput

app = QApplication()

loader = QUiLoader()

#define the video file type
file_type = "unit_square"

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

def visualise():
    try:
        a = float(interpretInput(window.a_value.text()))
        b = float(interpretInput(window.b_value.text()))
        c = float(interpretInput(window.c_value.text()))
        d = float(interpretInput(window.d_value.text()))
    except:
        QMessageBox.information(window, 'Input Error', 'An unknown function or invalid values have been inputted. Please check or change your inputs and try again.')
        return

    matrix = [[a, b],
              [c, d]]

    values = f"{str(a)}{str(b)}{str(c)}{str(d)}"
    video_history = find_matrix_video(file_type,get_video_quality(),values)
    if video_history != None:
        os.startfile(video_history)
        return
    
    QMessageBox.information(window, 'Video Generation', 'Visualising the transformation and generating video...')
    
    print(f"Values: {values}")

    print("Processing...")

    config.preview = True                         
    config.quality = get_video_quality()             
    print(f"Output file name: matrix_animation_{values}_{file_type}")
    config.output_file = f"matrix_animation_{values}_{file_type}"   

    if window.inverseMatrix_checkBox.isChecked():
        show_inverse = 1
    else:
        show_inverse = 0
    scene = UnitSquareTransformation(show_inverse, matrix=matrix)
        
    scene.render()


file = QFile('unit_square.ui')
file.open(QFile.ReadOnly)
window = loader.load(file)
file.close()
window.setWindowTitle('Matrix Visualiser')

window.visualiseButton.clicked.connect(visualise)

window.show()

app.exec()

