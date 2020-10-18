#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains rig toolbox server implementation for Maya
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os

import tpDcc as tp
from tpDcc.core import server
from tpDcc.libs.python import path as path_utils
from tpDcc.dccs.maya.core import helpers, joint as joint_utils, skin as skin_utils


class RigToolboxServer(server.DccServer, object):
    PORT = 19344

    def _process_command(self, command_name, data_dict, reply_dict):
        if command_name == 'smooth_bind_skin':
            self.smooth_bind_skin(data_dict, reply_dict)
        elif command_name == 'rigid_bind_skin':
            self.rigid_bind_skin(data_dict, reply_dict)
        elif command_name == 'detach_bind_skin':
            self.detach_bind_skin(data_dict, reply_dict)
        elif command_name == 'open_paint_skin_weights_tool':
            self.open_paint_skin_weights_tool(data_dict, reply_dict)
        elif command_name == 'check_joints_labels':
            self.check_joints_labels(data_dict, reply_dict)
        elif command_name == 'mirror_skin_weights':
            self.mirror_skin_weights(data_dict, reply_dict)
        elif command_name == 'copy_skin_weights':
            self.copy_skin_weights(data_dict, reply_dict)
        elif command_name == 'prune_skin_weights':
            self.prune_skin_weights(data_dict, reply_dict)
        elif command_name == 'transfer_skin_uvs':
            self.transfer_skin_uvs(data_dict, reply_dict)
        elif command_name == 'clean_skinned_mesh':
            self.clean_skinned_mesh(data_dict, reply_dict)
        elif command_name == 'combine_skinned_meshes':
            self.combine_skinned_meshes(data_dict, reply_dict)
        elif command_name == 'extract_skinned_selected_faces':
            self.extract_skinned_selected_faces(data_dict, reply_dict)
        elif command_name == 'remove_unused_influences':
            self.remove_unused_influences(data_dict, reply_dict)
        elif command_name == 'restore_bind_pose':
            self.restore_bind_pose(data_dict, reply_dict)
        elif command_name == 'remove_bind_poses':
            self.remove_bind_poses(data_dict, reply_dict)
        elif command_name == 'weights_hammer':
            self.weights_hammer(data_dict, reply_dict)
        elif command_name == 'load_plugins':
            self.load_plugins(data_dict, reply_dict)
        elif command_name == 'average_vertex_weights':
            self.average_vertex_weights(data_dict, reply_dict)
        elif command_name == 'move_skin_weights':
            self.move_skin_weights(data_dict, reply_dict)
        elif command_name == 'swap_skin_weights':
            self.swap_skin_weights(data_dict, reply_dict)
        elif command_name == 'select_influences':
            self.select_influences(data_dict, reply_dict)
        elif command_name == 'select_influence_components':
            self.select_influence_components(data_dict, reply_dict)
        elif command_name == 'delete_influences':
            self.delete_influences(data_dict, reply_dict)
        else:
            super(RigToolboxServer, self)._process_command(command_name, data_dict, reply_dict)

    def smooth_bind_skin(self, data, reply):

        geo_node = data['geo_node']
        show_options = data['show_options']

        success = skin_utils.apply_smooth_bind(geo=geo_node, show_options=show_options)

        reply['success'] = success

    def rigid_bind_skin(self, data, reply):

        geo_node = data['geo_node']
        show_options = data['show_options']

        success = skin_utils.apply_rigid_skin(geo=geo_node, show_options=show_options)

        reply['success'] = success

    def detach_bind_skin(self, data, reply):

        show_options = data['show_options']

        success = skin_utils.detach_bind_skin(show_options=show_options)

        reply['success'] = success

    def open_paint_skin_weights_tool(self, data, reply):

        show_options = data['show_options']

        success = skin_utils.open_pain_skin_weights_tool(show_options=show_options)

        reply['success'] = success

    def check_joints_labels(self, data, reply):

        joints = data['joints']

        result = joint_utils.check_joint_labels(joints=joints)

        reply['result'] = result
        reply['success'] = True

    def mirror_skin_weights(self, data, reply):

        mesh = data['mesh']
        auto_assign_labels = data['auto_assign_labels']
        left_side_label = data['left_side_label']
        right_side_label = data['right_side_label']
        show_options = data['show_options']

        success = skin_utils.mirror_skin_weights(
            mesh=mesh, auto_assign_labels=auto_assign_labels, left_side_label=left_side_label,
            right_side_label=right_side_label, show_options=show_options)

        reply['success'] = success

    def copy_skin_weights(self, data, reply):

        source_mesh = data['source_mesh']
        target_mesh = data['target_mesh']
        auto_assign_labels = data['auto_assign_labels']
        left_side_label = data['left_side_label']
        right_side_label = data['right_side_label']
        show_options = data['show_options']

        success = skin_utils.copy_skin_weights(
            source_mesh=source_mesh, target_mesh=target_mesh, auto_assign_labels=auto_assign_labels,
            left_side_label=left_side_label, right_side_label=right_side_label, show_options=show_options)

        reply['success'] = success

    def prune_skin_weights(self, data, reply):
        show_options = data['show_options']
        mesh = data['mesh']

        success = skin_utils.prune_skin_weights(geo=mesh, show_options=show_options)

        reply['success'] = success

    def transfer_skin_uvs(self, data, reply):

        source_mesh = data['source_mesh']
        target_mesh = data['target_mesh']
        auto_assign_labels = data['auto_assign_labels']
        left_side_label = data['left_side_label']
        right_side_label = data['right_side_label']

        success = skin_utils.transfer_uvs_to_skinned_geometry(
            source_mesh=source_mesh, target_mesh=target_mesh, auto_assign_labels=auto_assign_labels,
            left_side_label=left_side_label, right_side_label=right_side_label)

        reply['success'] = success

    def clean_skinned_mesh(self, data, reply):
        mesh = data['mesh']
        auto_assign_labels = data['auto_assign_labels']
        left_side_label = data['left_side_label']
        right_side_label = data['right_side_label']

        success = skin_utils.freeze_skinned_mesh(
            mesh, auto_assign_labels=auto_assign_labels, left_side_label=left_side_label,
            right_side_label=right_side_label)

        reply['success'] = success

    def combine_skinned_meshes(self, data, reply):
        meshes = data['meshes']

        combined_mesh = skin_utils.combine_skinned_meshes(meshes)

        reply['result'] = combined_mesh
        reply['success'] = bool(combined_mesh)

    def extract_skinned_selected_faces(self, data, reply):
        components = data['components']
        auto_assign_labels = data['auto_assign_labels']
        left_side_label = data['left_side_label']
        right_side_label = data['right_side_label']

        extract_mesh = skin_utils.extract_skinned_selected_components(
            components, auto_assign_labels=auto_assign_labels, left_side_label=left_side_label,
            right_side_label=right_side_label)

        reply['result'] = extract_mesh

    def remove_unused_influences(self, data, reply):
        mesh = data['mesh']

        skin_utils.delete_unused_influences(mesh)

        reply['success'] = True

    def restore_bind_pose(self, data, reply):
        mesh = data['mesh']

        success = skin_utils.restore_to_bind_pose(mesh)

        reply['success'] = success

    def remove_bind_poses(self, data, reply):
        success = skin_utils.remove_all_bind_poses_in_scene()

        reply['success'] = success

    def weights_hammer(self, data, reply):

        vertices_to_hammer = data['vertices_to_hammer']

        success = skin_utils.hammer_vertices(vertices_to_hammer)

        reply['success'] = success

    def load_plugins(self, data, reply):

        do_reload = data['do_reload']

        plugins_path = path_utils.clean_path(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'plugins'))
        if not os.path.isdir(plugins_path):
            reply['msg'] = 'Impossible to load tpRigToolkit-tools-rigtoolbox Maya plugins because plugin ' \
                           'folder was not found: "{}"'.format(plugins_path)
            reply['success'] = False
            return

        # Update Maya Plugin paths
        maya_plugin_path = os.getenv('MAYA_PLUG_IN_PATH', None)
        if not maya_plugin_path:
            os.environ['MAYA_PLUG_IN_PATH'] = plugins_path
        else:
            path_already_added = False
            current_plugin_paths = os.environ['MAYA_PLUG_IN_PATH'].split(os.pathsep)
            for current_plugin_path in current_plugin_paths:
                if path_utils.clean_path(current_plugin_path) == plugins_path:
                    path_already_added = True
                    break
            if not path_already_added:
                os.environ['MAYA_PLUG_IN_PATH'] = '{}{}{}'.format(
                    os.environ['MAYA_PLUG_IN_PATH'], os.pathsep, plugins_path)

        # Load plugins
        for plugin_file in os.listdir(plugins_path):
            if not plugin_file:
                continue
            plugin_ext = os.path.splitext(plugin_file)[-1]
            if not plugin_ext == '.py':
                continue
            plugin_path = path_utils.clean_path(os.path.join(plugins_path, plugin_file))
            if do_reload:
                if helpers.is_plugin_loaded(plugin_path):
                    helpers.unload_plugin(plugin_path)
            helpers.load_plugin(plugin_path)

        reply['success'] = True

    def average_vertex_weights(self, data, reply):
        components = data['components'] or tp.Dcc.selected_nodes_in_order(flatten=True)
        use_distance = data['use_distance']

        skin_utils.average_vertices_weights(components, use_distance=use_distance)

        reply['success'] = True

    def move_skin_weights(self, data, reply):

        selection = tp.Dcc.selected_nodes()
        if len(selection) < 3:
            reply['msg'] = 'Select source joint, target joint (joint that will receive skin weights) ' \
                           'and geometry that has the skin cluster attached'
            reply['success'] = False
            return

        source_joint = selection[0]
        target_joint = selection[1]
        mesh = selection[2]

        success = skin_utils.move_skin_weights(source_joint, target_joint, mesh)

        reply['success'] = success

    def swap_skin_weights(self, data, reply):

        selection = tp.Dcc.selected_nodes()
        if len(selection) < 3:
            reply['msg'] = 'Select source joint, target joint (joint that will receive skin weights) ' \
                           'and geometry that has the skin cluster attached'
            reply['success'] = False
            return

        source_joint = selection[0]
        target_joint = selection[1]
        mesh = selection[2]

        skin_utils.swap_skin_weights(source_joint, target_joint, mesh)

        reply['success'] = True

    def select_influences(self, data, reply):
        mesh_node = data['mesh_node']
        if not mesh_node:
            selected_transforms = tp.Dcc.selected_nodes_of_type(node_type='transform')
            mesh_node = selected_transforms[0] if selected_transforms else None
        if not mesh_node:
            reply['msg'] = 'No mesh selected to retrieve influences of'
            reply['success'] = False
            return

        success = skin_utils.select_influencing_joints(mesh_node)

        reply['success'] = success

    def select_influence_components(self, data, reply):

        influence_joints = data['influence_joints']
        mesh_node = data['mesh_node']

        success = skin_utils.select_influence_vertices(joint_nodes=influence_joints, mesh_name=mesh_node)

        reply['success'] = success

    def delete_influences(self, data, reply):

        mesh_nodes = data['mesh_nodes']
        influences_to_remove = data['influences_to_remove']
        fast_delete = data['fast_delete']

        success = skin_utils.delete_influences(
            skinned_objects=mesh_nodes, influences_to_remove=influences_to_remove, fast=fast_delete)

        reply['success'] = success
