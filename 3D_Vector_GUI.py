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
from matrix_video_finder import find_matrix_video
from maths_syntaxer import interpretInput
import os
import sys
from resources import resource_path

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
            run_manim_worker(
                {
                    "kind": "3d_vector",
                    "matrix": self.matrix,
                    "show_inverse": bool(self.show_inverse),
                    "show_coordinates": self.file_type == "3D_vector_with_coords",
                    "vectors": self.user_vectors,
                    "quality": self.video_quality,
                    "output_file": f"matrix_animation_{self.values}_{self.file_type}",
                }
            )

            video_path = find_matrix_video(
                self.file_type, self.video_quality, self.values
            )
            self.render_finished.emit(
                video_path or "", self.open_video_separately
            )
        except Exception as error:
            self.error.emit(str(error))


# define the file type
file_type = "3D_vector"

vector_rows = []


def play_video(video_path):
    sub_window.media_player.setSource(QUrl.fromLocalFile(video_path))
    sub_window.media_player.play()


def close_progress_dialog():
    dialog = getattr(sub_window, "progress_dialog", None)
    if dialog is not None:
        dialog.close()
        dialog.deleteLater()
        sub_window.progress_dialog = None


def get_video_quality():
    selected_quality = sub_window.quality_buttonGroup.checkedButton()

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
        
    target_layout = sub_window.scrollArea_verticalLayout
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
        v1_x = float(interpretInput(sub_window.vector1_x.text() or 0))
        v1_y = float(interpretInput(sub_window.vector1_y.text() or 0))
        v1_z = float(interpretInput(sub_window.vector1_z.text() or 0))
        all_vectors.append([v1_x, v1_y, v1_z])
    except:
        QMessageBox.information(sub_window, 'Input Error', 'An unknown function or invalid values have been inputted. Please check or change your inputs and try again.')

    for label, boxes, layout in vector_rows:
        try:
            x = float(interpretInput(boxes[0].text() or 0))
            y = float(interpretInput(boxes[1].text() or 0))
            z = float(interpretInput(boxes[2].text() or 0))
            all_vectors.append([x, y, z])
        except ValueError:
            all_vectors.append([0.0, 0.0, 0.0])
        except:
            QMessageBox.information(sub_window, 'Input Error', 'An unknown function or invalid values have been inputted. Please check or change your inputs and try again.')
            
    return all_vectors


def visualise():
    try:
        a = float(interpretInput(sub_window.a_value.text()))
        b = float(interpretInput(sub_window.b_value.text()))
        c = float(interpretInput(sub_window.c_value.text()))
        d = float(interpretInput(sub_window.d_value.text()))
        e = float(interpretInput(sub_window.e_value.text()))
        f = float(interpretInput(sub_window.f_value.text()))
        g = float(interpretInput(sub_window.g_value.text()))
        h = float(interpretInput(sub_window.h_value.text()))
        i = float(interpretInput(sub_window.i_value.text()))
    except:
        QMessageBox.information(sub_window, 'Input Error', 'An unknown function or invalid values have been inputted. Please check or change your inputs and try again.')
        return

    matrix = [[a, b, c],
              [d, e, f],
              [g, h, i]]
              
    user_vectors = get_all_vectors()
    print(f"Vectors to transform: {user_vectors}")
    vector_values = "".join(str(num) for vector in user_vectors for num in vector)
    values = f"{str(a)}{str(b)}{str(c)}{str(d)}{str(e)}{str(f)}{str(g)}{str(h)}{str(i)}{vector_values}"
    
    if sub_window.inverseMatrix_checkBox.isChecked():
        show_inverse = 1
    else:
        show_inverse = 0

    if sub_window.coordinates_checkBox.isChecked():
        file_type = "3D_vector_with_coords"
    else:
        file_type = "3D_vector"

    video_quality = get_video_quality()
    video_history = find_matrix_video(file_type, video_quality, values)
    if video_history != None:
        if sub_window.seperateVideo_checkBox.isChecked():
            os.startfile(video_history)
        else:
            play_video(video_history)
        return

    open_video_separately = sub_window.seperateVideo_checkBox.isChecked()

    sub_window.progress_dialog = QProgressDialog(
        "Generating Matrix Transformation Video...", None, 0, 0, sub_window
    )
    sub_window.progress_dialog.setWindowTitle("Processing Request")
    sub_window.progress_dialog.setWindowModality(Qt.WindowModality.NonModal)
    sub_window.progress_dialog.show()

    sub_window.render_thread = VideoRenderer(
        show_inverse,
        matrix,
        user_vectors,
        file_type,
        video_quality,
        values,
        open_video_separately,
    )
    sub_window.render_thread.render_finished.connect(on_render_finished)
    sub_window.render_thread.error.connect(on_render_error)
    sub_window.render_thread.start()


def on_render_finished(video_path, open_video_separately):
    close_progress_dialog()

    if video_path and os.path.exists(video_path):
        if open_video_separately:
            os.startfile(video_path)
        else:
            play_video(video_path)
    else:
        QMessageBox.warning(
            sub_window,
            "File Error",
            "The video was generated successfully but file explorer could not find the video.",
        )


def on_render_error(error_message):
    close_progress_dialog()
    QMessageBox.critical(
        sub_window,
        "Rendering Error",
        f"An error occurred whilst generating the video:\n{error_message}",
    )



loader = QUiLoader()
file = QFile(str(resource_path('3D_vector.ui')))
file.open(QFile.ReadOnly)
sub_window = loader.load(file)
file.close()
sub_window.setWindowTitle('Matrix Visualiser')

audio_output = QAudioOutput(sub_window)
sub_window.media_player = QMediaPlayer(sub_window)
sub_window.media_player.setAudioOutput(audio_output)
sub_window.video_widget = QVideoWidget(sub_window.video_container)
sub_window.video_widget.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
sub_window.video_widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
sub_window.media_player.setVideoOutput(sub_window.video_widget)
sub_window.media_player.setLoops(1)

sub_window.video_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
video_layout = QVBoxLayout(sub_window.video_container)
video_layout.setContentsMargins(0, 0, 0, 0)
video_layout.setSpacing(0)
video_layout.addWidget(sub_window.video_widget)
sub_window.settings_frame.setMaximumWidth(400)

# --- Button Connections ---
sub_window.visualiseButton.clicked.connect(visualise)
sub_window.addVectorButton.clicked.connect(add_vector)       # Action for adding rows
sub_window.removeVectorButton.clicked.connect(remove_vector) # Action for clearing rows

app = QApplication.instance()

if not app:
    app = QApplication(sys.argv)
    sub_window.setsub_windowTitle("Matrix Visualiser")
    sub_window.show()

    sys.exit(app.exec())
