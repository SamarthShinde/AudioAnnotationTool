# gui.py

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLabel, QFileDialog, QCheckBox, QMessageBox, QProgressBar, QShortcut
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from segmenter import segment_audio
from annotations import AnnotationHandler
from audio_player import AudioPlayer

class AudioAnnotator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Annotation Tool")
        self.setGeometry(100, 100, 1200, 600)

        # Initialize variables
        self.audio_folder = ''
        self.audio_files = []
        self.current_audio_index = -1
        self.current_segment_index = -1
        self.segments = []
        self.player = AudioPlayer()
        self.player.playback_finished.connect(self.on_playback_finished)
        self.is_playing = False

        # Annotation classes
        self.classes = ['Male', 'Female', 'Engine_rev', 'No_sound', 'Music']
        self.class_checkboxes = []

        # Annotation handler
        self.annotation_handler = AnnotationHandler('annotations.csv')

        # Build GUI components
        self.create_widgets()

        # Setup keyboard shortcuts
        self.setup_shortcuts()

    def create_widgets(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Left layout
        left_layout = QVBoxLayout()

        # Audio file list
        self.audio_list = QListWidget()
        self.audio_list.itemClicked.connect(self.on_audio_select)
        left_layout.addWidget(self.audio_list)

        # Segment list
        self.segment_list = QListWidget()
        self.segment_list.itemClicked.connect(self.on_segment_select)
        left_layout.addWidget(self.segment_list)

        main_layout.addLayout(left_layout)

        # Center layout for controls and annotations
        center_layout = QVBoxLayout()

        # Load folder button
        load_button = QPushButton("Load Audio Folder")
        load_button.clicked.connect(self.load_audio_folder)
        center_layout.addWidget(load_button)

        # Audio info label
        self.audio_info_label = QLabel("No audio loaded")
        center_layout.addWidget(self.audio_info_label)

        # Control buttons
        control_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_segment)
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_audio)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_audio)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_segment)
        control_layout.addWidget(self.prev_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.next_button)
        center_layout.addLayout(control_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        center_layout.addWidget(self.progress_bar)

        # Class checkboxes
        for cls in self.classes:
            checkbox = QCheckBox(cls)
            checkbox.stateChanged.connect(self.update_selected_class)
            self.class_checkboxes.append(checkbox)
            center_layout.addWidget(checkbox)

        # Selected class label
        self.selected_class_label = QLabel("Selected Class: None")
        center_layout.addWidget(self.selected_class_label)

        main_layout.addLayout(center_layout)

        # Right column for annotations list
        self.annotation_list = QListWidget()
        main_layout.addWidget(self.annotation_list)

    def setup_shortcuts(self):
        # Shortcuts for class selection
        self.shortcut1 = QShortcut(QKeySequence('1'), self)
        self.shortcut1.activated.connect(lambda: self.toggle_class_checkbox(0))

        self.shortcut2 = QShortcut(QKeySequence('2'), self)
        self.shortcut2.activated.connect(lambda: self.toggle_class_checkbox(1))

        self.shortcut3 = QShortcut(QKeySequence('3'), self)
        self.shortcut3.activated.connect(lambda: self.toggle_class_checkbox(2))

        self.shortcut4 = QShortcut(QKeySequence('4'), self)
        self.shortcut4.activated.connect(lambda: self.toggle_class_checkbox(3))

        self.shortcut5 = QShortcut(QKeySequence('5'), self)
        self.shortcut5.activated.connect(lambda: self.toggle_class_checkbox(4))

        # Shortcuts for navigation and playback
        self.shortcut_next = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.shortcut_next.activated.connect(self.next_segment)

        self.shortcut_prev = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.shortcut_prev.activated.connect(self.prev_segment)

        self.shortcut_play_pause = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.shortcut_play_pause.activated.connect(self.toggle_playback)

    def toggle_class_checkbox(self, index):
        if 0 <= index < len(self.class_checkboxes):
            checkbox = self.class_checkboxes[index]
            checkbox.setChecked(not checkbox.isChecked())

    def toggle_playback(self):
        if self.is_playing:
            self.stop_audio()
        else:
            self.play_audio()

    def load_audio_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Audio Folder")
        if folder:
            self.audio_folder = folder
            self.audio_files = [f for f in os.listdir(self.audio_folder) if f.lower().endswith('.wav')]
            self.update_audio_list()
            self.current_audio_index = -1
            self.current_segment_index = -1
            if self.audio_files:
                self.audio_list.setCurrentRow(0)
                self.load_audio(0)
            else:
                QMessageBox.warning(self, "No WAV Files", "The selected folder contains no WAV audio files.")

    def update_audio_list(self):
        self.audio_list.clear()
        for audio_file in self.audio_files:
            annotated = self.annotation_handler.is_audio_annotated(audio_file)
            display_name = f"✓ {audio_file}" if annotated else audio_file
            self.audio_list.addItem(display_name)
        self.update_annotation_list()

    def update_annotation_list(self):
        self.annotation_list.clear()
        annotations = self.annotation_handler.get_all_annotations()
        for annotation in annotations:
            audio_name = annotation['Audio Name']
            segment_number = annotation['Segment Number']
            class_name = annotation['Class Name']
            self.annotation_list.addItem(f"{audio_name} - Segment {segment_number}: {class_name}")

    def on_audio_select(self, item):
        index = self.audio_list.row(item)
        self.load_audio(index)

    def load_audio(self, index):
        if index < 0 or index >= len(self.audio_files):
            return
        self.current_audio_index = index
        audio_file = self.audio_files[index]
        audio_path = os.path.join(self.audio_folder, audio_file)
        self.audio_path = audio_path  # Store the full path
        self.segments = segment_audio(audio_path)
        if self.segments:
            self.current_segment_index = 0
            self.update_segment_list()
            self.update_audio_info()
            self.reset_class_selection()
            self.load_existing_annotation()
            self.update_progress_bar()
        else:
            QMessageBox.warning(self, "Error", f"Could not segment audio file: {audio_file}")

    def update_segment_list(self):
        self.segment_list.clear()
        audio_name = self.audio_files[self.current_audio_index]
        for i, (start_ms, end_ms) in enumerate(self.segments):
            annotated = self.annotation_handler.get_annotation(audio_name, i) is not None
            display_name = f"✓ Segment {i + 1}" if annotated else f"Segment {i + 1}"
            self.segment_list.addItem(display_name)

    def on_segment_select(self, item):
        index = self.segment_list.row(item)
        self.current_segment_index = index
        self.update_audio_info()
        self.reset_class_selection()
        self.load_existing_annotation()
        self.update_progress_bar()

    def update_audio_info(self):
        if self.current_audio_index < 0 or self.current_segment_index < 0:
            self.audio_info_label.setText("No audio loaded")
            return
        audio_name = self.audio_files[self.current_audio_index]
        segment_number = self.current_segment_index + 1
        total_segments = len(self.segments)
        start_ms, end_ms = self.segments[self.current_segment_index]
        duration_s = (end_ms - start_ms) / 1000.0
        self.segment_time = f"{int(start_ms / 1000)}-{int(end_ms / 1000)}"  # Store segment time
        self.audio_info_label.setText(
            f"Audio: {audio_name} | Segment: {segment_number}/{total_segments} | Duration: {duration_s:.2f}s"
        )

    def play_audio(self):
        if self.is_playing or self.current_audio_index < 0 or self.current_segment_index < 0:
            return
        audio_file = self.audio_path  # Use the stored full path
        start_ms, end_ms = self.segments[self.current_segment_index]
        self.player.play_audio_segment(audio_file, start_ms, end_ms)
        self.is_playing = True

    def stop_audio(self):
        if self.is_playing:
            self.player.stop()
            self.is_playing = False

    def on_playback_finished(self):
        self.is_playing = False

    def next_segment(self):
        if self.current_segment_index < len(self.segments) - 1:
            self.current_segment_index += 1
            self.segment_list.setCurrentRow(self.current_segment_index)
            self.update_audio_info()
            self.reset_class_selection()
            self.load_existing_annotation()
            self.update_progress_bar()

    def prev_segment(self):
        if self.current_segment_index > 0:
            self.current_segment_index -= 1
            self.segment_list.setCurrentRow(self.current_segment_index)
            self.update_audio_info()
            self.reset_class_selection()
            self.load_existing_annotation()
            self.update_progress_bar()

    def update_progress_bar(self):
        if self.current_segment_index >= 0 and len(self.segments) > 0:
            progress = int((self.current_segment_index + 1) / len(self.segments) * 100)
            self.progress_bar.setValue(progress)
        else:
            self.progress_bar.setValue(0)

    def update_selected_class(self):
        selected_classes = [cb.text() for cb in self.class_checkboxes if cb.isChecked()]
        self.selected_class_label.setText(f"Selected Class: {', '.join(selected_classes)}")
        self.save_current_annotation()

    def reset_class_selection(self):
        for cb in self.class_checkboxes:
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.blockSignals(False)
        self.selected_class_label.setText("Selected Class: None")

    def save_current_annotation(self):
        if self.current_audio_index < 0 or self.current_segment_index < 0:
            return
        selected_classes = [cb.text() for cb in self.class_checkboxes if cb.isChecked()]
        class_ids = [self.classes.index(cls) for cls in selected_classes]
        audio_name = self.audio_files[self.current_audio_index]
        file_location = self.audio_path  # Use the stored full path
        segment_number = self.current_segment_index
        segment_time = self.segment_time  # Use the stored segment time
        self.annotation_handler.save_annotation(
            audio_name, file_location, segment_number, segment_time, class_ids, selected_classes
        )
        self.update_audio_list()
        self.update_annotation_list()
        self.update_segment_list()

    def load_existing_annotation(self):
        if self.current_audio_index < 0 or self.current_segment_index < 0:
            return
        audio_name = self.audio_files[self.current_audio_index]
        segment_number = self.current_segment_index
        annotation = self.annotation_handler.get_annotation(audio_name, segment_number)
        if annotation is not None:
            class_names = annotation['Class Name'].split(',')
            for cb in self.class_checkboxes:
                cb.blockSignals(True)
                cb.setChecked(cb.text() in class_names)
                cb.blockSignals(False)
            self.selected_class_label.setText(f"Selected Class: {', '.join(class_names)}")
        else:
            self.reset_class_selection()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 'Do you really wish to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()