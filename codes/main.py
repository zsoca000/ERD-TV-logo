import sys
import os
import time
import numpy as np

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, 
    QLineEdit, QRadioButton, QButtonGroup, QFileDialog, QLabel, QGroupBox, QSpinBox
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QImage

from logo_to_video import AddLogoQWorker, MetaData, get_frame


class SimulateProcess(QThread):
    progress_signal = pyqtSignal(str)  # Signal for (outer loop, inner loop)
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        for i in range(1,101):
            time.sleep(0.05)
            log = f'Frame processed: {i}/100'  
            self.progress_signal.emit(log)
        self.progress_signal.emit('Finished!')


class FileBrowseApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # File selection
        self.file_label = QLabel("No file selected")
        self.browse_button = QPushButton("Browse File")
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.file_label)
        self.worker = None # load with the file is selected

        # Text input
        self.spin_input = QSpinBox()
        self.spin_input.setRange(0, 100)  # Set min and max range
        self.spin_input.setValue(10)  # Set initial value
        self.spin_input.valueChanged.connect(self.update_image)
        layout.addWidget(self.spin_input)

        # First Radio Button Group (4 options)
        self.radio_group1 = self.create_radio_group("Select the position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"])
        layout.addWidget(self.radio_group1)

        # Second Radio Button Group (2 options)
        self.radio_group2 = self.create_radio_group("Choose logo", ["ERD TV", "Ismétlés"])
        layout.addWidget(self.radio_group2)

        # Image Preview Section
        self.thumbnail = None
        self.preview_label = QLabel(self)
        self.preview_label.setText("Image Preview")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setFixedSize(400, 200)  # Set a fixed size for preview
        layout.addWidget(self.preview_label)  # Add to layout
        self.setLayout(layout)
        self.setWindowTitle("Form with Image Preview")

        # Process button
        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process_action)
        layout.addWidget(self.process_button)

        # Process status label
        self.process_label = QLabel("")
        layout.addWidget(self.process_label)

        # Set layout
        self.setLayout(layout)
        self.setWindowTitle("ERD TV Logo")
        self.resize(400, 300)

    def create_radio_group(self, title, options):
        group_box = QGroupBox(title)
        radio_layout = QVBoxLayout()
        button_group = QButtonGroup(self)

        for i, option in enumerate(options):
            radio = QRadioButton(option)
            if i == 0:
                radio.setChecked(True)
            button_group.addButton(radio, i)
            radio_layout.addWidget(radio)
            radio.toggled.connect(self.update_image)
            
        group_box.setLayout(radio_layout)
        return group_box

    def update_image(self):
        
        # Get selected radio button text (first group)
        location = next(
            (btn.text() for btn in self.radio_group1.findChildren(QRadioButton) if btn.isChecked()), None
        )
        
        # Get selected radio button text (second group)
        logo_type = next(
            (btn.text() for btn in self.radio_group2.findChildren(QRadioButton) if btn.isChecked()), None
        )

        start_frame = self.spin_input.value()
        
        if self.worker:
            self.thumbnail = get_frame(
                self.worker.video_path,
                width=self.worker.meta_data.width,
                height=self.worker.meta_data.height,
                frame_number=int(start_frame)
            )
            if location and logo_type and start_frame:
                self.worker.set_loc(location)
                self.display_image(
                    self.worker.logo2frame(self.thumbnail)
                )
            else:
                self.display_image(self.thumbnail)


    def display_image(self, image):
        if isinstance(image, QPixmap):  # If it's already a QPixmap
            self.preview_label.setPixmap(image.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        elif isinstance(image, np.ndarray):  # If it's a NumPy array
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.preview_label.setPixmap(pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            self.preview_label.setText("Invalid Image")
    

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_label.setText(file_path)

            try:
                self.worker = AddLogoQWorker(file_path)
                self.update_image()
            except:
                self.preview_label.setText("Unable to load video")


    def process_action(self):

        file_path = self.file_label.text()
        
        # Get selected radio button text (first group)
        location = next(
            (btn.text() for btn in self.radio_group1.findChildren(QRadioButton) if btn.isChecked()), None
        )
        
        # Get selected radio button text (second group)
        logo_type = next(
            (btn.text() for btn in self.radio_group2.findChildren(QRadioButton) if btn.isChecked()), None
        )

        start_frame = self.spin_input.value()

        if not os.path.exists(file_path):
            self.process_label.setText(f"Invalid file path")
        elif location is None:
            self.process_label.setText(f"Please choose a location")
        elif location is None:
            self.process_label.setText(f"Please choose a the logo type")
        else:
            self.process_button.setEnabled(False)
            self.process_label.setText(f"Started...")
            # self.worker.set_loc(loc=location) # Became redundant by tracking toggle
            self.worker.set_start_frame(start_frame)
            print(self.worker.start_frame)
            self.worker.progress_signal.connect(self.update_progress)
            self.worker.start()

        # self.process_button.setEnabled(False)
        # self.process_label.setText(f"Started...")
        # self.add_logo = SimulateProcess()
        # self.add_logo.progress_signal.connect(self.update_progress)
        # self.add_logo.start()


    def update_progress(self, label_text):
        self.process_label.setText(label_text)
        if label_text == 'Finished!':
            self.process_button.setEnabled(True)  # Re-enable button after completion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileBrowseApp()
    window.show()
    sys.exit(app.exec())
