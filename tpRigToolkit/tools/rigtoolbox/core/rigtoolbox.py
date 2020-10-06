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

import os

from tpDcc.core import tool
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import stack, toolset

from tpRigToolkit.tools.rigtoolbox.widgets import menu, general, joint, skin, control, rename

# Defines ID of the tool
TOOL_ID = 'tpRigToolkit-tools-rigtoolbox'


class RigToolboxTool(tool.DccTool, object):
    def __init__(self, *args, **kwargs):
        super(RigToolboxTool, self).__init__(*args, **kwargs)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.DccTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'Rig ToolBox',
            'id': 'tpRigToolkit-tools-rigtoolbox',
            'logo': 'rigtoolbox',
            'icon': 'rigtoolbox',
            'tooltip': 'Collection of tools to improve the rigging process',
            'tags': ['tpRigToolkit', 'rig', 'tools', 'toolbox'],
            'logger_dir': os.path.join(os.path.expanduser('~'), 'tpRigToolkit', 'logs', 'tools'),
            'logger_level': 'INFO',
            'is_checkable': False,
            'is_checked': False,
            'menu_ui': {'label': 'Rig ToolBox', 'load_on_startup': False, 'color': '', 'background_color': ''}
        }
        base_tool_config.update(tool_config)

        return base_tool_config

    def launch(self, *args, **kwargs):
        return self.launch_frameless(*args, **kwargs)


class RigToolboxToolset(toolset.ToolsetWidget, object):

    ID = TOOL_ID

    def __init__(self, *args, **kwargs):
        super(RigToolboxToolset, self).__init__(*args, **kwargs)

    def contents(self):
        rig_toolbox_widget = RigToolboxWidget(parent=self)

        return [rig_toolbox_widget]


class RigToolboxWidget(base.BaseWidget, object):
    def __init__(self, parent=None):
        super(RigToolboxWidget, self).__init__(parent=parent)

    def ui(self):
        super(RigToolboxWidget, self).ui()

        self._stack = stack.SlidingStackedWidget()
        self._rig_toolbox_menu = menu.RigToolBoxMenu()
        self.main_layout.addWidget(self._stack)
        self.main_layout.addWidget(self._rig_toolbox_menu)

        self._general_widget = general.GeneralWidget(parent=self)
        self._joint_widget = joint.JointWidget(parent=self)
        self._rename_widget = rename.RenameWidget(parent=self)
        self._control_widget = control.ControlWidget(parent=self)
        self._skinning_widget = skin.SkinningWidget(parent=self)
        for w in [
            self._general_widget, self._joint_widget, self._rename_widget,
            self._control_widget, self._skinning_widget
        ]:
            self._stack.addWidget(w)

        self._rig_toolbox_menu.title_lbl.setText(self._general_widget.title)

    def setup_signals(self):
        self._rig_toolbox_menu.right_arrow.clicked.connect(self._on_next_widget)
        self._rig_toolbox_menu.left_arrow.clicked.connect(self._on_prev_widget)

    def _on_next_widget(self):
        self._stack.slide_in_next()
        self._rig_toolbox_menu.title_lbl.setText(self._stack.current_widget.title)

    def _on_prev_widget(self):
        self._stack.slide_in_prev()
        self._rig_toolbox_menu.title_lbl.setText(self._stack.current_widget.title)
