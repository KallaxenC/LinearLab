from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QSizePolicy,
    QProgressDialog,
)
from PySide6.QtCore import QFile, Qt, QUrl, QThread, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from ThreeD_vector_animator import ThreeDVectorTransformation, ThreeDVectorTransformationWithCoordinates
from manim import config
from matrix_video_finder import find_matrix_video
from maths_syntaxer import interpretInput
import os


class VideoRenderer(QThread):
    render_finished = Signal(str, bool)
    error = Signal(str)

    def __init__(
        self,
        show_inverse,
        matrix,
        user_vectors,
        file_type,
        video_quality,
        values,
        open_video_separately,
    ):
        super().__init__()
        self.show_inverse = show_inverse
        self.matrix = matrix
        self.user_vectors = user_vectors
        self.file_type = file_type
        self.video_quality = video_quality
        self.values = values
        self.open_video_separately = open_video_separately

    def run(self):
        try:
            config.preview = False
            config.quality = self.video_quality
            config.output_file = f"matrix_animation_{self.values}_{self.file_type}"

            if self.file_type == "3D_vector_with_coords":
                scene = ThreeDVectorTransformationWithCoordinates(
                    self.show_inverse, self.matrix, self.user_vectors
                )
            else:
                scene = ThreeDVectorTransformation(
                    self.show_inverse, self.matrix, self.user_vectors
                )
            scene.render()

            video_path = find_matrix_video(
                self.file_type, self.video_quality, self.values
            )
            self.render_finished.emit(
                video_path or "", self.open_video_separately
            )
        except Exception as error:
            self.error.emit(str(error))


app = QApplication()

loader = QUiLoader()
# define the file type
file_type = "3D_vector"

# --- Dynamic Row Tracker ---
# This list will store tuples: (label_widget, [box_x, box_y, box_z])
vector_rows = []


def play_video(video_path):
    window.media_player.setSource(QUrl.fromLocalFile(video_path))
    window.media_player.play()


def close_progress_dialog():
    dialog = getattr(window, "progress_dialog", None)
    if dialog is not None:
        dialog.close()
        dialog.deleteLater()
        window.progress_dialog = None


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
        v1_x = float(interpretInput(window.vector1_x.text() or 0))
        v1_y = float(interpretInput(window.vector1_y.text() or 0))
        v1_z = float(interpretInput(window.vector1_z.text() or 0))
        all_vectors.append([v1_x, v1_y, v1_z])
    except:
        QMessageBox.information(window, 'Input Error', 'An unknown function or invalid values have been inputted. Please check or change your inputs and try again.')

    for label, boxes, layout in vector_rows:
        try:
            x = float(interpretInput(boxes[0].text() or 0))
            y = float(interpretInput(boxes[1].text() or 0))
            z = float(interpretInput(boxes[2].text() or 0))
            all_vectors.append([x, y, z])
        except ValueError:
            all_vectors.append([0.0, 0.0, 0.0])
        except:
            QMessageBox.information(window, 'Input Error', 'An unknown function or invalid values have been inputted. Please check or change your inputs and try again.')
            
    return all_vectors


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
              
    user_vectors = get_all_vectors()
    print(f"Vectors to transform: {user_vectors}")
    vector_values = "".join(str(num) for vector in user_vectors for num in vector)
    values = f"{str(a)}{str(b)}{str(c)}{str(d)}{str(e)}{str(f)}{str(g)}{str(h)}{str(i)}{vector_values}"
    
    if window.inverseMatrix_checkBox.isChecked():
        show_inverse = 1
    else:
        show_inverse = 0

    if window.coordinates_checkBox.isChecked():
        file_type = "3D_vector_with_coords"
    else:
        file_type = "3D_vector"

    video_quality = get_video_quality()
    video_history = find_matrix_video(file_type, video_quality, values)
    if video_history != None:
        if window.seperateVideo_checkBox.isChecked():
            os.startfile(video_history)
        else:
            play_video(video_history)
        return

    open_video_separately = window.seperateVideo_checkBox.isChecked()

    window.progress_dialog = QProgressDialog(
        "Generating Matrix Transformation Video...", None, 0, 0, window
    )
    window.progress_dialog.setWindowTitle("Processing Request")
    window.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
    window.progress_dialog.show()

    window.render_thread = VideoRenderer(
        show_inverse,
        matrix,
        user_vectors,
        file_type,
        video_quality,
        values,
        open_video_separately,
    )
    window.render_thread.render_finished.connect(on_render_finished)
    window.render_thread.error.connect(on_render_error)
    window.render_thread.start()


def on_render_finished(video_path, open_video_separately):
    close_progress_dialog()

    if video_path and os.path.exists(video_path):
        if open_video_separately:
            os.startfile(video_path)
        else:
            play_video(video_path)
    else:
        QMessageBox.warning(
            window,
            "File Error",
            "The video was generated successfully but file explorer could not find the video.",
        )


def on_render_error(error_message):
    close_progress_dialog()
    QMessageBox.critical(
        window,
        "Rendering Error",
        f"An error occurred whilst generating the video:\n{error_message}",
    )


file = QFile('3D_vector.ui')
file.open(QFile.ReadOnly)
window = loader.load(file)
file.close()
window.setWindowTitle('Matrix Visualiser')

audio_output = QAudioOutput(window)
window.media_player = QMediaPlayer(window)
window.media_player.setAudioOutput(audio_output)
window.video_widget = QVideoWidget(window.video_container)
window.video_widget.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
window.video_widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
window.media_player.setVideoOutput(window.video_widget)
window.media_player.setLoops(1)

window.video_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
video_layout = QVBoxLayout(window.video_container)
video_layout.setContentsMargins(0, 0, 0, 0)
video_layout.setSpacing(0)
video_layout.addWidget(window.video_widget)
window.settings_frame.setMaximumWidth(400)

# --- Button Connections ---
window.visualiseButton.clicked.connect(visualise)
window.addVectorButton.clicked.connect(add_vector)       # Action for adding rows
window.removeVectorButton.clicked.connect(remove_vector) # Action for clearing rows
window.show()

app.exec()
