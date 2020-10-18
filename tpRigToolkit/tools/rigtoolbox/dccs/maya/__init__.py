#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Init module of RigToolbox for Maya
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import traceback

import tpDcc as tp

LOGGER = tp.LogsMgr().get_logger('tpRigToolkit-tools-rigtoolbox')


def get_toolbox_widgets(client, parent=None):

    all_widgets = list()
    # try:
    #     from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import general
    #     general_widget = general.GeneralWidget(client=client)
    #     general_widget.setParent(parent)
    #     all_widgets.append(general_widget)
    # except Exception:
    #     LOGGER.exception('Error while creating general widget: "{}"'.format(traceback.format_exc()))
    #
    # try:
    #     from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import joint
    #     joint_widget = joint.JointWidget(client=client)
    #     joint_widget.setParent(parent)
    #     all_widgets.append(joint_widget)
    # except Exception:
    #     LOGGER.exception('Error while creating joint widget: "{}"'.format(traceback.format_exc()))

    try:
        from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import skin
        skinning_widget = skin.SkinningWidget(client=client)
        skinning_widget.setParent(parent)
        all_widgets.append(skinning_widget)
    except Exception:
        LOGGER.exception('Error while creating skinning widget: "{}"'.format(traceback.format_exc()))

    # try:
    #     from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import rename
    #     rename_widget = rename.RenameWidget()
    #     rename_widget.setParent(parent)
    #     all_widgets.append(rename_widget)
    # except Exception:
    #     LOGGER.exception('Error while creating renamer widget: "{}"'.format(traceback.format_exc()))
    #
    # try:
    #     from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import control
    #     control_widget = control.ControlWidget()
    #     control_widget.setParent(parent)
    #     all_widgets.append(control_widget)
    # except Exception:
    #     LOGGER.exception('Error while creating control widget: "{}"'.format(traceback.format_exc()))

    return all_widgets
