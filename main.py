from PyQt6.Qt6 import *
from PyQt6.QtWidgets import *
import sys

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Josephine")
window.resize(400, 400)
window.show()

sys.exit(app.exec())