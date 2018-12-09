from collections import namedtuple
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QGridLayout, QLabel, QPushButton, QWidget

# from pb_tool.utils.configuration import PbConf
#
# cfg_file = Path(__file__).parent / 'pb_tool.cfg'
# conf = PbConf(cfg_file)

PLUGIN_NAME = 'HelloWorld'
ICON = 'assets/icons/icon.png'
ABOUT = 'HelloWorld Addin'

QgsAction = namedtuple('QgsAction', 'action where')


class _MainWindow(QWidget):

    def __init__(self, iface, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.iface = iface

        self.setGeometry(100, 100, 200, 50)
        self.setWindowTitle(PLUGIN_NAME)

        grid = QGridLayout(self)
        self.setLayout(grid)

        label = QLabel('Hello World', self)
        label.setAlignment(Qt.AlignCenter)

        btn = QPushButton('About', self)
        btn.clicked.connect(self._show_about)
        grid.addWidget(label, 0, 0)
        grid.addWidget(btn, 1, 0)

    def _show_about(self):
        from .ui.about_widget import Ui_Form

        class About(QWidget, Ui_Form):
            def __init__(self, parent=self):
                super().__init__(parent)
                self.setupUi(self)

        about = About()
        about.show()


class MainWindow(_MainWindow):
    # https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins.html#init-py

    actions: List[QgsAction] = []

    def __init__(self, iface, *args, **kwargs):
        super().__init__(iface, *args, **kwargs)
        self.iface = iface

    def initGui(self):
        # called when the plugin is loaded

        def _add_action(icon_path: str, text: str, callback, parent=None, where: str = None):
            func = self.iface.addPluginToMenu
            if where is not None:
                if where == 'raster':
                    func = self.iface.addPluginToRasterMenu
                if where == 'vector':
                    func = self.iface.addPluginToVectorMenu
                if where == 'database':
                    func = self.iface.addPluginToDatabaseMenu
                if where == 'web':
                    func = self.iface.addPluginToWebMenu
            icon = QIcon(r':/' + icon_path)
            action = QAction(icon, text, parent)
            action.setObjectName(PLUGIN_NAME)
            action.setWhatsThis(ABOUT)

            action.triggered.connect(callback)

            self.iface.addToolBarIcon(action)
            func(PLUGIN_NAME, action)
            self.actions.append(QgsAction(action, where))

        _add_action(
                icon_path=ICON,
                text=ABOUT,
                callback=self.show,
                parent=self.iface.mainWindow(),
                where='raster',
        )

    def unload(self):
        #  called when the plugin is unloaded
        for q_action in self.actions:
            if q_action.where == 'raster':
                func = self.iface.removePluginRasterMenu
            if q_action.where == 'vector':
                func = self.iface.removePluginVectorMenu
            if q_action.where == 'database':
                func = self.iface.removePluginDatabaseMenu
            if q_action.where == 'web':
                func = self.iface.removePluginWebMenu
            self.iface.removeToolBarIcon(q_action.action)
            func(PLUGIN_NAME, q_action.action)


def app(iface):
    # Here you can some buisness logic before initialising the main window your tests
    # if everything is correct return
    return MainWindow(iface)
