import sys
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
# Import state handlers and the initialization function from our state management module
from states.states import handle_wake, handle_sleep, init_states, state_thread
from core.executor import Executor

# Initialize the core application object. sys.argv allows PyQt to process any command-line arguments 
# passed when the script is executed. Every PyQt application must have exactly one QApplication instance 
# to manage the control flow and core settings of the graphical user interface.
app = QApplication(sys.argv)

# By default, a PyQt application shuts down when its last visible window is closed. 
# Since JOSEPHINE is designed to be a background assistant living in the system tray 
# without a persistent main window, we must disable this behavior. This ensures the app 
# continues running quietly in the background.
app.setQuitOnLastWindowClosed(False)

# Initialize the context menu for the system tray icon. This acts as the primary user interface 
# for JOSEPHINE when she is running in the background, allowing the user to right-click the icon 
# and interact with her states directly.
menu = QMenu()

executor = Executor()  # Create an instance of the Executor class to handle core functionalities

open_app_action = QAction("Open App")
open_app_action.triggered.connect(executor.open_app)  # Connect the action to the open_app method of the Executor instance
open_app_action.setVisible(False)
menu.addAction(open_app_action)  # Add the "Open App" action to the context

open_app_separator = menu.addSeparator()
open_app_separator.setVisible(False)
state_thread.state_changed.connect(open_app_action.setVisible)
state_thread.state_changed.connect(open_app_separator.setVisible)

# Create the "Wake Up" action. QAction represents a command that can be added to menus or toolbars.
# We then connect its 'triggered' signal to our handle_wake function, meaning that clicking this 
# menu item will safely spin up the background worker thread without blocking the UI.
wake_action = QAction("Wake Up")
wake_action.triggered.connect(handle_wake)
menu.addAction(wake_action)

# Create the "Sleep" action. Similar to the wake action, this connects to the handle_sleep function,
# which safely requests the background thread to halt its current tasks and go dormant.
sleep_action = QAction("Sleep")
sleep_action.triggered.connect(handle_sleep)
menu.addAction(sleep_action)

# Add a visual separator line to the menu. This improves the UI/UX by grouping the state 
# transition commands (Wake/Sleep) away from the critical application commands (Quit).
menu.addSeparator()

# Create the "Quit" action. We connect this directly to the application's built-in quit method.
# This ensures that when the user wants to completely close JOSEPHINE, the PyQt event loop 
# is safely terminated and all background processes are cleaned up.
quit_action = QAction("Quit")
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)

# Initialize the System Tray Icon itself. We assign it the custom JOSEPHINE icon and set its parent 
# to the main app instance. Then, we attach the context menu we just built to this icon.
tray_icon = QSystemTrayIcon(QIcon("assets/josephine.png"), parent=app)
tray_icon.setContextMenu(menu)

# Instruct the OS to render and display the system tray icon in the taskbar.
tray_icon.show()

# Inject the initialized tray icon into our state management module. Because states.py handles 
# logic completely separate from the UI, it needs a reference to this tray_icon so it can send 
# OS-level native notifications (like "Going to sleep") when background thread states change.
init_states(tray_icon)

# Start the main PyQt event loop. app.exec() blocks the script here, constantly waiting for and 
# handling user interactions (like menu clicks). sys.exit() wraps it to ensure that when the app 
# does finally quit, it returns the correct exit code to the operating system.
sys.exit(app.exec())