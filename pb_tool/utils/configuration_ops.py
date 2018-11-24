import subprocess
from pathlib import Path
from typing import List
from configparser import ConfigParser

import click

from .files import pyuic5_exec, pyrcc5_exec, file_changed



