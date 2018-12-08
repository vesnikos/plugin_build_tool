from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget

from pb_tool.utils.configuration import PbConf

cfg_file = Path(__file__).parent / 'pb_tool.cfg'
conf = PbConf(cfg_file)


class _MainWindow(QWidget):

    def __init__(self, iface, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.iface = iface

        self.setGeometry(100, 100, 200, 50)
        self.setWindowTitle(conf.plugin_name)

        grid = QGridLayout(self)
        self.setLayout(grid)

        label = QLabel('Hello World', self)
        label.setAlignment(Qt.AlignCenter)
        grid.addWidget(label, 0, 0)


class MainWindow(_MainWindow):
    # https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins.html#init-py

    def __init__(self, iface, flags, *args, **kwargs):
        super().__init__(iface, flags, *args, **kwargs)
        self.iface = iface

    def initGui(self):
        # called when the plugin is loaded

        self._add_action(
                icon_path=conf.icon,
                text=conf.about,
                callback=self._run,
                parent=self.iface.mainWindow(),
                where='raster',
        )

    def _add_action(self, icon_path: str, text: str, callback, parent=None, where: str = None):
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

    def _run(self):
        # show the dialog
        self.show()
        self.dialog.adjustSize()
        # Run the dialog event loop
        result = self.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def unload(self):
        #  called when the plugin is unloaded
        pass


def app(iface):
    # Here you can some buisness logic before initialising the main window your tests
    # if everything is correct return
    return MainWindow(iface)
