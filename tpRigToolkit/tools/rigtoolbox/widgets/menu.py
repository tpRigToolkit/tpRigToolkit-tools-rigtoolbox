#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains menu widget for tpRigToolbox.tools.rigtoolbox
"""

from __future__ import print_function, division, absolute_import

from Qt.QtWidgets import *

import tpDcc
from tpDcc.libs.qt.widgets import buttons


class RigToolBoxMenu(QFrame, object):
    def __init__(self, parent=None):
        super(RigToolBoxMenu, self).__init__(parent=parent)

        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet('background-color: rgb(50, 50, 50);')

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        self.title_lbl = QLabel()
        left_arrow_icon = tpDcc.ResourcesMgr().icon('left_arrow')
        right_arrow_icon = tpDcc.ResourcesMgr().icon('right_arrow')
        self.left_arrow = buttons.IconButton(icon=left_arrow_icon)
        self.right_arrow = buttons.IconButton(icon=right_arrow_icon)
        main_layout.addWidget(self.left_arrow)
        main_layout.addItem(QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
        main_layout.addWidget(self.title_lbl)
        main_layout.addItem(QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
        main_layout.addWidget(self.right_arrow)