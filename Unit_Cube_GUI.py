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
from unit_cube_animator import CubeVertexTransformation
from manim import config
from matrix_video_finder import find_matrix_video
from maths_syntaxer import interpretInput
import os


class VideoRenderer(QThread):
    render_finished = Signal(str, bool)
    error = Signal(str)

    def __init__(
        self,
        matrix,
        show_inverse,
        show_coordinates,
        file_type,
        video_quality,
        values,
        open_video_separately,
    ):
        super().__init__()
        self.matrix = matrix
        self.show_inverse = show_inverse
        self.show_coordinates = show_coordinates
        self.file_type = file_type
        self.video_quality = video_quality
        self.values = values
        self.open_video_separately = open_video_separately

    def run(self):
        try:
            config.preview = False
            config.quality = self.video_quality
            config.output_file = f"matrix_animation_{self.values}_{self.file_type}"

            scene = CubeVertexTransformation(
                self.matrix,
                show_inverse=self.show_inverse,
                show_coordinates=self.show_coordinates,
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
#define the file type
file_type = "unit_cube"


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
        matrix,
        show_inverse,
        show_coordinates,
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


file = QFile('unit_cube.ui')
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

window.visualiseButton.clicked.connect(visualise)

window.show()

app.exec()
