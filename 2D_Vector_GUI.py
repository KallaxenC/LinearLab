from PySide6.QtWidgets import QApplication, QMessageBox, QHBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader
from TwoD_vector_animator import TwoDVectorTransformation, TwoDVectorTransformationWithCoordinates
from manim import config
from matrix_video_finder import find_matrix_video
import os
from maths_syntaxer import interpretInput

app = QApplication()

loader = QUiLoader()

vector_rows = []


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

def add_vector():

    vector_count = len(vector_rows) + 2 
    
    new_label = QLabel(f"Enter 2D vector {vector_count}:")
    new_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    row_layout = QHBoxLayout()
    row_boxes = []
    
    open_bracket = QLabel(" ( ")
    row_layout.addWidget(open_bracket)
    
    for i in range(2):
        box = QLineEdit()
        box.setPlaceholderText("0")
        row_layout.addWidget(box)
        row_boxes.append(box)
        
        if i < 1:
            comma = QLabel(" , ")
            row_layout.addWidget(comma)
            
    close_bracket = QLabel(" ) ")
    row_layout.addWidget(close_bracket)
        
    target_layout = window.scrollArea_verticalLayout
    target_layout.addWidget(new_label)
    target_layout.addLayout(row_layout)
    
    vector_rows.append((new_label, row_boxes, row_layout))


def remove_vector():
    if not vector_rows:
        return 
        
    label, boxes, row_layout = vector_rows.pop()
    
    for box in boxes:
        box.deleteLater()
    row_layout.deleteLater()
    
    label.deleteLater()

def get_all_vectors():
    all_vectors = []
    
    try:
        v1_x = float(interpretInput(window.vector1_x.text())) or 0
        v1_y = float(interpretInput(window.vector1_y.text())) or 0
        #v1_z = float(window.vector1_z.text() or 0)
        all_vectors.append([v1_x, v1_y])
    except AttributeError:
        print("Warning: Could not read default vector boxes. Ensure names match your UI.")

    for label, boxes, layout in vector_rows:
        try:
            x = float(interpretInput(boxes[0].text())) or 0
            y = float(interpretInput(boxes[1].text())) or 0
            #z = float(boxes[2].text() or 0)
            all_vectors.append([x, y])
        except ValueError:
            all_vectors.append([0.0, 0.0])
            
    return all_vectors


def visualise():
    try:
        a = float(interpretInput(window.a_value.text()))
        b = float(interpretInput(window.b_value.text()))
        c = float(interpretInput(window.c_value.text()))
        d = float(interpretInput(window.d_value.text()))
        

    except:
        QMessageBox.information(window, 'Input Error', 'An unknown function or invalid values have been inputted. Please check or change your inputs and try again.')
        return
    
    user_vectors = get_all_vectors()
    matrix = [[a, b],
              [c, d]]
              
    print(f"Vectors to transform: {user_vectors}")
    vector_values = "".join(str(num) for vector in user_vectors for num in vector)
    values = f"{str(a)}{str(b)}{str(c)}{str(d)}{vector_values}"
    
    QMessageBox.information(window, 'Video Generation', 'Visualising the transformation and generating video...')
    
    print(f"Values: {values}")
    

    print("Processing...")
    if window.inverseMatrix_checkBox.isChecked():
        show_inverse = 1
    else:
        show_inverse = 0
    if window.coordinates_checkBox.isChecked():
        print("Showing coords")
        file_type = "2D_vector_with_coords"
    else:
        file_type = "2D_vector"

    video_quality = get_video_quality()
    video_history = find_matrix_video(file_type, video_quality, values)
    if video_history != None:
        os.startfile(video_history)
        return

    config.preview = True
    config.quality = video_quality
    print(video_quality)
    print(f"Output file name: matrix_animation_{values}_{file_type}")
    config.output_file = f"matrix_animation_{values}_{file_type}"

    if window.coordinates_checkBox.isChecked():
        scene = TwoDVectorTransformationWithCoordinates(show_inverse, matrix, user_vectors)
    else:
        scene = TwoDVectorTransformation(show_inverse, matrix, user_vectors)

    scene.render()


file = QFile('2D_vector.ui')
file.open(QFile.ReadOnly)
window = loader.load(file)
file.close()
window.setWindowTitle('Matrix Visualiser')

# --- Button Connections ---
window.visualiseButton.clicked.connect(visualise)
window.addVectorButton.clicked.connect(add_vector)       # Action for adding rows
window.removeVectorButton.clicked.connect(remove_vector) # Action for clearing rows
window.show()

app.exec()
