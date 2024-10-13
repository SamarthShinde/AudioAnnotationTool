# audio_player.py

from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class AudioPlayer(QObject):
    playback_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.player.stateChanged.connect(self.on_state_changed)
        self.end_ms = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_position)

    def play_audio_segment(self, audio_file, start_ms, end_ms):
        media = QMediaContent(QUrl.fromLocalFile(audio_file))
        self.player.setMedia(media)
        self.player.setPosition(start_ms)
        self.end_ms = end_ms
        self.player.play()
        self.timer.start(100)  # Check position every 100 ms

    def check_position(self):
        if self.player.position() >= self.end_ms:
            self.stop()

    def stop(self):
        self.player.stop()
        self.timer.stop()
        self.playback_finished.emit()

    def on_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.timer.stop()
            self.playback_finished.emit()