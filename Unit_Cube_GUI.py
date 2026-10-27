from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from unit_cube_animator import CubeVertexTransformation
from manim import config
from matrix_video_finder import find_matrix_video
from maths_syntaxer import interpretInput
import os

app = QApplication()

loader = QUiLoader()
#define the file type
file_type = "unit_cube"


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
        e = float(interpretInput(window.e_value.text()))
        f = float(interpretInput(window.f_value.text()))
        g = float(interpretInput(window.g_value.text()))
        h = float(interpretInput(window.h_value.text()))
        i = float(interpretInput(window.i_value.text()))
    except:
        QMessageBox.information(window, 'Input Error', 'An unknown function or invalid values have been inputted. Please check or change your inputs and try again.')
        return

    matrix = [[a, b, c],
              [d, e, f],
              [g, h, i]]

    values = f"{str(a)}{str(b)}{str(c)}{str(d)}{str(e)}{str(f)}{str(g)}{str(h)}{str(i)}"
    show_inverse = window.inverseMatrix_checkBox.isChecked()
    show_coordinates = window.coordinates_checkBox.isChecked()
    file_type = "unit_cube"
    if show_coordinates:
        file_type = "unit_cube_with_coords"
    if show_inverse:
        file_type += "_inverse"

    video_quality = get_video_quality()
    video_history = find_matrix_video(file_type, video_quality, values)
    if video_history != None:
        os.startfile(video_history)
        return
    
    QMessageBox.information(window, 'Video Generation', 'Visualising the transformation and generating video...')
    
    print(f"Values: {values}")
    

    print("Processing...")

    config.preview = True                         
    config.quality = video_quality
    print(video_quality)                
    print(f"Output file name: matrix_animation_{values}_{file_type}")
    config.output_file = f"matrix_animation_{values}_{file_type}"   
    
    scene = CubeVertexTransformation(
        matrix,
        show_inverse=show_inverse,
        show_coordinates=show_coordinates,
    )
    scene.render()


file = QFile('unit_cube.ui')
file.open(QFile.ReadOnly)
window = loader.load(file)
file.close()
window.setWindowTitle('Matrix Visualiser')

window.visualiseButton.clicked.connect(visualise)

window.show()

app.exec()
