#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget for rig skinning functionality
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import *
from Qt.QtWidgets import *

import tpDcc as tp
from tpDcc.libs.qt.core import qtutils
from tpDcc.libs.qt.widgets import layouts, accordion

from tpRigToolkit.tools.rigtoolbox.widgets import base
from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import labelsdialog

LOGGER = tp.LogsMgr().get_logger('tpRigToolkit-tools-rigtoolbox')


class SkinningWidget(base.BaseRigToolBoxWidget, object):
    def __init__(self, client, parent=None):
        super(SkinningWidget, self).__init__(title='Skinning', parent=parent)

        self._model = SkinningWidgetModel()
        self._controller = SkinningWidgetController(model=self._model, client=client)

        self._accordion = accordion.AccordionWidget()
        self.main_layout.addWidget(self._accordion)

        self._accordion.add_item('Create / Bind', self._setup_create_tools())
        self._accordion.add_item('Edit', self._setup_edit_tools())

        self.refresh()

    @property
    def model(self):
        return self._model

    @property
    def controller(self):
        return self._controller

    def refresh(self):
        self._mirror_auto_assign_joints_labels_action.setChecked(self._model.mirror_auto_assign_labels)
        self._copy_skin_weights_auto_assign_joints_labels_action.setChecked(
            self._model.copy_skin_weights_auto_assign_labels)
        self._clean_skin_mesh_auto_assign_joints_labels_action.setChecked(
            self._model.clean_skin_mesh_auto_assign_labels)
        self._extract_skin_faces_auto_assign_joints_labels_action.setChecked(
            self._model.extract_skin_faces_auto_assign_labels)
        self._distance_average_action.setChecked(self._model.use_distance_average)
        self._fast_delete_action.setChecked(self._model.fast_delete)

    def _setup_create_tools(self):
        create_widget = QWidget()
        self._create_layout = layouts.FlowLayout()
        self._create_layout.setAlignment(Qt.AlignLeft)
        create_widget.setLayout(self._create_layout)

        smooth_skin_icon = tp.ResourcesMgr().icon('smooth_skin')
        rigid_skin_icon = tp.ResourcesMgr().icon('rigid_skin')
        detach_skin_icon = tp.ResourcesMgr().icon('detach_skin')
        paint_skin_weights_icon = tp.ResourcesMgr().icon('paint_skin_weights')
        mirror_skin_weights_icon = tp.ResourcesMgr().icon('mirror_skin_weights')
        copy_skin_weights_icon = tp.ResourcesMgr().icon('copy_skin_weights')
        prune_skin_weights_icon = tp.ResourcesMgr().icon('prune_skin_weights')
        transfer_skin_uvs_icon = tp.ResourcesMgr().icon('transfer_skin_uvs')
        clean_skinned_mesh_icon = tp.ResourcesMgr().icon('clean_skinned_mesh')
        combine_skinned_meshes_icon = tp.ResourcesMgr().icon('combine_skinned_meshes')
        extract_skinned_faces_icon = tp.ResourcesMgr().icon('extract_skinned_faces')
        remove_unused_influences_icon = tp.ResourcesMgr().icon('remove_unused_influences')
        restore_bind_pose_icon = tp.ResourcesMgr().icon('restore_bind_pose')
        remove_bind_poses_icon = tp.ResourcesMgr().icon('remove_bind_poses')
        weights_hammer_icon = tp.ResourcesMgr().icon('weights_hammer')

        self._mirror_auto_assign_joints_labels_action = QAction('Auto Assign Labels', self)
        self._mirror_auto_assign_joints_labels_action.setCheckable(True)
        self._copy_skin_weights_auto_assign_joints_labels_action = QAction('Auto Assign Labels', self)
        self._copy_skin_weights_auto_assign_joints_labels_action.setCheckable(True)
        self._transfer_skin_uvs_auto_assign_joints_labels_action = QAction('Auto Assign Labels', self)
        self._transfer_skin_uvs_auto_assign_joints_labels_action.setCheckable(True)
        self._clean_skin_mesh_auto_assign_joints_labels_action = QAction('Auto Assign Labels', self)
        self._clean_skin_mesh_auto_assign_joints_labels_action.setCheckable(True)
        self._extract_skin_faces_auto_assign_joints_labels_action = QAction('Auto Assign Labels', self)
        self._extract_skin_faces_auto_assign_joints_labels_action.setCheckable(True)

        self._smooth_bind_btn = self._create_button(
            '', smooth_skin_icon, self._controller.smooth_bind_skin, description='Smooth Bind Skin')
        self._rigid_bind_btn = self._create_button(
            '', rigid_skin_icon, self._controller.rigid_bind_skin, description='Rigid Bind Skin')
        detach_widget, self._detach_skin_btn, self._detack_skin_options_btn = self._create_button(
            '', detach_skin_icon, self._controller.detach_skin, description='Detach Skin',
            has_settings=True, settings_fn=self._controller.detach_skin_options)
        self._paint_skin_weights_btn = self._create_button(
            '', paint_skin_weights_icon, self._controller.open_paint_skin_weights_tool,
            description='Pain Skin Weights Tool')
        self._mirror_skin_weights_btn = self._create_button(
            '', mirror_skin_weights_icon, self._controller.mirror_skin_weights, description='Mirror Skin Weights',
            actions=[self._mirror_auto_assign_joints_labels_action])
        self._copy_skin_weights_btn = self._create_button(
            '', copy_skin_weights_icon, self._controller.copy_skin_weights, description='Copy Skin Weights',
            actions=[self._copy_skin_weights_auto_assign_joints_labels_action])
        self._prune_skin_weights_btn = self._create_button(
            '', prune_skin_weights_icon, self._controller.prune_skin_weights, description='Prune Skin Weights')
        self._transfer_skin_uvs_btn = self._create_button(
            '', transfer_skin_uvs_icon, self._controller.transfer_skin_uvs, description='Transfer Skin UVs',
            actions=[self._transfer_skin_uvs_auto_assign_joints_labels_action])
        self._clean_skinned_mesh_btn = self._create_button(
            '', clean_skinned_mesh_icon, self._controller.clean_skinned_mesh, description='Clean Skinned Mesh',
            actions=[self._clean_skin_mesh_auto_assign_joints_labels_action])
        self._combine_skinned_meshes_btn = self._create_button(
            '', combine_skinned_meshes_icon, self._controller.combine_skinned_meshes,
            description='Combine Skinned Meshes')
        self._extract_skinned_faces_btn = self._create_button(
            '', extract_skinned_faces_icon, self._controller.extract_skinned_faces,
            description='Extract Skinned Faces', actions=[self._extract_skin_faces_auto_assign_joints_labels_action])
        self._remove_unused_influences_btn = self._create_button(
            '', remove_unused_influences_icon, self._controller.remove_unused_influences,
            description='Remove Unused Influences')
        self._restore_bind_pose_btn = self._create_button(
            '', restore_bind_pose_icon, self._controller.restore_bind_pose, description='Restore Bind Pose')
        self._remove_bind_poses_btn = self._create_button(
            '', remove_bind_poses_icon, self._controller.remove_bind_poses, description='Remove Bind Poses')
        self._weights_hammer_btn = self._create_button(
            '', weights_hammer_icon, self._controller.weights_hammer, description='Weights Hammer')

        self._create_layout.addWidget(self._smooth_bind_btn)
        self._create_layout.addWidget(self._rigid_bind_btn)
        self._create_layout.addWidget(detach_widget)
        self._create_layout.addWidget(self._paint_skin_weights_btn)
        self._create_layout.addWidget(self._mirror_skin_weights_btn)
        self._create_layout.addWidget(self._copy_skin_weights_btn)
        self._create_layout.addWidget(self._prune_skin_weights_btn)
        self._create_layout.addWidget(self._transfer_skin_uvs_btn)
        self._create_layout.addWidget(self._clean_skinned_mesh_btn)
        self._create_layout.addWidget(self._combine_skinned_meshes_btn)
        self._create_layout.addWidget(self._extract_skinned_faces_btn)
        self._create_layout.addWidget(self._remove_unused_influences_btn)
        self._create_layout.addWidget(self._restore_bind_pose_btn)
        self._create_layout.addWidget(self._remove_bind_poses_btn)
        self._create_layout.addWidget(self._weights_hammer_btn)

        self._mirror_auto_assign_joints_labels_action.toggled.connect(self._controller.set_mirror_auto_assign_labels)
        self._copy_skin_weights_auto_assign_joints_labels_action.toggled.connect(
            self._controller.set_copy_skin_weights_auto_assign_labels)
        self._transfer_skin_uvs_auto_assign_joints_labels_action.toggled.connect(
            self._controller.set_transfer_skin_uvs_auto_assign_labels)
        self._clean_skin_mesh_auto_assign_joints_labels_action.toggled.connect(
            self._controller.set_clean_skin_mesh_auto_assign_labels)
        self._extract_skin_faces_auto_assign_joints_labels_action.toggled.connect(
            self._controller.set_extract_skin_faces_auto_assign_labels)

        self._model.mirrorAutoAssignLabelsChanged.connect(self._mirror_auto_assign_joints_labels_action.setChecked)
        self._model.copySkinWeightsAutoAssignLabelsChanged.connect(
            self._copy_skin_weights_auto_assign_joints_labels_action.setChecked)
        self._model.transferSkinUVsAutoAssignLabelsChanged.connect(
            self._transfer_skin_uvs_auto_assign_joints_labels_action.setChecked)
        self._model.cleanSkinMeshAutoAssignLabelsChanged.connect(
            self._clean_skin_mesh_auto_assign_joints_labels_action.setChecked)
        self._model.extractSkinFacesAutoAssignLabelsChanged.connect(
            self._extract_skin_faces_auto_assign_joints_labels_action.setChecked)

        return create_widget

    def _setup_edit_tools(self):
        edit_widget = QWidget()
        self._edit_layout = layouts.FlowLayout()
        self._edit_layout.setAlignment(Qt.AlignLeft)
        edit_widget.setLayout(self._edit_layout)

        self._distance_average_action = QAction('On Distance', self)
        self._distance_average_action.setCheckable(True)
        self._fast_delete_action = QAction('Fast Delete', self)
        self._fast_delete_action.setCheckable(True)

        self._average_weights_btn = self._create_button(
            'Average Weights', None, self._controller.average_vertex_weights, actions=[self._distance_average_action])
        self._move_skin_weights_btn = self._create_button('Move Skin Weights', None, self._controller.move_skin_weights)
        self._swap_skin_weights_btn = self._create_button('Swap Skin Weights', None, self._controller.swap_skin_weights)
        self._select_influences_btn = self._create_button('Select Influences', None, self._controller.select_influences)
        self._select_influence_components_btn = self._create_button(
            'Select Influence Components', None, self._controller.select_influence_components)
        self._delete_influences_btn = self._create_button(
            'Delete Influence', None, self._controller.delete_influences, actions=[self._fast_delete_action])

        self._edit_layout.addWidget(self._average_weights_btn)
        self._edit_layout.addWidget(self._move_skin_weights_btn)
        self._edit_layout.addWidget(self._swap_skin_weights_btn)
        self._edit_layout.addWidget(self._select_influences_btn)
        self._edit_layout.addWidget(self._select_influence_components_btn)
        self._edit_layout.addWidget(self._delete_influences_btn)

        self._distance_average_action.toggled.connect(self._controller.set_distance_average)
        self._fast_delete_action.toggled.connect(self._controller.set_fast_delete)

        self._model.useDistanceAverageChanged.connect(self._distance_average_action.setChecked)
        self._model.fastDeleteChanged.connect(self._fast_delete_action.setChecked)

        return edit_widget


class SkinningWidgetModel(QObject, object):

    mirrorAutoAssignLabelsChanged = Signal(bool)
    copySkinWeightsAutoAssignLabelsChanged = Signal(bool)
    transferSkinUVsAutoAssignLabelsChanged = Signal(bool)
    cleanSkinMeshAutoAssignLabelsChanged = Signal(bool)
    extractSkinFacesAutoAssignLabelsChanged = Signal(bool)
    useDistanceAverageChanged = Signal(bool)
    fastDeleteChanged = Signal(bool)

    def __init__(self):
        super(SkinningWidgetModel, self).__init__()

        self._mirror_auto_assign_labels = True
        self._copy_skin_weights_auto_assign_labels = True
        self._transfer_skin_uvs_auto_assign_labels = True
        self._clean_skin_mesh_auto_assign_labels = True
        self._extract_skin_faces_auto_assign_labels = True
        self._use_distance_average = True
        self._fast_delete = True

    @property
    def mirror_auto_assign_labels(self):
        return self._mirror_auto_assign_labels

    @mirror_auto_assign_labels.setter
    def mirror_auto_assign_labels(self, flag):
        self._mirror_auto_assign_labels = bool(flag)
        self.mirrorAutoAssignLabelsChanged.emit(self._mirror_auto_assign_labels)

    @property
    def copy_skin_weights_auto_assign_labels(self):
        return self._copy_skin_weights_auto_assign_labels

    @copy_skin_weights_auto_assign_labels.setter
    def copy_skin_weights_auto_assign_labels(self, flag):
        self._copy_skin_weights_auto_assign_labels = bool(flag)
        self.copySkinWeightsAutoAssignLabelsChanged.emit(self._copy_skin_weights_auto_assign_labels)

    @property
    def transfer_uvs_auto_assign_labels(self):
        return self._transfer_skin_uvs_auto_assign_labels

    @transfer_uvs_auto_assign_labels.setter
    def transfer_uvs_auto_assign_labels(self, flag):
        self._transfer_skin_uvs_auto_assign_labels = bool(flag)
        self.transferSkinUVsAutoAssignLabelsChanged.emit(self._transfer_skin_uvs_auto_assign_labels)()

    @property
    def clean_skin_mesh_auto_assign_labels(self):
        return self._clean_skin_mesh_auto_assign_labels

    @clean_skin_mesh_auto_assign_labels.setter
    def clean_skin_mesh_auto_assign_labels(self, flag):
        self._clean_skin_mesh_auto_assign_labels = bool(flag)
        self.cleanSkinMeshAutoAssignLabelsChanged.emit(self._clean_skin_mesh_auto_assign_labels)

    @property
    def extract_skin_faces_auto_assign_labels(self):
        return self._extract_skin_faces_auto_assign_labels

    @extract_skin_faces_auto_assign_labels.setter
    def extract_skin_faces_auto_assign_labels(self, flag):
        self._extract_skin_faces_auto_assign_labels = bool(flag)
        self.extractSkinFacesAutoAssignLabelsChanged.emit(self._extract_skin_faces_auto_assign_labels)

    @property
    def use_distance_average(self):
        return self._use_distance_average

    @use_distance_average.setter
    def use_distance_average(self, flag):
        self._use_distance_average = bool(flag)
        self.useDistanceAverageChanged.emit(self._use_distance_average)

    @property
    def fast_delete(self):
        return self._fast_delete

    @fast_delete.setter
    def fast_delete(self, flag):
        self._fast_delete = bool(flag)
        self.fastDeleteChanged.emit(self._fast_delete)


class SkinningWidgetController(object):

    def __init__(self, client, model):
        super(SkinningWidgetController, self).__init__()

        self._model = model
        self._client = client

    @property
    def model(self):
        return self._model

    @property
    def client(self):
        return self._client

    def set_mirror_auto_assign_labels(self, flag):
        self._model.mirror_auto_assign_labels = flag

    def set_copy_skin_weights_auto_assign_labels(self, flag):
        self._model.copy_skin_weights_auto_assign_labels = flag

    def set_transfer_skin_uvs_auto_assign_labels(self, flag):
        self._model.transfer_skin_uvs_auto_assign_labels = flag

    def set_clean_skin_mesh_auto_assign_labels(self, flag):
        self._model.clean_skin_mesh_auto_assign_labels = flag

    def set_extract_skin_faces_auto_assign_labels(self, flag):
        self._model.extract_skin_faces_auto_assign_labels = flag

    def set_distance_average(self, flag):
        self._model.use_distance_average = flag

    def set_fast_delete(self, flag):
        self._model.fast_delete = flag

    def smooth_bind_skin(self):
        return self._client.smooth_bind_skin(show_options=True)

    def rigid_bind_skin(self):
        return self._client.rigid_bind_skin(show_options=True)

    def detach_skin(self):
        self._client.detach_bind_skin(show_options=False)

    def detach_skin_options(self):
        self._client.detach_bind_skin(show_options=True)

    def open_paint_skin_weights_tool(self):
        self._client.open_paint_skin_weights_tool(show_options=True)

    def mirror_skin_weights(self):
        auto_assign_labels = self._model.mirror_auto_assign_labels
        left_side, right_side = self._check_labels(auto_assign_labels)
        if left_side is False or right_side is False:
            LOGGER.warning('No sides specified. Aborting mirror skin weights operation ...')
            return False

        return self._client.mirror_skin_weights(
            auto_assign_labels=auto_assign_labels, left_side_label=left_side,
            right_side_label=right_side, show_options=True)

    def copy_skin_weights(self):
        auto_assign_labels = self._model.copy_skin_weights_auto_assign_labels
        left_side, right_side = self._check_labels(auto_assign_labels)
        if left_side is False or right_side is False:
            LOGGER.warning('No sides specified. Aborting copy skin weights operation ...')
            return False

        return self._client.copy_skin_weights(
            auto_assign_labels=auto_assign_labels, left_side_label=left_side,
            right_side_label=right_side, show_options=True)

    def prune_skin_weights(self):
        return self._client.prune_skin_weights(show_options=True)

    def transfer_skin_uvs(self):
        auto_assign_labels = self._model.transfer_skin_uvs_auto_assign_labels
        left_side, right_side = self._check_labels(auto_assign_labels)
        if left_side is False or right_side is False:
            LOGGER.warning('No sides specified. Aborting transfer skin uvs operation ...')
            return False

        return self._client.transfer_skin_uvs(
            auto_assign_labels=auto_assign_labels, left_side_label=left_side, right_side_label=right_side)

    def clean_skinned_mesh(self):
        auto_assign_labels = self._model.clean_skin_mesh_auto_assign_labels
        left_side, right_side = self._check_labels(auto_assign_labels)
        if left_side is False or right_side is False:
            LOGGER.warning('No sides specified. Aborting clean skinned mesh operation ...')
            return False

        return self._client.clean_skinned_mesh(
            auto_assign_labels=auto_assign_labels, left_side_label=left_side, right_side_label=right_side)

    def combine_skinned_meshes(self):
        return self._client.combine_skinned_meshes()

    def extract_skinned_faces(self):
        auto_assign_labels = self._model.extract_skin_faces_auto_assign_labels
        left_side, right_side = self._check_labels(auto_assign_labels)
        if left_side is False or right_side is False:
            LOGGER.warning('No sides specified. Aborting extract skinned faces operation ...')
            return False

        return self._client.extract_skinned_selected_faces(
            auto_assign_labels=auto_assign_labels, left_side_label=left_side, right_side_label=right_side)

    def remove_unused_influences(self):
        return self._client.remove_unused_influences()

    def restore_bind_pose(self):
        res = qtutils.show_question(None, 'Go to Bind Pose', 'Are you sure yo want to restore bind pose?')
        if res != QMessageBox.Yes:
            return False

        return self._client.restore_bind_pose()

    def remove_bind_poses(self):
        res = qtutils.show_question(
            None, 'Remove Bind Poses', 'Are you sure yo want to remove all bind poses from the current scene?')
        if res != QMessageBox.Yes:
            return False

        return self._client.remove_bind_poses()

    def weights_hammer(self):
        return self._client.weights_hammer()

    def average_vertex_weights(self):
        use_distance_average = self._model.use_distance_average

        return self._client.average_vertex_weights(use_distance=use_distance_average)

    def move_skin_weights(self):
        return self._client.move_skin_weights()

    def swap_skin_weights(self):
        return self._client.swap_skin_weights()

    def select_influences(self):
        return self._client.select_influences()

    def select_influence_components(self):
        return self._client.select_influence_components()

    def delete_influences(self):
        fast_delete = self._model.fast_delete
        return self._client.delete_influences(fast_delete=fast_delete)

    def _check_labels(self, auto_assign_labels):
        left_side = None
        right_side = None
        if auto_assign_labels:
            check_joints_labels = self._client.check_joints_labels()
            if not check_joints_labels:
                labels_dialog = labelsdialog.JointsLabelDialog()
                labels_dialog.exec_()
                left_side, right_side = labels_dialog.get_sides()
                if not left_side or not right_side:
                    return False, False

        return left_side, right_side
