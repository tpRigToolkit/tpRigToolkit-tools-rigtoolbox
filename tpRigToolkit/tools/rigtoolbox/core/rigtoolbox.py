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
from Qt.QtGui import *

import tpDcc as tp
from tpDcc.core import tool
from tpDcc.libs.python import yamlio
from tpDcc.libs.qt.core import base, window, icon
from tpDcc.libs.qt.widgets import toolset, progressbar, dock, message, buttons

import tpRigToolkit
from tpRigToolkit.tools.rigtoolbox.widgets import dock, base as base_widgets
from tpRigToolkit.tools.rigtoolbox.widgets import library

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
                tpRigToolkit.logger.warning(
                    'Impossible to launch RigToolbox server! Error while importing: {} >> {}'.format(dcc_mod_name, exc))
                return
        else:
            self._update_client()

    def help_mode(self, flag):
        if not flag:
            return

        help_event = toolset.ToolsetHelpEvent(
            self._rig_toolbox_widget.main_layout, self._toolbox_widgets, self._help_widget)

        return help_event

    def contents(self):
        dcc_name, dcc_version = self._client.get_dcc_info()

        self._client.load_plugins()

        commands_datas = dict()
        if dcc_name:
            commands_path = os.path.join(
                os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'dccs', dcc_name, 'commands')
            if os.path.isdir(commands_path):
                for command_file in os.listdir(commands_path):
                    if not command_file.endswith('.yaml'):
                        continue
                    commands_category = os.path.splitext(command_file)[0]
                    if commands_category in commands_datas:
                        continue
                    command_file_path = os.path.join(commands_path, command_file)
                    try:
                        commands_data = yamlio.read_file(command_file_path, maintain_order=True)
                    except Exception as exc:
                        tpRigToolkit.logger.error(
                            'Error while reading commands data from "{}" : {}'.format(command_file_path, exc))
                        continue
                    commands_datas[commands_category] = commands_data

        # Load widgets
        self._rig_toolbox_widget = RigToolboxWidget(parent=self)
        self._toolbox_widgets = list()
        if not dcc_name:
            from tpRigToolkit.tools.rigtoolbox.widgets import base
            toolbox_widget = base.BaseRigToolBoxWidget(
                title='Hello World!', commands_data=None, controller=None, parent=self)
            bug_icon = tp.ResourcesMgr().icon('bug')
            palette_icon = tp.ResourcesMgr().icon('palette')
            print('Bug Icon', bug_icon)
            print('Palette Icon', palette_icon)
            toolbox_widget.main_layout.addWidget(buttons.BaseButton('Hello', icon=bug_icon, parent=self))
            toolbox_widget.main_layout.addWidget(buttons.BaseButton('Hello2', icon=tp.ResourcesMgr().icon('download'), parent=self))
            toolbox_widget.main_layout.addWidget(buttons.BaseButton('Hello2', icon=palette_icon, parent=self))
            self._toolbox_widgets.append(toolbox_widget)

        if dcc_name == tp.Dccs.Maya:
            from tpRigToolkit.tools.rigtoolbox.dccs import maya
            self._toolbox_widgets = maya.get_toolbox_widgets(
                client=self._client, commands_data=commands_datas, parent=self)
        self._rig_toolbox_widget.load_widgets(self._toolbox_widgets, parent=self)

        library.Command.startCommand.connect(self._rig_toolbox_widget._on_start_command)
        library.Command.progressCommand.connect(self._rig_toolbox_widget._on_set_progress_command)
        library.Command.endCommand.connect(self._rig_toolbox_widget._on_end_command)
        # self.helpModeChanged.connect(rig_toolbox_widget.set_info_mode)

        return [self._rig_toolbox_widget]

    def reload_theme(self, theme=None):
        super(RigToolboxToolset, self).reload_theme(theme)

        if not theme:
            return
        stylesheet = theme.stylesheet()
        self._rig_toolbox_widget._base_window.setStyleSheet(stylesheet)


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

        self._progress = progressbar.BaseProgressBar(parent=self)
        self._progress.setMinimum(0)
        self._progress.setMaximum(100)

        self.main_layout.addWidget(self._base_window)
        self.main_layout.addWidget(self._progress)

    def load_widgets(self, widgets, parent=None):
        for w in widgets:
            if isinstance(w, base_widgets.BaseRigToolBoxWidget):
                w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                w.emitInfo.connect(self._on_show_success)
                w.emitError.connect(self._on_show_error)
                dock_widget = dock.DockWidget(w.title, parent=parent or self)
                info_button = QToolButton(parent=parent or self)
                info_button.setCheckable(True)
                info_button.setChecked(True)
                info_button.setIcon(tp.ResourcesMgr().icon('info', theme='color'))
                info_button.toggled.connect(w._on_toggle_info)
                dock_widget.add_button(info_button)
            else:
                dock_widget = dock.DockWidget(w.objectName(), parent=parent or self)

            dock_widget.setWidget(w)
            self._base_window.addDockWidget(Qt.TopDockWidgetArea, dock_widget)

    def _on_start_command(self, command_name):
        library.Command.command = command_name
        self._progress.setFormat('Executing command: "{}"'.format(command_name))
        self._progress.setValue(0)
        self._progress.theme_status = progressbar.BaseProgressBar.NORMAL_STATUS

    def _on_set_progress_command(self, value, msg=None):
        current_command = library.Command.command
        if not current_command:
            return

        self._progress.setValue(value)
        if msg:
            self._progress.setFormat(msg)

    def _on_end_command(self, was_success):
        current_command = library.Command.command
        if not current_command:
            return
        if was_success:
            self._progress.setFormat('Command "{}" executed successfully!'.format(current_command))
            self._progress.theme_status = progressbar.BaseProgressBar.SUCCESS_STATUS
        else:
            self._progress.setFormat('Error while executing command "{}"!'.format(current_command))
            self._progress.theme_status = progressbar.BaseProgressBar.ERROR_STATUS
        self._progress.setValue(100)
        library.Command.command = None

    def _on_show_success(self, success_message):
        message.PopupMessage.success(success_message, self, closable=True)

    def _on_show_error(self, error_message):
        message.PopupMessage.error(error_message, self, closable=True)
