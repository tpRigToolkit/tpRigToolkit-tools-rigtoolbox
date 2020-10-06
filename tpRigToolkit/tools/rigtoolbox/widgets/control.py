#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget for rig control functionality
"""

from __future__ import print_function, division, absolute_import

from tpRigToolkit.tools.rigtoolbox.widgets import base
from tpRigToolkit.tools.controlrig.core import controlrig


class ControlWidget(base.BaseRigToolBoxWidget, object):
    def __init__(self, parent=None):
        super(ControlWidget, self).__init__(title='Control', parent=parent)

        ctrl_rig = controlrig.ControlRigToolset(collapsable=False, parent=self)
        ctrl_rig.initialize()
        self.main_layout.addWidget(ctrl_rig)
