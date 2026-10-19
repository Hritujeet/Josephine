import time
from PyQt6.QtCore import QThread, pyqtSignal

class StateManager(QThread): # Inherits from QThread to run in a separate thread, ensuring it acts as a background process without blocking the main UI thread

    # Create a custom signal to pass messages back to the main UI thread, esnuring thread-safe communication between the background process and the UI. Here, it emits a string message that can be displayed as a notification or used to update the UI in some way.
    status_update = pyqtSignal(str)
    state_changed = pyqtSignal(bool)

    def run(self):
        """This method runs in a separate thread when the wake state is active. It handle the main logic for the wake state, such as listening for commands or performing tasks. It also emits status updates to the main UI thread to keep the user informed."""

        self.state_changed.emit(True)
        self.status_update.emit("I am online and ready.")
        
        # The main loop for the wake state e.g., listening for commands, performing tasks, etc. The loop continues until the thread is requested to stop, allowing for continuous operation without blocking the main UI thread. It will continue running until the stop method is called, which requests an interruption and waits for the thread to finish before fully stopping. This ensures a clean shutdown of the background process when transitioning to sleep.
        try:
            while not self.isInterruptionRequested():
                time.sleep(1)
        finally:
            self.state_changed.emit(False)
            
    def stop(self):
        """Safely stop the thread when transitioning to sleep. This method requests an interruption to the thread on which the run method is excuting to keep JOSEPHINE online. It then ensures that the thread has stopped fully, without any crashes or memory leaks, thus allowing for a smooth transistion between the Wake and Sleep states."""
        self.requestInterruption()
        self.wait()