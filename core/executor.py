import subprocess

class Executor:
    def __init__(self):
        print("JOSEPHINE is online and ready.")

    def open_app(self):
        print("Opening an ms edge")
        subprocess.Popen(["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"])

    def manage_files_and_folders(self):
        pass

    def view_system_vitals(self):
        pass

    def configure_volume(self):
        pass

    def toggle_bluetooth(self):
        pass

