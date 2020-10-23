#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains library with joint functions
"""

from __future__ import print_function, division, absolute_import

from tpDcc.libs.python import python

import tpDcc as tp
import tpDcc.dccs.maya as maya
from tpDcc.dccs.maya.core import decorators, joint as joint_utils, curve as curve_utils


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def start_joint_tool():
    """
    Initializes joint tool
    """

    out_dict = {'success': False, 'result': list()}

    try:
        tp.Dcc.start_joint_tool()
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to open joint tool: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def create_new_joint_on_center(transforms=None):
    """
    Creates a new joint in the center of the selected transforms
    """

    out_dict = {'success': False, 'result': None}

    try:
        selection = maya.cmds.ls(sl=True)
        if transforms:
            result = joint_utils.create_joint_on_center()
        else:
            if '.[' in selection:
                result = joint_utils.create_joints_on_selected_components_center()
            else:
                result = joint_utils.create_joint_on_center()
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to open joint tool: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def create_joints_on_selected_components_center():
    """
    Creates new joints on the selected components center
    """

    out_dict = {'success': False, 'result': None}

    try:

        result = joint_utils.create_joints_on_selected_components_center()
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to open joint tool: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def insert_joints(joints=None, num_joints=1):
    """
    Inserts new joints between selected joint and its direct child
    :param joints: int
    :param num_joints: int
    """

    out_dict = {'success': False, 'result': None}

    joints = joints or tp.Dcc.selected_nodes_of_type(node_type='joint')
    joints = python.force_list(joints)
    if not joints:
        out_dict['msg'] = 'No joints to insert joints into found.'
        return out_dict

    try:

        result = joint_utils.insert_joints(joints=joints, joint_count=num_joints)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to insert joints: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def create_joints_on_curve(curve=None, num_joints=1):

    out_dict = {'success': False, 'result': list()}

    valid_curves = list()
    curves = curve or tp.Dcc.selected_nodes_of_type(node_type='transform')
    curves = python.force_list(curves)
    for curve in curves:
        if not curve_utils.is_a_curve(curve):
            continue
        valid_curves.append(curve)
    if not valid_curves:
        out_dict['msg'] = 'No curves to create joints on found.'
        return out_dict

    try:
        for curve in valid_curves:
            new_joint = joint_utils.create_oriented_joints_along_curve(curve, num_joints)
            out_dict['result'].append(new_joint)
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to create joints on curve: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def snap_joints_to_curve(joints=None, curve=None, num_joints=1):

    out_dict = {'success': False, 'result': dict()}

    valid_joints = list()
    joints = joints or tp.Dcc.selected_nodes_of_type(node_type='joint')
    joints = python.force_list(joints)
    for joint in joints:
        if not tp.Dcc.object_type(joint) == 'joint':
            continue
        valid_joints.append(joint)
    if not valid_joints:
        out_dict['msg'] = 'No joints to snap to curve found.'
        return out_dict

    valid_curves = list()
    curves = curve or tp.Dcc.selected_nodes_of_type(node_type='transform')
    curves = python.force_list(curves)
    for curve in curves:
        if not curve_utils.is_a_curve(curve):
            continue
        valid_curves.append(curve)

    try:
        for curve in valid_curves:
            new_joints = curve_utils.snap_joints_to_curve(valid_joints, curve=curve, count=num_joints)
            out_dict['result'][curve] = new_joints
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to snap joints to curve: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


def check_joint_labels(joints=None):

    out_dict = {'success': False, 'result': False}

    valid_joints = list()
    joints = joints or tp.Dcc.selected_nodes_of_type(node_type='joint')
    joints = python.force_list(joints)
    for joint in joints:
        if not tp.Dcc.object_type(joint) == 'joint':
            continue
        valid_joints.append(joint)
    if not valid_joints:
        out_dict['msg'] = 'No joints to check found.'
        return out_dict

    try:
        result = joint_utils.check_joint_labels(valid_joints)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to check joints label: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict
