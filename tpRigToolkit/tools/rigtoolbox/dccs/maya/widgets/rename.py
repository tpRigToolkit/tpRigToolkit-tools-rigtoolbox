#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget for rename functionality
"""

from __future__ import print_function, division, absolute_import

import tpDcc
from tpDcc.tools.renamer.core import renamer

from tpRigToolkit.tools.rigtoolbox.widgets import base


class RenameWidget(base.BaseRigToolBoxWidget, object):
    def __init__(self, dev=True, parent=None):
        super(RenameWidget, self).__init__(title='Rename', parent=parent)

        names_config = tpDcc.ConfigsMgr().get_config(
            config_name='tpRigToolkit-names', environment='development' if dev else 'production')
        naming_config = tpDcc.ConfigsMgr().get_config(
            config_name='tpRigToolkit-naming', environment='development' if dev else 'production')

        rename_widget = renamer.RenamerToolsetWidget(
            names_config=names_config, naming_config=naming_config, parent=self)
        rename_widget.initialize()
        rename_widget._title_frame.setVisible(False)
        self.main_layout.addWidget(rename_widget)
