from PySide6.QtWidgets import QApplication, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QVBoxLayout, QSizePolicy, QProgressDialog
from PySide6.QtCore import QFile, Qt, QUrl, QThread, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from TwoD_vector_animator import TwoDVectorTransformation, TwoDVectorTransformationWithCoordinates
from manim import config
from matrix_video_finder import find_matrix_video
import os
import sys
from maths_syntaxer import interpretInput

#Classes go below here

#I seperate the rendering process into a seperate 'Thread' to allow the sub_window to remain responsive whilst all the rendering stuff happens
class VideoRenderer(QThread):
    #Allows the renderer to report errors because you need that obviously
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
    open_video_seperately
    ):
        super().__init__()
        self.show_inverse = show_inverse
        self.matrix = matrix
        self.user_vectors = user_vectors
        self.file_type = file_type
        self.video_quality = video_quality
        self.values = values
        self.open_video_seperately = open_video_seperately

    def run(self):
        try:
            config.preview = False
            config.quality = self.video_quality
            config.output_file = f"matrix_animation_{self.values}_{self.file_type}"

            if self.file_type == "2D_vector_with_coords":
                scene = TwoDVectorTransformationWithCoordinates(self.show_inverse, self.matrix, self.user_vectors)
            else:
                scene = TwoDVectorTransformation(self.show_inverse, self.matrix, self.user_vectors)

            #scene.render() is what blocks all our stuff really
            scene.render()

            video_path = find_matrix_video(self.file_type, self.video_quality, self.values)
            self.render_finished.emit(video_path or "", self.open_video_seperately)

        except Exception as e:
            self.error.emit(str(e))



#FUNCTION STUFF
def play_video(video_path):
    # Converts "C:/path/to/video.mp4" into a local QUrl format
    local_url = QUrl.fromLocalFile(video_path)
    sub_window.media_player.setSource(local_url)
    sub_window.media_player.play()

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


def close_progress_dialog():
    dialog = getattr(sub_window, "progress_dialog", None)
    if dialog is not None:
        dialog.close()
        dialog.deleteLater()
        sub_window.progress_dialog = None

vector_rows = []
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
        v1_x = float(interpretInput(sub_window.vector1_x.text())) or 0
        v1_y = float(interpretInput(sub_window.vector1_y.text())) or 0
        #v1_z = float(sub_window.vector1_z.text() or 0)
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
        a = float(interpretInput(sub_window.a_value.text()))
        b = float(interpretInput(sub_window.b_value.text()))
        c = float(interpretInput(sub_window.c_value.text()))
        d = float(interpretInput(sub_window.d_value.text()))
        

    except:
        QMessageBox.information(sub_window, 'Input Error', 'An unknown function or invalid values have been inputted. Please check or change your inputs and try again.')
        return
    
    user_vectors = get_all_vectors()
    matrix = [[a, b],
              [c, d]]
              
    print(f"Vectors to transform: {user_vectors}")
    vector_values = "".join(str(num) for vector in user_vectors for num in vector)
    values = f"{str(a)}{str(b)}{str(c)}{str(d)}{vector_values}"
    
    #print(f"Values: {values}")
    

    #print("Processing...")
    if sub_window.inverseMatrix_checkBox.isChecked():
        show_inverse = 1
    else:
        show_inverse = 0
    if sub_window.coordinates_checkBox.isChecked():
        #print("Showing coords")
        file_type = "2D_vector_with_coords"
    else:
        file_type = "2D_vector"

    if sub_window.seperateVideo_checkBox.isChecked():
        open_video_seperately = True
    else:
        open_video_seperately = False

    video_quality = get_video_quality()
    video_history = find_matrix_video(file_type, video_quality, values)
    if video_history != None:
        if open_video_seperately == False:
            play_video(video_history)
        else:
            os.startfile(video_history)
        return

    sub_window.progress_dialog = QProgressDialog("Generating Matrix Transformation Video...", None, 0, 0, sub_window)
    sub_window.progress_dialog.setsub_windowTitle("Processing Request")
    sub_window.progress_dialog.setsub_windowModality(Qt.sub_windowModality.sub_windowModal)
    #progress_dialog.setCancelButton(None)
    sub_window.progress_dialog.show()

    global render_thread

    sub_window.render_thread = VideoRenderer(show_inverse, matrix, user_vectors, file_type, video_quality, values, open_video_seperately)

    sub_window.render_thread.render_finished.connect(on_render_finished)
    sub_window.render_thread.error.connect(on_render_error)

    sub_window.render_thread.start()

    
def on_render_finished(video_path, open_video_seperately):
    close_progress_dialog()
        
    if video_path and os.path.exists(video_path):
        print(f"Video generated successfully: {video_path}")
        if open_video_seperately == False:
            play_video(video_path)
        else:
            os.startfile(video_path)
    else:
        QMessageBox.warning(sub_window, "File Error", "The video was generated successfully but file explorer could not find the video. ")

def on_render_error(error_msg):
    close_progress_dialog()
    QMessageBox.critical(sub_window, "Rendering Error", f"An error occurred whilst generating the video:\n{error_msg}")



loader = QUiLoader()
file = QFile('2D_vector.ui')
file.open(QFile.ReadOnly)
sub_window = loader.load(file)
file.close()
sub_window.setWindowTitle('Matrix Visualiser')

audio_output = QAudioOutput()
sub_window.media_player = QMediaPlayer()
sub_window.media_player.setAudioOutput(audio_output)
sub_window.video_widget = QVideoWidget()

#I make sure that the video widget runs the video using a GPU rather than laggy software rendering

sub_window.video_widget.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
sub_window.video_widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

sub_window.media_player.setVideoOutput(sub_window.video_widget)
sub_window.media_player.setLoops(1)

sub_window.video_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
sub_window.video_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

video_layout = QVBoxLayout(sub_window.video_container)

video_layout.setContentsMargins(0,0,0,0)
video_layout.setSpacing(0)

video_layout.addWidget(sub_window.video_widget)
#sub_window.video_container.layout().addWidget(sub_window.video_widget)
#sub_window.video_container.setMinimumWidth(0) 


sub_window.settings_frame.setSizePolicy(
    sub_window.settings_frame.sizePolicy().horizontalPolicy(),
    sub_window.settings_frame.sizePolicy().verticalPolicy()
)
sub_window.settings_frame.setMaximumWidth(400)
#sub_window.settings_frame.parentWidget().layout().setColumnMaximumWidth(0, 400)

#sub_window.gridLayout_Main.setColumnStretch(0,1)
#sub_window.gridLayout_Main.setColumnStretch(1,4)

# --- Button Connections ---
sub_window.visualiseButton.clicked.connect(visualise)
sub_window.addVectorButton.clicked.connect(add_vector)       # Action for adding rows
sub_window.removeVectorButton.clicked.connect(remove_vector) # Action for clearing rows

app = QApplication.instance()

if not app:
    app = QApplication(sys.argv)
    sub_window.setWindowTitle("Matrix Visualiser")
    sub_window.show()

    sys.exit(app.exec())
