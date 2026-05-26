from states.state_manager import StateManager
from PyQt6.QtGui import QIcon

# Initialize the state manager thread and the tray icon reference. The state manager will handle the logic for the various states of JOSEPHINE, while the tray icon reference allows us to show notifications from within this file without needing to pass the tray icon around as a parameter.
state_thread = StateManager()
_tray_icon = None # Placeholder for the tray icon reference

def init_states(tray_icon_reference):
    """This function initializes the state management system by setting the global tray icon reference and connecting the state manager's status update signal to the show_notification function. This allows the state manager to send status updates that will be displayed as notifications in the system tray, providing feedback to the user about the current state of JOSEPHINE. It acts as a middleman to set up the necessary connections and references for the state management system to function properly."""
    global _tray_icon
    _tray_icon = tray_icon_reference
    
    # Whenever state_thread emits a status_update signal, automatically run the show_notification function and pass it the string payload
    state_thread.status_update.connect(show_notification)

def show_notification(message):
    """This function for now only needs the message from the signal. It uses the global tray icon reference to show a notification with the given message. This allows us to display status updates from the state manager as notifications in the system tray, providing feedback to the user about the current state of JOSEPHINE. The notification includes a title ("JOSEPHINE"), the message content, an icon, and a duration for how long the notification should be displayed."""
    if _tray_icon:
        _tray_icon.showMessage("JOSEPHINE", message, QIcon("assets/josephine.png"), 2000)

def handle_wake():
    """This function is tied to the Wake Up action of JOSEPHINE. It safely starts the thread that manages the wake state, allowing JOSEPHINE to perform its tasks and listen for commands without blocking the main UI thread. If the thread is already running, it does nothing, ensuring that we don't accidentally start multiple threads or cause any issues with the state management."""
    if not state_thread.isRunning():
        state_thread.start()

def handle_sleep():
    """This function is tied to the Sleep action of JOSEPHINE. It safely stops the thread that manages the wake state, allowing JOSEPHINE to enter the sleep state without blocking the main UI thread. If the thread is not running, it does nothing, ensuring that we don't accidentally stop a thread that isn't running."""
    if state_thread.isRunning():
        state_thread.stop()
        show_notification("Going to sleep.")