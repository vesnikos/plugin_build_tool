from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from pathlib import Path
from pb_tool.utils.configuration import PbConf

cfg_file = Path(__file__).parent / 'pb_tool.cfg'
conf = PbConf(cfg_file)


class _MainWindow(QWidget):

    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.iface = kwargs['iface']

        self.setGeometry(100, 100, 200, 50)
        self.setWindowTitle(conf.plugin_name)

        grid = QGridLayout(self)
        self.setLayout(grid)

        label = QLabel('Hello World', self)
        label.setAlignment(Qt.AlignCenter)
        grid.addWidget(label, 0, 0)


def app(iface):
    # Here you can put your tests
    # if everything is correct return
    return _MainWindow(iface)
