#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base class for tpRigToolbox widgets
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import *
from Qt.QtWidgets import *


class BaseRigToolBoxWidget(QFrame, object):

    emitInfo = Signal(str)
    emitWarning = Signal(str)
    emitError = Signal(str, object)

    def __init__(self, title, parent=None):
        super(BaseRigToolBoxWidget, self).__init__(parent=parent)

        self._title = title

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.main_layout)

    @property
    def title(self):
        return self._title

    def _create_button(self, text, icon, fn, status=None, tooltip=None):
        """
        Internal function to easily create buttons for the box widget
        :param text:
        :param icon:
        :param fn:
        :param status:
        :param tooltip:
        :return:
        """

        new_btn = QToolButton()
        new_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if icon:
            new_btn.setIcon(icon)
        new_btn.setText(text)
        new_btn.setStatusTip(status or text)
        new_btn.setToolTip(tooltip or text)
        if fn:
            new_btn.clicked.connect(fn)

        return new_btn
