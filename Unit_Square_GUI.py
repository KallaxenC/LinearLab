from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QVBoxLayout,
    QSizePolicy,
    QProgressDialog,
)
from PySide6.QtCore import QFile, Qt, QUrl, QThread, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from matrix_video_finder import find_matrix_video
import os
import sys
from maths_syntaxer import interpretInput
from resources import resource_path

class VideoRenderer(QThread):
    render_finished = Signal(str, bool)
    error = Signal(str)

    def __init__(
        self,
        show_inverse,
        matrix,
        file_type,
        video_quality,
        values,
        open_video_separately,
    ):
        super().__init__()
        self.show_inverse = show_inverse
        self.matrix = matrix
        self.file_type = file_type
        self.video_quality = video_quality
        self.values = values
        self.open_video_separately = open_video_separately

    def run(self):
        try:
            run_manim_worker(
                {
                    "kind": "unit_square",
                    "matrix": self.matrix,
                    "show_inverse": bool(self.show_inverse),
                    "show_coordinates": False,
                    "vectors": [],
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


#define the video file type
file_type = "unit_square"


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

def visualise():
    try:
        a = float(interpretInput(sub_window.a_value.text()))
        b = float(interpretInput(sub_window.b_value.text()))
        c = float(interpretInput(sub_window.c_value.text()))
        d = float(interpretInput(sub_window.d_value.text()))
    except:
        QMessageBox.information(sub_window, 'Input Error', 'An unknown function or invalid values have been inputted. Please check or change your inputs and try again.')
        return

    matrix = [[a, b],
              [c, d]]

    values = f"{str(a)}{str(b)}{str(c)}{str(d)}"
    video_quality = get_video_quality()
    video_history = find_matrix_video(file_type, video_quality, values)
    if video_history != None:
        if sub_window.seperateVideo_checkBox.isChecked():
            os.startfile(video_history)
        else:
            play_video(video_history)
        return

    show_inverse = int(sub_window.inverseMatrix_checkBox.isChecked())
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
            "The video was generated successfully but file explorer could not find the video...",
        )


def on_render_error(error_message):
    close_progress_dialog()
    QMessageBox.critical(
        sub_window,
        "Rendering Error",
        f"An error occurred whilst generating the video:\n{error_message}",
    )

loader = QUiLoader()
file = QFile(str(resource_path('unit_square.ui')))
file.open(QFile.ReadOnly)
sub_window = loader.load(file)
file.close()
sub_window.setWindowTitle("Matrix Visualiser")


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

sub_window.visualiseButton.clicked.connect(visualise)

app = QApplication.instance()

if not app:
    app = QApplication(sys.argv)
    sub_window.setWindowTitle("Matrix Visualiser")
    sub_window.show()

    sys.exit(app.exec())
