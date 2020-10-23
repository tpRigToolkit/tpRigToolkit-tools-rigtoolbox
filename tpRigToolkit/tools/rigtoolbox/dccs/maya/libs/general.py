#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains library with general functions
"""

from __future__ import print_function, division, absolute_import

import tpDcc as tp
from tpDcc.libs.python import python
import tpDcc.dccs.maya as maya
from tpDcc.dccs.maya.core import decorators, transform as xform_utils

from tpRigToolkit.tools.rigtoolbox.widgets import library


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def delete_history(transforms=None):
    """
    Delete history of selected transforms
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No nodes to delete history of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Deleting history: {}'.format(node))
        try:
            tp.Dcc.delete_history(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to delete history in node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def freeze_transforms(transforms=None):
    """
    Freeze selected transforms
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to freeze transforms of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Freezing transforms: {}'.format(node))
        try:
            tp.Dcc.freeze_transforms(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to freeze transforms in node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def move_pivot_to_zero(transforms=None):
    """
    Moves selected nodes pivots to zero (0, 0, 0 in the world)
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to move pivot to zero of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Moving pivot to zero: {}'.format(node))
        try:
            tp.Dcc.move_pivot_to_zero(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible move pivot to zero for node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def lock_all_transforms(transforms=None):
    """
    Locks all the transform channels of the given transforms nodes
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to lock all transform channels of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Locking all transforms: {}'.format(node))
        try:
            tp.Dcc.lock_translate_attributes(node)
            tp.Dcc.lock_rotate_attributes(node)
            tp.Dcc.lock_scale_attributes(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to lock all transforms for node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def lock_translation(transforms=None):
    """
    Locks all translation channels of the given transforms nodes
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to lock all translation channels of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Locking translation channels: {}'.format(node))
        try:
            tp.Dcc.lock_translate_attributes(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to lock translate channels in node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def lock_rotation(transforms=None):
    """
    Locks all rotation channels of the given transforms nodes
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to lock all rotation channels of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Locking rotation channels: {}'.format(node))
        try:
            tp.Dcc.lock_rotate_attributes(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to lock rotations channel in node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def lock_scale(transforms=None):
    """
    Locks all scale channels of the given transforms nodes
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to lock all scale channels of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Locking scale channels: {}'.format(node))
        try:
            tp.Dcc.lock_scale_attributes(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to lock scale channels in node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def lock_visibility(transforms=None):
    """
    Locks visibility channel of the given transforms nodes
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to lock all scale channels of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Locking visibility channel: {}'.format(node))
        try:
            tp.Dcc.lock_visibility_attribute(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to lock visibility channel in node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def unlock_all_transforms(transforms=None):
    """
    Locks all the transform channels of the given transforms nodes
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to unlock all transform channels of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Unlocking all transforms: {}'.format(node))
        try:
            tp.Dcc.unlock_translate_attributes(node)
            tp.Dcc.unlock_rotate_attributes(node)
            tp.Dcc.unlock_scale_attributes(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to unlock all transforms for node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def unlock_translation(transforms=None):
    """
    Locks all translation channels of the given transforms nodes
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to unlock all translation channels of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Unlocking translation channels: {}'.format(node))
        try:
            tp.Dcc.unlock_translate_attributes(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to unlock translate channels in node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def unlock_rotation(transforms=None):
    """
    Locks all rotation channels of the given transforms nodes
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to unlock all rotation channels of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Unlocking rotation channels: {}'.format(node))
        try:
            tp.Dcc.unlock_rotate_attributes(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to unlock rotations channel in node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def unlock_scale(transforms=None):
    """
    Locks all scale channels of the given transforms nodes
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to unlock all scale channels of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Unlocking scale channels: {}'.format(node))
        try:
            tp.Dcc.unlock_scale_attributes(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to unlock scale channels in node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def unlock_visibility(transforms=None):
    """
    Locks visibility channel of the given transforms nodes
    """

    out_dict = {'success': False, 'result': list()}

    transforms = python.force_list(transforms or tp.Dcc.selected_nodes_of_type(node_type='transform') or list())
    if not transforms:
        out_dict['msg'] = 'No transforms to unlock all scale channels of. Select at least one.'
        return out_dict

    percentage = 100.0 / len(transforms)

    for i, node in enumerate(transforms):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Unlocking scale channels: {}'.format(node))
        try:
            tp.Dcc.unlock_visibility_attribute(node)
            out_dict['result'].append(node)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to unlock visibility channel in node: "{}" : {}'.format(node, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def match_transform(source_transform=None, target_transform=None):
    """
    Matches all the transforms of the source node to the transforms of the given target node(s)
    """

    out_dict = {'success': False, 'result': list()}

    selection = tp.Dcc.selected_nodes_of_type(node_type='transform')
    source_transform = source_transform or selection[0] if python.index_exists_in_list(selection, 0) else None
    if not source_transform:
        out_dict['msg'] = 'No source transform given to match against target transform.'
        return out_dict
    target_transform = target_transform or selection[1:] if len(selection) > 1 else None
    if not source_transform:
        out_dict['msg'] = 'No target transform(s) given to match source transform against.'
        return out_dict
    source_transform = python.force_list(source_transform)
    target_transform = python.force_list(target_transform)

    percentage = 100.0 / len(source_transform)

    for i, source in enumerate(source_transform):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Matching transforms: {}'.format(source))
        try:
            maya.cmds.delete(maya.cmds.parentConstraint(target_transform, source, maintainOffset=False))
            maya.cmds.delete(maya.cmds.scaleConstraint(target_transform, source, maintainOffset=False))

            # For joints, we store now rotation data in jointOrient attribute
            if tp.Dcc.node_type(source) == 'joint':
                for axis in 'XYZ':
                    joint_orient_attr = 'jointOrient{}'.format(axis)
                    joint_rotation_attr = 'rotate{}'.format(axis)
                    tp.Dcc.set_attribute_value(source, joint_orient_attr, 0.0)
                    joint_rotation = tp.Dcc.get_attribute_value(source, joint_rotation_attr)
                    tp.Dcc.set_attribute_value(source, joint_orient_attr, joint_rotation)
                    tp.Dcc.set_attribute_value(source, joint_rotation_attr, 0.0)

            out_dict['result'].append(source)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to match node "{}" transforms to "{}" : {}'.format(
                source_transform, target_transform, exc)
            return out_dict

    matched_nodes = out_dict.get('result', None)
    if matched_nodes:
        tp.Dcc.select_node(matched_nodes)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def match_translation(source_transform=None, target_transform=None):
    """
    Matches translation of the source node to the translation of the given target node(s)
    """

    out_dict = {'success': False, 'result': list()}

    selection = tp.Dcc.selected_nodes_of_type(node_type='transform')
    source_transform = source_transform or selection[0] if python.index_exists_in_list(selection, 0) else None
    if not source_transform:
        out_dict['msg'] = 'No source transform given to match against target translation.'
        return out_dict
    target_transform = target_transform or selection[1:] if len(selection) > 1 else None
    if not source_transform:
        out_dict['msg'] = 'No target transform(s) given to match source translation against.'
        return out_dict
    source_transform = python.force_list(source_transform)
    target_transform = python.force_list(target_transform)

    percentage = 100.0 / len(source_transform)

    for i, source in enumerate(source_transform):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Matching translation: {}'.format(source))
        try:
            maya.cmds.delete(maya.cmds.pointConstraint(target_transform, source, maintainOffset=False))
            out_dict['result'].append(source)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to match node "{}" translation to "{}" : {}'.format(
                source_transform, target_transform, exc)
            return out_dict

    matched_nodes = out_dict.get('result', None)
    if matched_nodes:
        tp.Dcc.select_node(matched_nodes)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def match_rotation(source_transform=None, target_transform=None):
    """
    Matches rotation of the source node to the rotation of the given target node(s)
    """

    out_dict = {'success': False, 'result': list()}

    selection = tp.Dcc.selected_nodes_of_type(node_type='transform')
    source_transform = source_transform or selection[0] if python.index_exists_in_list(selection, 0) else None
    if not source_transform:
        out_dict['msg'] = 'No source transform given to match against target rotation.'
        return out_dict
    target_transform = target_transform or selection[1:] if len(selection) > 1 else None
    if not source_transform:
        out_dict['msg'] = 'No target transform(s) given to match source rotation against.'
        return out_dict
    source_transform = python.force_list(source_transform)
    target_transform = python.force_list(target_transform)

    percentage = 100.0 / len(source_transform)

    for i, source in enumerate(source_transform):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Matching rotation: {}'.format(source))
        try:
            maya.cmds.delete(maya.cmds.orientConstraint(target_transform, source, maintainOffset=False))

            # For joints, we store now rotation data in jointOrient attribute
            if tp.Dcc.node_type(source) == 'joint':
                for axis in 'XYZ':
                    joint_orient_attr = 'jointOrient{}'.format(axis)
                    joint_rotation_attr = 'rotate{}'.format(axis)
                    tp.Dcc.set_attribute_value(source, joint_orient_attr, 0.0)
                    joint_rotation = tp.Dcc.get_attribute_value(source, joint_rotation_attr)
                    tp.Dcc.set_attribute_value(source, joint_orient_attr, joint_rotation)
                    tp.Dcc.set_attribute_value(source, joint_rotation_attr, 0.0)

            out_dict['result'].append(source)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to match node "{}" rotation to "{}" : {}'.format(
                source_transform, target_transform, exc)
            return out_dict

    matched_nodes = out_dict.get('result', None)
    if matched_nodes:
        tp.Dcc.select_node(matched_nodes)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def match_scale(source_transform=None, target_transform=None):
    """
    Matches scale of the source node to the scale of the given target node(s)
    """

    out_dict = {'success': False, 'result': list()}

    selection = tp.Dcc.selected_nodes_of_type(node_type='transform')
    source_transform = source_transform or selection[0] if python.index_exists_in_list(selection, 0) else None
    if not source_transform:
        out_dict['msg'] = 'No source transform given to match against target scale.'
        return out_dict
    target_transform = target_transform or selection[1:] if len(selection) > 1 else None
    if not source_transform:
        out_dict['msg'] = 'No target transform(s) given to match source scale against.'
        return out_dict
    source_transform = python.force_list(source_transform)
    target_transform = python.force_list(target_transform)

    percentage = 100.0 / len(source_transform)

    for i, source in enumerate(source_transform):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Matching scale: {}'.format(source))
        try:
            maya.cmds.delete(maya.cmds.scaleConstraint(target_transform, source, maintainOffset=False))
            out_dict['result'].append(source)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to match node "{}" scale to "{}" : {}'.format(
                source_transform, target_transform, exc)
            return out_dict

    matched_nodes = out_dict.get('result', None)
    if matched_nodes:
        tp.Dcc.select_node(matched_nodes)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def combine_meshes(meshes=None, new_mesh_name=None):
    """
    Combines given meshes into one transform
    """

    out_dict = {'success': False, 'result': None}

    meshes = meshes or tp.Dcc.selected_nodes_of_type(node_type='transform')
    meshes = python.force_list(meshes)
    if not meshes:
        out_dict['msg'] = 'No meshes to combine selected.'
        return out_dict
    if len(meshes) < 2:
        out_dict['msg'] = 'You need to select at least two meshes to combine.'
        return out_dict
    new_mesh_name = new_mesh_name or tp.Dcc.node_short_name(meshes[0])

    parent_node = None
    node_parents = list(set([tp.Dcc.node_parent(mesh) for mesh in meshes]))
    if all(parent == node_parents[0] for parent in node_parents):
        parent_node = node_parents[0]

    try:
        combined_mesh = tp.Dcc.combine_meshes(construction_history=False)
        if not combined_mesh:
            out_dict['msg'] = 'Combine operation was done but not combined mesh was generated'
            return out_dict
        combined_mesh = tp.Dcc.rename_node(combined_mesh, new_mesh_name)
        if parent_node:
            tp.Dcc.set_parent(combined_mesh, parent_node)

        out_dict['result'] = combined_mesh
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to combine meshes "{}" : {}'.format(meshes, exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def mirror_mesh(mesh=None):
    """
    Mirror given meshes
    """

    out_dict = {'success': False, 'result': list()}

    meshes = mesh or tp.Dcc.selected_nodes_of_type(node_type='transform')
    meshes = python.force_list(meshes)
    if not meshes:
        out_dict['msg'] = 'No meshes to mirror selected.'
        return out_dict

    for mesh in meshes:
        try:
            parent_node = tp.Dcc.node_parent(mesh)
            mirror_geo_name = xform_utils.find_transform_right_side(mesh, check_if_exists=False)
            mirror_geo = maya.cmds.duplicate(mesh, n=mirror_geo_name or None)
            root = maya.cmds.group(empty=True, world=True)
            maya.cmds.parent(mirror_geo, root)
            maya.cmds.setAttr('{}.rx'.format(root), 180)
            for axis in 'xyz':
                maya.cmds.setAttr('{}.s{}'.format(root, axis), -1)
            maya.cmds.parent(mirror_geo, world=True)
            maya.cmds.delete(root)
            maya.cmds.makeIdentity(mirror_geo, apply=True, t=False, r=True, s=True, n=False, pn=True)
            if parent_node:
                tp.Dcc.set_parent(mirror_geo, parent_node)
            out_dict['result'].append(mirror_geo)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to mirror meshes "{}" : '.format(meshes, exc)
            return out_dict

    out_dict['success'] = True

    return out_dict


def open_symmetry_tool():

    out_dict = {'success': False, 'result': None}

    try:
        tool = tp.ToolsMgr().launch_tool_by_id('tpRigToolkit-tools-symmesh')
        out_dict['result'] = tool
    except Exception as exc:
        out_dict['msg'] = 'Was not to open symmetry tool : {} '.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict
