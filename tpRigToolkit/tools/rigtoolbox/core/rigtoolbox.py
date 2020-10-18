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
import importlib

from Qt.QtCore import *
from Qt.QtWidgets import *

import tpDcc as tp
from tpDcc.core import tool
from tpDcc.libs.qt.core import base, window
from tpDcc.libs.qt.widgets import layouts, toolset, progressbar, dock, label

from tpRigToolkit.tools.rigtoolbox.widgets import dock

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

    def setup_client(self):

        from tpRigToolkit.tools.rigtoolbox.core import rigtoolboxclient

        self._client = rigtoolboxclient.RigToolboxClient()
        self._client.signals.dccDisconnected.connect(self._on_dcc_disconnected)

        if not tp.is_standalone():
            dcc_mod_name = '{}.dccs.{}.rigtoolboxserver'.format(TOOL_ID.replace('-', '.'), tp.Dcc.get_name())
            try:
                mod = importlib.import_module(dcc_mod_name)
                if hasattr(mod, 'RigToolboxServer'):
                    server = mod.RigToolboxServer(self, client=self._client, update_paths=False)
                    self._client.set_server(server)
                    self._update_client()
            except Exception as exc:
                tp.logger.warning(
                    'Impossible to launch RigToolbox server! Error while importing: {} >> {}'.format(dcc_mod_name, exc))
                return
        else:
            self._update_client()

    def contents(self):
        dcc_name, dcc_version = self._client.get_dcc_info()

        self._client.load_plugins()

        rig_toolbox_widget = RigToolboxWidget(parent=self)

        toolbox_widgets = list()
        if dcc_name == tp.Dccs.Maya:
            from tpRigToolkit.tools.rigtoolbox.dccs import maya
            toolbox_widgets = maya.get_toolbox_widgets(client=self._client, parent=rig_toolbox_widget)

        rig_toolbox_widget.load_widgets(toolbox_widgets)

        return [rig_toolbox_widget]


class RigToolboxWidget(base.BaseWidget, object):

    WindowName = 'RigToolBoxWidgetsWindow'

    def __init__(self, parent=None):
        super(RigToolboxWidget, self).__init__(parent=parent)

    def ui(self):
        super(RigToolboxWidget, self).ui()

        self._base_window = window.BaseWindow(parent=self)
        self._base_window.centralWidget().hide()
        self._base_window.setDockOptions(
            QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks | QMainWindow.AllowTabbedDocks)
        self._base_window.setWindowFlags(Qt.Widget)

        self.main_layout.addWidget(self._base_window)

        description_layout = layouts.HorizontalLayout()
        self._description_label = label.BaseLabel()
        description_layout.addStretch()
        description_layout.addWidget(self._description_label)
        description_layout.addStretch()
        self.main_layout.addLayout(description_layout)

        self._progress = progressbar.BaseProgressBar(parent=self)
        self.main_layout.addWidget(self._progress)

    def load_widgets(self, widgets):
        for w in widgets:
            w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            w.setDescription.connect(self._on_set_description)
            dock_widget = dock.DockWidget(w.title)
            dock_widget.setWidget(w)
            self._base_window.addDockWidget(Qt.TopDockWidgetArea, dock_widget)

    def _on_set_description(self, description):
        self._description_label.setText(description)

