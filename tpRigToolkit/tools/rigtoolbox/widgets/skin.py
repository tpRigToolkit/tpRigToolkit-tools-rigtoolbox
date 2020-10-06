#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget for rig skinning functionality
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import *
from Qt.QtWidgets import *

import tpDcc as tp
from tpDcc.libs.python import decorators
from tpDcc.libs.qt.widgets import dividers

from tpRigToolkit.tools.rigtoolbox.widgets import base

if tp.is_maya():
    import tpDcc.dccs.maya as maya
    from tpDcc.dccs.maya.core import skin, decorators as maya_decorators
    undo_decorator = maya_decorators.undo_chunk
    repeat_last_decorator = maya_decorators.repeat_static_command
else:
    undo_decorator = decorators.empty_decorator
    repeat_last_decorator = decorators.empty_decorator


class SkinningWidget(base.BaseRigToolBoxWidget, object):
    def __init__(self, parent=None):
        super(SkinningWidget, self).__init__(title='Skinning', parent=parent)

        self._setup_create_tools()

            # self.main_layout = QVBoxLayout()
            # self.main_layout.setContentsMargins(0, 0, 0, 0)
            # self.main_layout.setSpacing(0)
            # self.setLayout(self.main_layout)
            #
            # self.main_layout.addWidget(QPushButton('Skin'))

    def smooth_bind_skin(self):
        skin.apply_smooth_bind()

    def _setup_create_tools(self):
        self.main_layout.addWidget(dividers.Divider('C R E A T E'))
        self.create_layout = QGridLayout()
        self.create_layout.setAlignment(Qt.AlignLeft)
        self.main_layout.addLayout(self.create_layout)

        self.smooth_bind_btn = QToolButton()
        smooth_skin_icon = tp.ResourcesMgr().icon('smooth_skin', extension='png')
        self.smooth_bind_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.smooth_bind_btn.setIcon(smooth_skin_icon)
        self.smooth_bind_btn.setText('Smooth Bind')
        self.smooth_bind_btn.clicked.connect(self.smooth_bind_skin)
        self.create_layout.addWidget(self.smooth_bind_btn, 0, 0)




