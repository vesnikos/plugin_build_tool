from PyQt5.QtWidgets import QWidget
from pathlib import Path
from pb_tool.utils.configuration import PbConf

cfg_file = Path(__file__).parent / 'pb_tool.cfg'
conf = PbConf(cfg_file)


class _MainWindow(QWidget):

    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self.setGeometry(100, 100, 200, 50)
        self.setWindowTitle(conf.plugin_name)
