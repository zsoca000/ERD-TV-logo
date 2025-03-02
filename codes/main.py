import sys
import os
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, 
    QLineEdit, QRadioButton, QButtonGroup, QFileDialog, QLabel, QGroupBox
)
from PyQt6.QtCore import QThread, pyqtSignal
from logo_to_video import AddLogoQWorker


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

        # Text input
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter the starting...")
        layout.addWidget(self.text_input)

        # First Radio Button Group (4 options)
        self.radio_group1 = self.create_radio_group("Select the position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"])
        layout.addWidget(self.radio_group1)

        # Second Radio Button Group (2 options)
        self.radio_group2 = self.create_radio_group("Choose logo", ["ERD TV", "Ismétlés"])
        layout.addWidget(self.radio_group2)

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
            button_group.addButton(radio, i)
            radio_layout.addWidget(radio)

        group_box.setLayout(radio_layout)
        return group_box

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_label.setText(file_path)

    def process_action(self):

        file_path = self.file_label.text()
        start_time = self.text_input.text()
        
        # Get selected radio button text (first group)
        location = next(
            (btn.text() for btn in self.radio_group1.findChildren(QRadioButton) if btn.isChecked()), None
        )
        
        # Get selected radio button text (second group)
        logo_type = next(
            (btn.text() for btn in self.radio_group2.findChildren(QRadioButton) if btn.isChecked()), None
        )

        if not os.path.exists(file_path):
            self.process_label.setText(f"Invalid file path")
        elif start_time == '':
            self.process_label.setText(f"Please define a starting time")
        elif location is None:
            self.process_label.setText(f"Please choose a location")
        elif location is None:
            self.process_label.setText(f"Please choose a the logo type")
        else:
            self.process_button.setEnabled(False)
            self.process_label.setText(f"Started...")
            self.worker = AddLogoQWorker(file_path,loc=location)
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
