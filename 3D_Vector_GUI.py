from PySide6.QtWidgets import QApplication, QMessageBox, QHBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from ThreeD_vector_animator import ThreeDVectorTransformation, ThreeDVectorTransformationWithCoordinates
from manim import config
from matrix_video_finder import find_matrix_video
import os

app = QApplication()

loader = QUiLoader()
# define the file type
file_type = "3D_vector"

# --- Dynamic Row Tracker ---
# This list will store tuples: (label_widget, [box_x, box_y, box_z])
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
    """Adds a new text label and 3 line edits inside the scroll area layout with brackets and commas."""
    vector_count = len(vector_rows) + 2 
    
    new_label = QLabel(f"Enter 3D vector {vector_count}:")
    
    row_layout = QHBoxLayout()
    row_boxes = []
    
    open_bracket = QLabel(" ( ")
    row_layout.addWidget(open_bracket)
    
    for i in range(3):
        box = QLineEdit()
        box.setPlaceholderText("0")
        row_layout.addWidget(box)
        row_boxes.append(box)
        
        if i < 2:
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
        v1_x = float(window.vector1_x.text() or 0)
        v1_y = float(window.vector1_y.text() or 0)
        v1_z = float(window.vector1_z.text() or 0)
        all_vectors.append([v1_x, v1_y, v1_z])
    except AttributeError:
        print("UI Vector boxes arent matching the names in the code so fix it bruh")

    for label, boxes, layout in vector_rows:
        try:
            x = float(boxes[0].text() or 0)
            y = float(boxes[1].text() or 0)
            z = float(boxes[2].text() or 0)
            all_vectors.append([x, y, z])
        except ValueError:
            all_vectors.append([0.0, 0.0, 0.0])
            
    return all_vectors


def visualise():
    try:
        a = float(window.a_value.text())
        b = float(window.b_value.text())
        c = float(window.c_value.text())
        d = float(window.d_value.text())
        e = float(window.e_value.text())
        f = float(window.f_value.text())
        g = float(window.g_value.text())
        h = float(window.h_value.text())
        i = float(window.i_value.text())
    except ValueError:
        QMessageBox.information(window, 'Alert', 'One or more boxes did not contain a number.')
        return

    matrix = [[a, b, c],
              [d, e, f],
              [g, h, i]]
              
    user_vectors = get_all_vectors()
    print(f"Vectors to transform: {user_vectors}")
    vector_values = "".join(str(num) for vector in user_vectors for num in vector)
    values = f"{str(a)}{str(b)}{str(c)}{str(d)}{str(e)}{str(f)}{str(g)}{str(h)}{str(i)}{vector_values}"
    
    QMessageBox.information(window, 'Video Generation', 'Visualising the transformation and generating video...')
    
    print(f"Values: {values}")
    

    print("Processing...")
    if window.inverseMatrix_checkBox.isChecked():
        show_inverse = 1
    else:
        show_inverse = 0
     

    if window.coordinates_checkBox.isChecked():
        scene = ThreeDVectorTransformationWithCoordinates(show_inverse, matrix, user_vectors)
        print("Showing coords")
        file_type = "3D_vector_with_coords"
    else:
        scene = ThreeDVectorTransformation(show_inverse, matrix, user_vectors)
        file_type = "3D_vector"    
    

    video_history = find_matrix_video(file_type, get_video_quality(), values)
    if video_history != None:
        os.startfile(video_history)
        return

    config.preview = True                         
    config.quality = get_video_quality()
    print(get_video_quality())                
    print(f"Output file name: matrix_animation_{values}_{file_type}")
    config.output_file = f"matrix_animation_{values}_{file_type}"

    scene.render()


file = QFile('3D_vector.ui')
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
