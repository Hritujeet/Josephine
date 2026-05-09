from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
import sys

app = QApplication(sys.argv)

# Ensures the app keeps running even if no windows are open
app.setQuitOnLastWindowClosed(False)

# Create the menu
menu = QMenu()

wake_action = QAction("Wake Up")
menu.addAction(wake_action)

sleep_action = QAction("Sleep")
menu.addAction(sleep_action)

menu.addSeparator()

quit_action = QAction("Quit")
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)

# Initialize Tray Icon
tray_icon = QSystemTrayIcon(QIcon("assets/josephine.png"), parent=app)
tray_icon.setContextMenu(menu)
tray_icon.show()

sys.exit(app.exec())