#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget with geometry functionality
"""

from Qt.QtCore import *
from Qt.QtWidgets import *

import tpDcc as tp
from tpDcc.libs.qt.core import qtutils
from tpDcc.libs.qt.widgets import layouts, accordion

from tpRigToolkit.tools.rigtoolbox.widgets import base

LOGGER = tp.LogsMgr().get_logger('tpRigToolkit-tools-rigtoolbox')


class GeneralWidget(base.BaseRigToolBoxWidget, object):
    def __init__(self, client, parent=None):
        super(GeneralWidget, self).__init__(title='General', parent=parent)

        self._model = GeneralWidgetModel()
        self._controller = GeneralWidgetController(model=self._model, client=client)

        self._accordion = accordion.AccordionWidget()
        self.main_layout.addWidget(self._accordion)

        self._accordion.add_item('General', self._setup_general_tools())
        self._accordion.add_item('Transforms', self._setup_transforms_tools())
        self._accordion.add_item('Geometry', self._setup_geometry_tools())

    def _setup_general_tools(self):
        general_widget = QWidget()
        self._general_layout = layouts.FlowLayout()
        self._general_layout.setAlignment(Qt.AlignLeft)
        general_widget.setLayout(self._general_layout)

        delete_history_icon = tp.ResourcesMgr().icon('delete_history')
        freeze_transforms_icon = tp.ResourcesMgr().icon('freeze_transforms')
        move_pivot_icon = tp.ResourcesMgr().icon('center_pivot')
        lock_icon = tp.ResourcesMgr().icon('lock')
        unlock_icon = tp.ResourcesMgr().icon('unlock')

        delete_history_btn = self._create_button('Delete History', delete_history_icon, self._controller.delete_history)
        freeze_transforms_btn = self._create_button(
            'Freeze Transforms', freeze_transforms_icon, self._controller.freeze_transforms)
        move_pivot_to_zero_btn = self._create_button(
            'Move Pivot to Zero', move_pivot_icon, self._controller.pivot_to_zero)

        lock_btn = self._create_button('Lock Transforms', lock_icon, self._controller.lock_all_transforms)
        lock_btn.setPopupMode(QToolButton.MenuButtonPopup)
        lock_menu = QMenu(lock_btn)
        lock_btn.setMenu(lock_menu)
        lock_translation_action = QAction(lock_icon, 'Lock Translation', lock_menu)
        lock_rotation_action = QAction(lock_icon, 'Lock Rotation', lock_menu)
        lock_scale_action = QAction(lock_icon, 'Lock Scale', lock_menu)
        lock_menu.addAction(lock_translation_action)
        lock_menu.addAction(lock_rotation_action)
        lock_menu.addAction(lock_scale_action)
        lock_translation_action.triggered.connect(self._controller.lock_translation)
        lock_rotation_action.triggered.connect(self._controller.lock_rotation)
        lock_scale_action.triggered.connect(self._controller.lock_scale)

        unlock_btn = self._create_button('Unlock Transforms', unlock_icon, self._controller.unlock_all_transforms)
        unlock_btn.setPopupMode(QToolButton.MenuButtonPopup)
        unlock_menu = QMenu(unlock_btn)
        unlock_btn.setMenu(unlock_menu)
        unlock_translation_action = QAction(unlock_icon, 'Unlock Translation', unlock_menu)
        unlock_rotation_action = QAction(unlock_icon, 'Unlock Rotation', unlock_menu)
        unlock_scale_action = QAction(unlock_icon, 'Unlock Scale', unlock_menu)
        unlock_menu.addAction(unlock_translation_action)
        unlock_menu.addAction(unlock_rotation_action)
        unlock_menu.addAction(unlock_scale_action)
        unlock_translation_action.triggered.connect(self._controller.unlock_translation)
        unlock_rotation_action.triggered.connect(self._controller.unlock_rotation)
        unlock_scale_action.triggered.connect(self._controller.unlock_scale)

        lock_vis_btn = self._create_button('Lock Visibility', lock_icon, self._controller.lock_visibility)
        unlock_vis_btn = self._create_button('Unlock Visibility', unlock_icon, self._controller.unlock_visibility)

        self._general_layout.addWidget(delete_history_btn)
        self._general_layout.addWidget(freeze_transforms_btn)
        self._general_layout.addWidget(move_pivot_to_zero_btn)
        self._general_layout.addWidget(lock_btn)
        self._general_layout.addWidget(unlock_btn)
        self._general_layout.addWidget(lock_vis_btn)
        self._general_layout.addWidget(unlock_vis_btn)

        return general_widget

    # TODO: Add functions to freeze specific transforms (translate, rotate, scale)
    def _setup_transforms_tools(self):
        transforms_widget = QWidget()
        self._transforms_layout = layouts.FlowLayout()
        self._transforms_layout.setAlignment(Qt.AlignLeft)
        transforms_widget.setLayout(self._transforms_layout)

        match_transform_icon = tp.ResourcesMgr().icon('match_transform')
        match_translation_icon = tp.ResourcesMgr().icon('match_translation')
        match_rotation_icon = tp.ResourcesMgr().icon('match_rotation')
        match_scale_icon = tp.ResourcesMgr().icon('match_scale')

        match_transform_btn = self._create_button(
            'Match Transform', match_transform_icon, self._controller.match_transform)
        match_translation_btn = self._create_button(
            'Match Translation', match_translation_icon, self._controller.match_translation)
        math_rotation_btn = self._create_button(
            'Match Rotation', match_rotation_icon, self._controller.match_rotation)
        match_scale_btn = self._create_button('Match Scale', match_scale_icon, self._controller.match_scale)

        self._transforms_layout.addWidget(match_transform_btn)
        self._transforms_layout.addWidget(match_translation_btn)
        self._transforms_layout.addWidget(math_rotation_btn)
        self._transforms_layout.addWidget(match_scale_btn)

        return transforms_widget

    def _setup_geometry_tools(self):
        geometry_widget = QWidget()
        self._geometry_layout = layouts.FlowLayout()
        self._geometry_layout.setAlignment(Qt.AlignLeft)
        geometry_widget.setLayout(self._geometry_layout)

        combine_meshes_icon = tp.ResourcesMgr().icon('combine')
        mirror_meshes_icon = tp.ResourcesMgr().icon('mirror')
        symmetry_icon = tp.ResourcesMgr().icon('symmetry')

        combine_meshes_btn = self._create_button(
            'Combine Meshes', combine_meshes_icon, self._controller.combine_meshes)
        mirror_meshes_btn = self._create_button(
            'Mirror Meshes', mirror_meshes_icon, self._controller.mirror_meshes)
        symmetry_btn = self._create_button(
            'Symmetry Tool', symmetry_icon, self._controller.open_symmetry_tool
        )

        self._geometry_layout.addWidget(combine_meshes_btn)
        self._geometry_layout.addWidget(mirror_meshes_btn)
        self._geometry_layout.addWidget(symmetry_btn)

        return geometry_widget


class GeneralWidgetModel(QObject, object):
    def __init__(self):
        super(GeneralWidgetModel, self).__init__()


class GeneralWidgetController(object):

    def __init__(self, model, client):
        super(GeneralWidgetController, self).__init__()

        self._model = model
        self._client = client

    @property
    def model(self):
        return self._model

    @property
    def client(self):
        return self._client

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def delete_history():
        """
        Delete history of selected transforms
        """

        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        for obj in selected:
            tp.Dcc.delete_history(obj)

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def freeze_transforms():
        """
        Freeze selected transforms
        """

        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        for obj in selected:
            tp.Dcc.freeze_transforms(obj)

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def pivot_to_zero():
        """
        Moves selected nodes pivots to zero (0, 0, 0 in the world)
        """

        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        for obj in selected:
            tp.Dcc.move_pivot_to_zero(obj)

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def combine_meshes():
        """
        Combines selected meshes
        """

        new_name = None
        if qtutils.is_shift_modifier():
            new_name = qtutils.get_string_input('Combine Mesh Name', title='Combine Mesh')

        meshes_to_combine = tp.Dcc.selected_nodes()
        if not meshes_to_combine:
            return

        parent_node = None
        node_parents = list(set([tp.Dcc.node_parent(mesh) for mesh in meshes_to_combine]))
        if all(parent == node_parents[0] for parent in node_parents):
            parent_node = node_parents[0]

        combined_mesh = tp.Dcc.combine_meshes(construction_history=False)

        if combined_mesh:
            if new_name:
                combined_mesh = tp.Dcc.rename_node(combined_mesh, new_name)
            if parent_node:
                tp.Dcc.set_parent(combined_mesh, parent_node)

        return combined_mesh

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def mirror_meshes():
        """
        Mirror selected meshes
        """

        if not tp.is_maya():
            return

        import tpDcc.dccs.maya as maya
        from tpDcc.dccs.maya.core import transform as maya_transform

        geos = maya.cmds.ls(sl=True, type='transform')
        for geo in geos:
            parent_node = tp.Dcc.node_parent(geo)
            mirror_geo_name = maya_transform.find_transform_right_side(geo, check_if_exists=False)
            mirror_geo = maya.cmds.duplicate(geo, n=mirror_geo_name or None)
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

    @staticmethod
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def open_symmetry_tool():
        tp.ToolsMgr().launch_tool_by_id('tpRigToolkit-tools-symmesh')

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def lock_all_transforms():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected:
            return False

        for node in selected:
            tp.Dcc.lock_translate_attributes(node)
            tp.Dcc.lock_rotate_attributes(node)
            tp.Dcc.lock_scale_attributes(node)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def lock_translation():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected:
            return False

        for node in selected:
            tp.Dcc.lock_translate_attributes(node)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeometryWidgetController')
    def lock_rotation():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected:
            return False

        for node in selected:
            tp.Dcc.lock_rotate_attributes(node)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def lock_scale():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected:
            return False

        for node in selected:
            tp.Dcc.lock_scale_attributes(node)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeometryWidgetController')
    def lock_visibility():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected:
            return False

        for node in selected:
            tp.Dcc.lock_visibility_attribute(node)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def unlock_all_transforms():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected:
            return False

        for node in selected:
            tp.Dcc.unlock_translate_attributes(node)
            tp.Dcc.unlock_rotate_attributes(node)
            tp.Dcc.unlock_scale_attributes(node)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeometryWidgetController')
    def unlock_translation():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected:
            return False

        for node in selected:
            tp.Dcc.unlock_translate_attributes(node)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def unlock_rotation():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected:
            return False

        for node in selected:
            tp.Dcc.unlock_rotate_attributes(node)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def unlock_scale():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected:
            return False

        for node in selected:
            tp.Dcc.unlock_scale_attributes(node)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeometryWidgetController')
    def unlock_visibility():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected:
            return False

        for node in selected:
            tp.Dcc.unlock_visibility_attribute(node)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def match_transform():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected or len(selected) < 2:
            return False

        sources = selected[:-1]
        target = selected[-1]

        for source in sources:
            tp.Dcc.match_transform(target, source)
            if tp.Dcc.node_type(source) == 'joint':
                for axis in 'XYZ':
                    joint_orient_attr = 'jointOrient{}'.format(axis)
                    joint_rotation_attr = 'rotate{}'.format(axis)
                    tp.Dcc.set_attribute_value(source, joint_orient_attr, 0.0)
                    joint_rotation = tp.Dcc.get_attribute_value(source, joint_rotation_attr)
                    tp.Dcc.set_attribute_value(source, joint_orient_attr, joint_rotation)
                    tp.Dcc.set_attribute_value(source, joint_rotation_attr, 0.0)

        tp.Dcc.select_node(sources)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def match_translation():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected or len(selected) < 2:
            return False

        sources = selected[:-1]
        target = selected[-1]

        for source in sources:
            tp.Dcc.match_translation(target, source)

        tp.Dcc.select_node(sources)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def match_rotation():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected or len(selected) < 2:
            return False

        sources = selected[:-1]
        target = selected[-1]

        for source in sources:
            tp.Dcc.match_rotation(target, source)
            if tp.Dcc.node_type(source) == 'joint':
                for axis in 'XYZ':
                    joint_orient_attr = 'jointOrient{}'.format(axis)
                    joint_rotation_attr = 'rotate{}'.format(axis)
                    tp.Dcc.set_attribute_value(source, joint_orient_attr, 0.0)
                    joint_rotation = tp.Dcc.get_attribute_value(source, joint_rotation_attr)
                    tp.Dcc.set_attribute_value(source, joint_orient_attr, joint_rotation)
                    tp.Dcc.set_attribute_value(source, joint_rotation_attr, 0.0)

        tp.Dcc.select_node(sources)

        return True

    @staticmethod
    @tp.Dcc.undo_decorator()
    @tp.Dcc.repeat_last_decorator(__name__ + '.GeneralWidgetController')
    def match_scale():
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        if not selected or len(selected) < 2:
            return False

        sources = selected[:-1]
        target = selected[-1]

        for source in sources:
            tp.Dcc.match_scale(target, source)

        tp.Dcc.select_node(sources)

        return True
