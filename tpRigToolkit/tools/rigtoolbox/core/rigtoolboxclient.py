#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains rig toolbox client implementation
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

from tpDcc.core import client


class RigToolboxClient(client.DccClient, object):

    PORT = 19344

    # =================================================================================================================
    # MAYA - GENERAL
    # =================================================================================================================

    def delete_history(self, transforms=None):
        cmd = {
            'cmd': 'delete_history',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def freeze_transforms(self, transforms=None):
        cmd = {
            'cmd': 'freeze_transforms',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def move_pivot_to_zero(self, transforms=None):
        cmd = {
            'cmd': 'move_pivot_to_zero',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def lock_all_transforms(self, transforms=None):
        cmd = {
            'cmd': 'lock_all_transforms',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def lock_translation(self, transforms=None):
        cmd = {
            'cmd': 'lock_translation',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def lock_rotation(self, transforms=None):
        cmd = {
            'cmd': 'lock_rotation',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def lock_scale(self, transforms=None):
        cmd = {
            'cmd': 'lock_scale',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def lock_visibility(self, transforms=None):
        cmd = {
            'cmd': 'lock_visibility',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def unlock_all_transforms(self, transforms=None):
        cmd = {
            'cmd': 'unlock_all_transforms',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def unlock_translation(self, transforms=None):
        cmd = {
            'cmd': 'unlock_translation',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def unlock_rotation(self, transforms=None):
        cmd = {
            'cmd': 'unlock_rotation',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def unlock_scale(self, transforms=None):
        cmd = {
            'cmd': 'unlock_scale',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def unlock_visibility(self, transforms=None):
        cmd = {
            'cmd': 'unlock_visibility',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def match_transform(self, source_transform=None, target_transform=None):
        cmd = {
            'cmd': 'match_transform',
            'source_transform': source_transform,
            'target_transform': target_transform
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def match_translation(self, source_transform=None, target_transform=None):
        cmd = {
            'cmd': 'match_translation',
            'source_transform': source_transform,
            'target_transform': target_transform
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def match_rotation(self, source_transform=None, target_transform=None):
        cmd = {
            'cmd': 'match_rotation',
            'source_transform': source_transform,
            'target_transform': target_transform
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def match_scale(self, source_transform=None, target_transform=None):
        cmd = {
            'cmd': 'match_scale',
            'source_transform': source_transform,
            'target_transform': target_transform
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def combine_meshes(self, meshes=None, new_mesh_name=None):
        cmd = {
            'cmd': 'combine_meshes',
            'meshes': meshes,
            'new_mesh_name': new_mesh_name
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def mirror_mesh(self, meshes=None):
        cmd = {
            'cmd': 'mirror_mesh',
            'meshes': meshes,
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def open_symmetry_tool(self):
        cmd = {
            'cmd': 'open_symmetry_tool'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    # =================================================================================================================
    # MAYA - JOINTS
    # =================================================================================================================

    def start_joint_tool(self):
        cmd = {
            'cmd': 'start_joint_tool'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def create_new_joint_on_center(self, transforms=None):
        cmd = {
            'cmd': 'create_new_joint_on_center',
            'transforms': transforms
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def create_new_joints_on_selected_components(self):
        cmd = {
            'cmd': 'create_new_joints_on_selected_components'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def insert_joints(self, joints=None, num_joints=1):
        cmd = {
            'cmd': 'insert_joints',
            'joints': joints,
            'num_joints': num_joints
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def create_joints_on_curve(self, curve=None, num_joints=1):
        cmd = {
            'cmd': 'create_joints_on_curve',
            'curve': curve,
            'num_joints': num_joints
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def snap_joints_to_curve(self, joints=None, curve=None, num_joints=1):
        cmd = {
            'cmd': 'snap_joints_to_curve',
            'joints': joints,
            'curve': curve,
            'num_joints': num_joints
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    # =================================================================================================================
    # MAYA - SKINNING
    # =================================================================================================================

    def smooth_bind_skin(self, geo_node=None, show_options=False):
        cmd = {
            'cmd': 'smooth_bind_skin',
            'geo_node': geo_node,
            'show_options': show_options
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def rigid_bind_skin(self, geo_node=None, show_options=False):
        cmd = {
            'cmd': 'rigid_bind_skin',
            'geo_node': geo_node,
            'show_options': show_options
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def detach_bind_skin(self, geo_node=None, show_options=False):
        cmd = {
            'cmd': 'detach_bind_skin',
            'geo_node': geo_node,
            'show_options': show_options
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def open_paint_skin_weights_tool(self, show_options=False):
        cmd = {
            'cmd': 'open_paint_skin_weights_tool',
            'show_options': show_options
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def check_joints_labels(self, joints=None):
        cmd = {
            'cmd': 'check_joints_labels',
            'joints': joints
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['result']

    def mirror_skin_weights(
            self, mesh=None, auto_assign_labels=True, left_side_label='*_l_*', right_side_label='*_r_*',
            show_options=False):
        cmd = {
            'cmd': 'mirror_skin_weights',
            'mesh': mesh,
            'auto_assign_labels': auto_assign_labels,
            'left_side_label': left_side_label,
            'right_side_label': right_side_label,
            'show_options': show_options
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def copy_skin_weights(
            self, source_mesh=None, target_mesh=None, auto_assign_labels=True, left_side_label='*_l_*',
            right_side_label='*_r_*', show_options=False):
        cmd = {
            'cmd': 'copy_skin_weights',
            'source_mesh': source_mesh,
            'target_mesh': target_mesh,
            'auto_assign_labels': auto_assign_labels,
            'left_side_label': left_side_label,
            'right_side_label': right_side_label,
            'show_options': show_options
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def prune_skin_weights(self, mesh=None, show_options=False):
        cmd = {
            'cmd': 'prune_skin_weights',
            'mesh': mesh,
            'show_options': show_options
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def transfer_skin_uvs(
            self, source_mesh=None, target_mesh=None, auto_assign_labels=True, left_side_label='*_l_*',
            right_side_label='*_r_*'):
        cmd = {
            'cmd': 'transfer_skin_uvs',
            'source_mesh': source_mesh,
            'target_mesh': target_mesh,
            'auto_assign_labels': auto_assign_labels,
            'left_side_label': left_side_label,
            'right_side_label': right_side_label
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def clean_skinned_mesh(self, mesh=None, auto_assign_labels=True, left_side_label='*_l_*', right_side_label='*_r_*'):
        cmd = {
            'cmd': 'clean_skinned_mesh',
            'mesh': mesh,
            'auto_assign_labels': auto_assign_labels,
            'left_side_label': left_side_label,
            'right_side_label': right_side_label
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def combine_skinned_meshes(self, meshes=None):
        cmd = {
            'cmd': 'combine_skinned_meshes',
            'meshes': meshes
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['result']

    def extract_skinned_selected_faces(
            self, components=None, auto_assign_labels=True, left_side_label='*_l_*', right_side_label='*_r_*'):
        cmd = {
            'cmd': 'extract_skinned_selected_faces',
            'components': components,
            'auto_assign_labels': auto_assign_labels,
            'left_side_label': left_side_label,
            'right_side_label': right_side_label
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['result']

    def remove_unused_influences(self, mesh=None):
        cmd = {
            'cmd': 'remove_unused_influences',
            'mesh': mesh
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def restore_bind_pose(self, mesh=None):
        cmd = {
            'cmd': 'restore_bind_pose',
            'mesh': mesh
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def remove_bind_poses(self):
        cmd = {
            'cmd': 'remove_bind_poses'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def weights_hammer(self, vertices_to_hammer=None):
        cmd = {
            'cmd': 'weights_hammer',
            'vertices_to_hammer': vertices_to_hammer
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def load_plugins(self, do_reload=True):
        cmd = {
            'cmd': 'load_plugins',
            'do_reload': do_reload
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def average_vertex_weights(self, components=None, use_distance=True, curve_weight_points=None):
        cmd = {
            'cmd': 'average_vertex_weights',
            'components': components,
            'use_distance': use_distance,
            'curve_weight_points': curve_weight_points
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def move_skin_weights(self):
        cmd = {
            'cmd': 'move_skin_weights'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def swap_skin_weights(self):
        cmd = {
            'cmd': 'swap_skin_weights'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def select_influences(self, mesh_node=None):
        cmd = {
            'cmd': 'select_influences',
            'mesh_node': mesh_node

        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def select_influence_components(self, influence_joints=None, mesh_node=None):
        cmd = {
            'cmd': 'select_influence_components',
            'influence_joints': influence_joints,
            'mesh_node': mesh_node
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def delete_influences(self, mesh_nodes=None, influences_to_remove=None, fast_delete=True):
        cmd = {
            'cmd': 'delete_influences',
            'mesh_nodes': mesh_nodes,
            'influences_to_remove': influences_to_remove,
            'fast_delete': fast_delete
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']
