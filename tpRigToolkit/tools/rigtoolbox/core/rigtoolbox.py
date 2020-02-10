#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Collection of rigging tools
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

from functools import partial

from Qt.QtCore import *
from Qt.QtWidgets import *

import tpDccLib as tp
from tpQtLib.core import base

import tpRigToolkit


class RigToolboxTool(tpRigToolkit.Tool, object):
    def __init__(self, config):
        super(RigToolboxTool, self).__init__(config=config)

    def ui(self):
        super(RigToolboxTool, self).ui()

        self._rig_toolbox_widget = RigToolboxWidget()
        self.main_layout.addWidget(self._rig_toolbox_widget)


class RigToolboxWidget(base.BaseWidget, object):
    def __init__(self, parent=None):
        super(RigToolboxWidget, self).__init__(parent=parent)

    def ui(self):
        super(RigToolboxWidget, self).ui()
