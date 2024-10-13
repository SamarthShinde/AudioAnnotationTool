# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui import AudioAnnotator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioAnnotator()
    window.show()
    sys.exit(app.exec_())