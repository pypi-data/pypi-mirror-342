import os
from PyQt5.QtWidgets import QPushButton, QListWidget, QListWidgetItem, QApplication, QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
from AnyQt.QtWidgets import QFileDialog
from Orange.widgets.widget import OWWidget, Output, Input
from Orange.data import Table, Domain, StringVariable
from Orange.widgets.settings import Setting

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.AAIT.utils import SimpleDialogQt
    from orangecontrib.AAIT.utils.MetManagement import get_local_store_path, GetFromRemote
else:
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.AAIT.utils import SimpleDialogQt
    from orangecontrib.AAIT.utils.MetManagement import get_local_store_path, GetFromRemote

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class OWFileExtSelector(OWWidget):
    name = "Javascript visualization"
    description = "Select multiple extensions and files"
    icon = "icons/visualizationer.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/visualizationer.png"
    category = "AAIT - Input"
    gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owvisualizationer.ui")
    priority = 10


    class Inputs:
        in_data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.in_data = None

        # Load UI
        uic.loadUi(self.gui_path, self)

        self.web_frame = self.findChild(QWidget, "webFrame")  # Doit exister dans le .ui
        self.web_view = QWebEngineView(self.web_frame)
        self.web_view.setMinimumSize(400, 300)
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Crée un layout si nécessaire
        layout = QVBoxLayout(self.web_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.web_view)

        # Charge ton fichier HTML local
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "designer/chart.html"))
        self.web_view.load(QUrl.fromLocalFile(html_path))


    @Inputs.in_data
    def set_input_data(self, data):
        self.in_data = data


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ow = OWFileExtSelector()
    ow.show()
    sys.exit(app.exec_())
