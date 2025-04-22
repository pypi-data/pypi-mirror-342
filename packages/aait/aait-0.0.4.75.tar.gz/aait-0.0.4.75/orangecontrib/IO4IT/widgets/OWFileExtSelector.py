import os
import subprocess
import tempfile

from PyQt5.QtWidgets import QPushButton, QListWidget, QListWidgetItem, QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5 import uic
from Orange.widgets.widget import OWWidget, Output, Input
from Orange.data import Table, Domain, StringVariable
from Orange.widgets.settings import Setting


class FileDialogWorker(QObject):
    finished = pyqtSignal(list)

    def __init__(self, ps_filter):
        super().__init__()
        self.ps_filter = ps_filter

    def run(self):
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        x = screen.x() + (screen.width() // 2) - 400
        y = screen.y() + (screen.height() // 2) - 200

        ps_code = f"""
            Add-Type -AssemblyName System.Windows.Forms
            
            # Créer une nouvelle fenêtre parent invisible
            $parentForm = New-Object System.Windows.Forms.Form -Property @{{ 
                Size = New-Object System.Drawing.Size(0,0) # Taille minimale
                StartPosition = 'CenterScreen'
                TopMost = $true
                ShowInTaskbar = $false
                FormBorderStyle = 'None'
                Opacity = 0 # Rendre la fenêtre totalement transparente
            }}
            
            # Créer la boîte de dialogue de sélection de fichiers
            $openFileDialog = New-Object System.Windows.Forms.OpenFileDialog -Property @{{ 
                Filter = "{self.ps_filter}"
                Multiselect = $true
            }}
            
            # Afficher la boîte de dialogue en tant que fenêtre enfant de $parentForm
            $result = $openFileDialog.ShowDialog($parentForm)
            
            # Traiter les fichiers sélectionnés
            if ($result -eq [System.Windows.Forms.DialogResult]::OK) {{
                $selectedFiles = $openFileDialog.FileNames
                foreach ($file in $selectedFiles) {{
                    Write-Output $file
                }}
            }}
            
            # Fermer la fenêtre parent
            $parentForm.Close()
        """

        with tempfile.NamedTemporaryFile(delete=False, suffix=".ps1", mode="w", encoding="utf-8") as f:
            f.write(ps_code)
            ps_path = f.name

        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_path],
            capture_output=True, text=True
        )
        os.unlink(ps_path)

        file_paths = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
        self.finished.emit(file_paths)


class OWFileExtSelector(OWWidget):
    name = "File Extension Selector"
    description = "Select multiple extensions and files"
    icon = "icons/file_extensor.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/file_extensor.png"
    category = "AAIT - Input"
    gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/ow_file_ext_selector.ui")
    priority = 10

    selected_extensions = Setting(["*.txt"])
    selected_paths = Setting([])

    class Inputs:
        in_data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.in_data = None
        self.overlay = None

        uic.loadUi(self.gui_path, self)

        self.extension_list = self.findChild(QListWidget, "listExtensions")
        self.file_button = self.findChild(QPushButton, "fileButton")

        self.extension_list.setSelectionMode(QListWidget.MultiSelection)
        self.populate_extensions()
        self.restore_selected_extensions()

        self.file_button.clicked.connect(self.select_files)
        self.extension_list.itemSelectionChanged.connect(self.update_settings)

    def loadSettings(self):
        super().loadSettings()

    def update_settings(self):
        self.selected_extensions = self.get_selected_extensions()
        self.saveSettings()

    def restore_selected_extensions(self):
        for i in range(self.extension_list.count()):
            item = self.extension_list.item(i)
            if item.flags() != Qt.NoItemFlags:
                ext = item.data(Qt.UserRole)
                if ext in self.selected_extensions:
                    item.setSelected(True)
        self.update_settings()

    def restore_selected_paths(self):
        if self.selected_paths:
            self.commit_paths()

    def populate_extensions(self):
        def add_category(label):
            item = QListWidgetItem(label)
            item.setFlags(Qt.NoItemFlags)
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            item.setForeground(Qt.gray)
            self.extension_list.addItem(item)

        def add_extension(label, ext):
            item = QListWidgetItem(f"  {label}")
            item.setData(Qt.UserRole, ext)
            self.extension_list.addItem(item)

        extensions = {
            "Documents": [
                ("Text files (*.txt)", "*.txt"),
                ("Word documents (*.docx)", "*.docx"),
                ("PDF files (*.pdf)", "*.pdf"),
                ("Markdown (*.md)", "*.md"),
            ],
            "Tableurs": [
                ("Excel files (*.xlsx)", "*.xlsx"),
                ("CSV files (*.csv)", "*.csv"),
            ],
            "Images": [
                ("JPEG images (*.jpg *.jpeg)", "*.jpg *.jpeg"),
                ("PNG images (*.png)", "*.png"),
                ("GIF images (*.gif)", "*.gif"),
                ("SVG images (*.svg)", "*.svg"),
            ],
            "Audio": [
                ("MP3 (*.mp3)", "*.mp3"),
                ("WAV (*.wav)", "*.wav"),
            ],
            "Vidéo": [
                ("MP4 (*.mp4)", "*.mp4"),
                ("MKV (*.mkv)", "*.mkv"),
            ],
            "Archives": [
                ("ZIP (*.zip)", "*.zip"),
                ("RAR (*.rar)", "*.rar"),
                ("7-Zip (*.7z)", "*.7z"),
            ],
            "Code": [
                ("Python (*.py)", "*.py"),
                ("JSON (*.json)", "*.json"),
                ("HTML (*.html)", "*.html"),
                ("XML (*.xml)", "*.xml"),
                ("OWS (*.ows)", "*.ows"),
            ],
            "Autres": [
                ("All files (*.*)", "*.*")
            ]
        }

        for category, items in extensions.items():
            add_category(category)
            for label, ext in items:
                add_extension(label, ext)

    def get_selected_extensions(self):
        selected = [
            item.data(Qt.UserRole)
            for item in self.extension_list.selectedItems()
            if item.flags() != Qt.NoItemFlags
        ]
        return selected

    def show_overlay(self):
        if not self.overlay:
            self.overlay = QWidget()
            self.overlay.setWindowFlags(
                Qt.FramelessWindowHint |
                Qt.Tool  # ← PAS de WindowStaysOnTopHint
            )
            self.overlay.setAttribute(Qt.WA_TranslucentBackground)
            self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 150);")

            layout = QVBoxLayout(self.overlay)
            message = QLabel("Veuillez sélectionner un fichier...")
            message.setStyleSheet("color: white; font-size: 24px;")
            message.setAlignment(Qt.AlignCenter)
            layout.addWidget(message)
            self.overlay.setLayout(layout)

            screen_geometry = QApplication.primaryScreen().geometry()
            self.overlay.setGeometry(screen_geometry)
            self.overlay.show()

            QApplication.processEvents()

    def hide_overlay(self):
        if self.overlay:
            self.overlay.hide()
            self.overlay = None

    def select_files(self):
        self.show_overlay()

        selected_exts = self.get_selected_extensions()
        if not selected_exts:
            self.warning("Please select at least one extension.")
            self.hide_overlay()
            return

        all_patterns = ";".join(selected_exts)
        ps_filter = f"Supported files ({all_patterns})|{all_patterns}"

        self.thread = QThread()
        self.worker = FileDialogWorker(ps_filter)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_files_selected)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_files_selected(self, file_paths):
        self.hide_overlay()
        if file_paths:
            self.selected_paths = file_paths
            self.commit_paths()

    def commit_paths(self):
        var = StringVariable("file_path")
        domain = Domain([], metas=[var])
        table = Table(domain, [[p] for p in self.selected_paths])
        self.Outputs.data.send(table)

    @Inputs.in_data
    def set_input_data(self, data):
        self.in_data = data

    def handleNewSignals(self):
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ow = OWFileExtSelector()
    ow.show()
    sys.exit(app.exec_())
