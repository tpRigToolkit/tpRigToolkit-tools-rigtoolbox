#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget with joint functionality
"""

from functools import partial

from Qt.QtCore import *
from Qt.QtWidgets import *

import tpDcc as tp
from tpDcc.libs.qt.widgets import layouts, label, spinbox, buttons, checkbox

from tpRigToolkit.tools.rigtoolbox.widgets import base

LOGGER = tp.LogsMgr().get_logger('tpRigToolkit-tools-rigtoolbox')


class JointWidget(base.CommandRigToolBoxWidget, object):

    def __init__(self, client, commands_data, parent=None):

        self._model = JointWidgetModel()

        super(JointWidget, self).__init__(
            title='Joint', commands_data=commands_data,
            controller=JointWidgetController(model=self._model, client=client), parent=parent)

        self.refresh()

    @property
    def model(self):
        return self._model

    @property
    def controller(self):
        return self._controller

    def ui(self):
        super(JointWidget, self).ui()

        self._joints_to_insert_widget = QWidget()
        joints_to_insert_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        self._joints_to_insert_widget.setLayout(joints_to_insert_layout)
        joints_to_insert_lbl = label.BaseLabel('Num. Joints: ', parent=self)
        self._joints_to_insert_spn = spinbox.BaseSpinBox(parent=self)
        self._joints_to_insert_spn.setMinimum(1)
        self._joints_to_insert_spn.setMaximum(99999999)
        joints_to_insert_layout.addWidget(joints_to_insert_lbl)
        joints_to_insert_layout.addWidget(self._joints_to_insert_spn)

        self._create_joints_on_curve_widget = QWidget()
        create_joints_on_curve_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        self._create_joints_on_curve_widget.setLayout(create_joints_on_curve_layout)
        create_joints_on_curve_lbl = label.BaseLabel('Num. Joints: ', parent=self)
        self._create_joints_on_curve_spn = spinbox.BaseSpinBox(parent=self)
        self._create_joints_on_curve_spn.setMinimum(1)
        self._create_joints_on_curve_spn.setMaximum(99999999)
        create_joints_on_curve_layout.addWidget(create_joints_on_curve_lbl)
        create_joints_on_curve_layout.addWidget(self._create_joints_on_curve_spn)

        self._snap_joints_to_curve_widget = QWidget()
        snap_joints_to_curve_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        self._snap_joints_to_curve_widget.setLayout(snap_joints_to_curve_layout)
        snap_joints_to_curve_lbl = label.BaseLabel('Num. Joints: ', parent=self)
        self._snap_joints_to_curve_spn = spinbox.BaseSpinBox(parent=self)
        self._snap_joints_to_curve_spn.setMinimum(0)
        self._snap_joints_to_curve_spn.setMaximum(99999999)
        snap_joints_to_curve_layout.addWidget(snap_joints_to_curve_lbl)
        snap_joints_to_curve_layout.addWidget(self._snap_joints_to_curve_spn)

        self._joints_to_insert_widget.setVisible(False)
        self._create_joints_on_curve_widget.setVisible(False)
        self._snap_joints_to_curve_widget.setVisible(False)

        self.main_layout.addWidget(self._joints_to_insert_widget)
        self.main_layout.addWidget(self._create_joints_on_curve_widget)
        self.main_layout.addWidget(self._snap_joints_to_curve_widget)

    def setup_signals(self):
        self._joints_to_insert_spn.valueChanged.connect(self._controller.change_joints_to_insert)
        self._create_joints_on_curve_spn.valueChanged.connect(self._controller.change_joints_on_curve)
        self._snap_joints_to_curve_spn.valueChanged.connect(self._controller.change_snap_joints_to_curve)

        self._model.jointsToInsertChanged.connect(self._joints_to_insert_spn.setValue)
        self._model.jointsOnCurveChanged.connect(self._create_joints_on_curve_spn.setValue)
        self._model.snapJointsToCurveChanged.connect(self._snap_joints_to_curve_spn.setValue)

    def refresh(self):
        self._joints_to_insert_spn.setValue(self._model.joints_to_insert)
        # self._joints_display_size_spn.setValue(self._model.joints_display_size)
        # self._joints_display_size_live_cbx.setChecked(self._model.joints_display_size_live)
        self._create_joints_on_curve_spn.setValue(self._model.joints_on_curve)
        self._snap_joints_to_curve_spn.setValue(self._model.snap_joints_to_curve)

    def _setup_display_tools(self):
        display_widget = QWidget()
        self.display_layout = layouts.FlowLayout()
        self.display_layout.setAlignment(Qt.AlignLeft)
        display_widget.setLayout(self.display_layout)

        local_axis_on_icon = tp.ResourcesMgr().icon('local_rotation_on')
        local_axis_off_icon = tp.ResourcesMgr().icon('local_rotation_off')
        local_axis_on_all_icon = tp.ResourcesMgr().icon('local_rotation_on_all')
        local_axis_off_all_icon = tp.ResourcesMgr().icon('local_rotation_off_all')
        local_axis_on_selected_icon = tp.ResourcesMgr().icon('local_rotation_on_selection')
        local_axis_off_selected_icon = tp.ResourcesMgr().icon('local_rotation_off_selection')
        toggle_lra_btn = buttons.BaseToolButton(parent=self)
        toggle_lra_btn.setPopupMode(QToolButton.MenuButtonPopup)
        toggle_lra_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        toggle_lra_btn.setIcon(local_axis_on_icon)
        toggle_lra_btn.setText('Toggle LRA')
        toggle_lra_menu = QMenu(toggle_lra_btn)
        toggle_lra_btn.setMenu(toggle_lra_menu)
        toggle_all_axis_action = QAction(local_axis_on_icon, 'Toggle All Local Rotation Axis', toggle_lra_menu)
        toggle_selected_axis_action = QAction(local_axis_on_selected_icon, 'Toggle Selected Local Rotation Axis',
                                              toggle_lra_menu)
        local_axis_on_all_action = QAction(local_axis_on_all_icon, 'On | All Local Rotation Axis', toggle_lra_menu)
        local_axis_off_all_action = QAction(local_axis_off_all_icon, 'Off | All Local Rotation Axis', toggle_lra_menu)
        local_axis_on_selected_action = QAction(local_axis_on_selected_icon, 'On | Select Local Rotation Axis',
                                                toggle_lra_menu)
        local_axis_off_selected_action = QAction(local_axis_off_selected_icon, 'Off | Select Local Rotation Axis',
                                                 toggle_lra_menu)
        toggle_lra_menu.addAction(toggle_all_axis_action)
        toggle_lra_menu.addAction(toggle_selected_axis_action)
        toggle_lra_menu.addSeparator()
        toggle_lra_menu.addAction(local_axis_on_all_action)
        toggle_lra_menu.addAction(local_axis_off_all_action)
        toggle_lra_menu.addSeparator()
        toggle_lra_menu.addAction(local_axis_on_selected_action)
        toggle_lra_menu.addAction(local_axis_off_selected_action)

        toggle_lra_btn.clicked.connect(self._controller.toggle_local_rotation_axis)
        toggle_all_axis_action.triggered.connect(self._controller.toggle_all_local_rotation_axis)
        toggle_selected_axis_action.triggered.connect(self._controller.toggle_selected_local_rotation_axis)
        local_axis_on_all_action.triggered.connect(partial(self._controller.toggle_all_local_rotation_axis, True))
        local_axis_off_all_action.triggered.connect(partial(self._controller.toggle_all_local_rotation_axis, False))
        local_axis_on_selected_action.triggered.connect(
            partial(self._controller.toggle_selected_local_rotation_axis, True))
        local_axis_off_selected_action.triggered.connect(
            partial(self._controller.toggle_selected_local_rotation_axis, False))
        self.display_layout.addWidget(toggle_lra_btn)

        toggle_xray_btn = self._create_button('Toggle X-Ray', None, self._controller.toggle_xray)
        toggle_xray_menu = QMenu(toggle_xray_btn)
        toggle_xray_btn.setMenu(toggle_xray_menu)
        toggle_selected_xray_action = QAction(local_axis_on_icon, 'Toggle X-Ray in selected objects', toggle_xray_menu)
        toggle_xray_menu.addAction(toggle_selected_xray_action)
        toggle_xray_btn.clicked.connect(self._controller.toggle_xray)
        toggle_selected_xray_action.triggered.connect(self._controller.toggle_selected_xray)
        self.display_layout.addWidget(toggle_xray_btn)

        toggle_xray_joints_btn = self._create_button('Toggle X-Ray', None, self._controller.toggle_xray_joints)
        self.display_layout.addWidget(toggle_xray_joints_btn)

        joint_icon = tp.ResourcesMgr().icon('joint', extension='png')
        joint_display_size_widget = QWidget()
        joint_display_size_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        joint_display_size_widget.setLayout(joint_display_size_layout)
        joint_display_size_btn = self._create_button(
            'Joint Display Size', joint_icon, self._controller.set_joint_display_size)
        self._joints_display_size_spn = spinbox.DragDoubleSpinBoxLine(min=0.1, max=99, parent=self)
        self._joints_display_size_spn.setMaximumWidth(50)
        self._joints_display_size_live_cbx = checkbox.BaseCheckBox('Live', parent=self)
        joint_display_size_layout.addWidget(joint_display_size_btn)
        joint_display_size_layout.addWidget(self._joints_display_size_spn)
        joint_display_size_layout.addWidget(self._joints_display_size_live_cbx)
        self.display_layout.addWidget(joint_display_size_widget)

        self._joints_display_size_spn.textChanged.connect(self._on_joints_display_size_changed)
        self._joints_display_size_live_cbx.toggled.connect(self._controller.change_joints_display_size_live)
        self._model.jointsDisplaySizeChanged.connect(self._joints_display_size_spn.setValue)
        self._model.jointsDisplaySizeLiveChanged.connect(self._joints_display_size_live_cbx.setChecked)

        return display_widget

    def _setup_select_tools(self):
        select_widget = QWidget()
        self.select_layout = layouts.FlowLayout()
        self.select_layout.setAlignment(Qt.AlignLeft)
        select_widget.setLayout(self.select_layout)

        select_hierarchy_btn = self._create_button('Select Hierarchy', None, self._controller.select_hierarchy)
        self.select_layout.addWidget(select_hierarchy_btn)

        return select_widget

    def _setup_orient_tools(self):
        orient_widget = QWidget()
        self.orient_layout = layouts.FlowLayout()
        self.orient_layout.setAlignment(Qt.AlignLeft)
        orient_widget.setLayout(self.orient_layout)

        orient_icon = tp.ResourcesMgr().icon('orient_joints')
        orient_all_icon = tp.ResourcesMgr().icon('orient_all_joints')
        orient_selected_icon = tp.ResourcesMgr().icon('orient_selected_joints')
        orient_joint_btn = buttons.BaseToolButton(parent=self)
        orient_joint_btn.setPopupMode(QToolButton.MenuButtonPopup)
        orient_joint_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        orient_joint_btn.setIcon(orient_icon)
        orient_joint_btn.setText('Orient Joint')
        orient_joint_btn.setStatusTip('Joint Tool')
        orient_joint_btn.setToolTip('Joint Tool')
        orient_joint_menu = QMenu(orient_joint_btn)
        orient_joint_btn.setMenu(orient_joint_menu)
        orient_all_joints_action = QAction(orient_all_icon, 'Orient All Joints', orient_joint_menu)
        orient_selected_joints_action = QAction(orient_selected_icon, 'Orient Selected Joints', orient_joint_menu)
        orient_joint_menu.addAction(orient_all_joints_action)
        orient_joint_menu.addAction(orient_selected_joints_action)
        orient_joint_btn.clicked.connect(self._controller.orient_joints)
        orient_selected_joints_action.triggered.connect(self._controller.orient_selected_joints)
        orient_all_joints_action.triggered.connect(self._controller.orient_all_joints)
        self.orient_layout.addWidget(orient_joint_btn)

        add_icon = tp.ResourcesMgr().icon('plus', extension='png')
        add_orient_data_btn = buttons.BaseToolButton(parent=self)
        add_orient_data_btn.setPopupMode(QToolButton.MenuButtonPopup)
        add_orient_data_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        add_orient_data_btn.setIcon(add_icon)
        add_orient_data_btn.setText('Add Orient Data')
        add_orient_data_menu = QMenu(add_orient_data_btn)
        add_orient_data_btn.setMenu(add_orient_data_menu)
        add_all_orient_data_action = QAction(add_icon, 'Add All Joints Orient Data', add_orient_data_menu)

        if tp.is_maya():
            add_selected_orient_data_action = QAction(
                add_icon, 'Add Selected Joints Orient Data', add_orient_data_menu)
            add_orient_data_menu.addAction(add_all_orient_data_action)
            add_orient_data_menu.addAction(add_selected_orient_data_action)
            add_orient_data_btn.clicked.connect(self._controller.add_orient_data)
            add_all_orient_data_action.triggered.connect(self._controller.add_all_orient_data)
            add_selected_orient_data_action.triggered.connect(self._controller.add_selected_orient_data)
            self.orient_layout.addWidget(add_orient_data_btn)

        clean_icon = tp.ResourcesMgr().icon('clean', extension='png')
        clean_orient_data_btn = buttons.BaseToolButton(parent=self)
        clean_orient_data_btn.setPopupMode(QToolButton.MenuButtonPopup)
        clean_orient_data_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        clean_orient_data_btn.setIcon(clean_icon)
        clean_orient_data_btn.setText('Clean Orient Data')
        clean_orient_data_menu = QMenu(clean_orient_data_btn)
        clean_orient_data_btn.setMenu(clean_orient_data_menu)
        clean_all_orient_data_action = QAction(clean_icon, 'Clean All Joints Orient Data', clean_orient_data_menu)
        clean_selected_orient_data_action = QAction(clean_icon, 'Clean Selected Joints Orient Data',
                                                    clean_orient_data_menu)
        clean_orient_data_menu.addAction(clean_all_orient_data_action)
        clean_orient_data_menu.addAction(clean_selected_orient_data_action)
        clean_orient_data_btn.clicked.connect(self._controller.remove_orient_data)
        clean_all_orient_data_action.triggered.connect(self._controller.remove_all_orient_data)
        clean_selected_orient_data_action.triggered.connect(self._controller.remove_selected_orient_data)
        self.orient_layout.addWidget(clean_orient_data_btn)

        zero_joint_orient_btn = buttons.BaseToolButton(parent=self)
        zero_joint_orient_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        zero_joint_orient_btn.setIcon(add_icon)
        zero_joint_orient_btn.setText('Zero Joint Orient')
        zero_joint_orient_menu = QMenu(zero_joint_orient_btn)
        zero_all_joint_orient_action = QAction(add_icon, 'Zero Out All Joint Orientation', zero_joint_orient_menu)
        zero_selected_joint_orient_action = QAction(add_icon, 'Zero Out Seleected Joints Orientation',
                                                    zero_joint_orient_menu)
        zero_joint_orient_btn.clicked.connect(self._controller.zero_joint_orient)
        zero_all_joint_orient_action.triggered.connect(self._controller.zero_all_joint_orient)
        zero_selected_joint_orient_action.triggered.connect(self._controller.zero_selected_joint_orient)
        self.orient_layout.addWidget(zero_joint_orient_btn)

        orient_tool_icon = tp.ResourcesMgr().icon('orient_tool', extension='png')
        orient_tool_btn = buttons.BaseToolButton(parent=self)
        orient_tool_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        orient_tool_btn.setIcon(orient_tool_icon)
        orient_tool_btn.setText('Joint Orient Tool')
        orient_tool_btn.clicked.connect(self._controller.open_joint_orient_tool)
        self.orient_layout.addWidget(orient_tool_btn)

        return orient_widget

    def _setup_mirror_tools(self):
        mirror_widget = QWidget()
        self.mirror_layout = layouts.FlowLayout()
        self.mirror_layout.setAlignment(Qt.AlignLeft)
        mirror_widget.setLayout(self.mirror_layout)
        self.main_layout.addLayout(self.mirror_layout)

        mirror_icon = tp.ResourcesMgr().icon('mirror', extension='png')
        mirror_all_icon = tp.ResourcesMgr().icon('mirror_all', extension='png')
        mirror_selection_icon = tp.ResourcesMgr().icon('mirror_selection', extension='png')
        mirror_joint_btn = buttons.BaseToolButton(parent=self)
        mirror_joint_btn.setPopupMode(QToolButton.MenuButtonPopup)
        mirror_joint_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        mirror_joint_btn.setIcon(mirror_icon)
        mirror_joint_btn.setText('Mirror Joint')
        mirror_joint_menu = QMenu(mirror_joint_btn)
        mirror_joint_btn.setMenu(mirror_joint_menu)
        mirror_all_joints_action = QAction(mirror_all_icon, 'Mirror All Joints', mirror_joint_menu)
        mirror_selected_joints_action = QAction(mirror_selection_icon, 'Mirror Selected Joints', mirror_joint_menu)
        mirror_hierarchy_joints_action = QAction(mirror_selection_icon, 'Mirror Hierarchy Joints', mirror_joint_menu)
        mirror_joint_menu.addAction(mirror_all_joints_action)
        mirror_joint_menu.addAction(mirror_selected_joints_action)
        mirror_joint_menu.addAction(mirror_hierarchy_joints_action)
        mirror_joint_btn.clicked.connect(self._controller.mirror_all_joints)
        mirror_selected_joints_action.triggered.connect(self._controller.mirror_selected_joints)
        mirror_all_joints_action.triggered.connect(self._controller.mirror_all_joints)
        mirror_hierarchy_joints_action.triggered.connect(self._controller.mirror_hierarchy_joints)
        self.mirror_layout.addWidget(mirror_joint_btn)

        mirror_create_icon = tp.ResourcesMgr().icon('mirror2', extension='png')
        mirror_create_all_icon = tp.ResourcesMgr().icon('mirror2', extension='png')
        mirror_create_btn = buttons.BaseToolButton(parent=self)
        mirror_create_btn.setPopupMode(QToolButton.MenuButtonPopup)
        mirror_create_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        mirror_create_btn.setIcon(mirror_create_icon)
        mirror_create_btn.setText('Mirror Create')
        mirror_create_menu = QMenu(mirror_create_btn)
        mirror_create_btn.setMenu(mirror_create_menu)
        mirror_create_all_joints_action = QAction(
            mirror_create_all_icon, 'Mirror Create All Joints', mirror_create_menu)
        mirror_create_menu.addAction(mirror_create_all_joints_action)
        mirror_create_btn.clicked.connect(self._controller.mirror_create_all_joints)
        mirror_create_all_joints_action.triggered.connect(self._controller.mirror_create_all_joints)
        self.mirror_layout.addWidget(mirror_create_btn)

        return mirror_widget

    def _setup_pose_tools(self):
        pose_widget = QWidget()
        self.pose_layout = layouts.FlowLayout()
        self.pose_layout.setAlignment(Qt.AlignLeft)
        pose_widget.setLayout(self.pose_layout)

        go_to_bindpose_btn = buttons.BaseButton('Go to Bindpose', parent=self)
        self.pose_layout.addWidget(go_to_bindpose_btn)

        return pose_widget

    def _on_joints_display_size_changed(self, *args):
        value = self._joints_display_size_spn.value()
        self._joints_display_size_spn.blockSignals(True)
        self._controller.change_joints_display_size(value)
        self._joints_display_size_spn.blockSignals(False)

        live_mode = self._model.joints_display_size_live
        if live_mode:
            self._controller.set_joint_display_size()


class JointWidgetModel(QObject, object):

    jointsToInsertChanged = Signal(int)
    jointsOnCurveChanged = Signal(int)
    snapJointsToCurveChanged = Signal(int)
    jointsDisplaySizeChanged = Signal(float)
    jointsDisplaySizeLiveChanged = Signal(bool)

    def __init__(self):
        super(JointWidgetModel, self).__init__()

        self._joints_to_insert = 1
        self._joints_on_curve = 10
        self._snap_joints_to_curve = 0
        self._joints_display_size_live = True

        try:
            self._joints_display_size = tp.Dcc.get_joint_display_size()
        except Exception:
            LOGGER.warning('Impossible to retrieve current DCC joint display size. Using 1.0 by default ...')
            self._joints_display_size = 1.0

    @property
    def joints_to_insert(self):
        return self._joints_to_insert

    @joints_to_insert.setter
    def joints_to_insert(self, value):
        self._joints_to_insert = int(value)
        self.jointsToInsertChanged.emit(self._joints_to_insert)

    @property
    def joints_on_curve(self):
        return self._joints_on_curve

    @joints_on_curve.setter
    def joints_on_curve(self, value):
        self._joints_on_curve = int(value)
        self.jointsOnCurveChanged.emit(self._joints_on_curve)

    @property
    def snap_joints_to_curve(self):
        return self._snap_joints_to_curve

    @snap_joints_to_curve.setter
    def snap_joints_to_curve(self, value):
        self._snap_joints_to_curve = int(value)
        self.snapJointsToCurveChanged.emit(self._snap_joints_to_curve)

    @property
    def joints_display_size_live(self):
        return self._joints_display_size_live

    @joints_display_size_live.setter
    def joints_display_size_live(self, flag):
        self._joints_display_size_live = bool(flag)
        self.jointsDisplaySizeLiveChanged.emit(self._joints_display_size_live)

    @property
    def joints_display_size(self):
        return self._joints_display_size

    @joints_display_size.setter
    def joints_display_size(self, value):
        self._joints_display_size = float(value)
        self.jointsDisplaySizeChanged.emit(self._joints_display_size)


class JointWidgetController(object):

    def __init__(self, model, client):
        super(JointWidgetController, self).__init__()

        self._model = model
        self._client = client

    @property
    def model(self):
        return self._model

    @property
    def client(self):
        return self._client

    def change_joints_to_insert(self, value):
        self._model.joints_to_insert = value

    def change_joints_on_curve(self, value):
        self._model.joints_on_curve = value

    def change_snap_joints_to_curve(self, value):
        self._model.snap_joints_to_curve = value

    def change_joints_display_size(self, value):
        self._model.joints_display_size = value

    def change_joints_display_size_live(self, flag):
        self._model.joints_display_size_live = flag

    def start_joint_tool(self):
        return self._client.start_joint_tool()

    def create_new_joint_on_center(self):
        return self._client.create_new_joint_on_center()

    def insert_joints(self):
        joint_count = self._model.joints_to_insert
        return self._client.insert_joints(num_joints=joint_count)

    def create_joints_on_curve(self):
        joints_on_curve = self._model.joints_on_curve
        return self._client.create_joints_on_curve(num_joints=joints_on_curve)

    def snap_joints_to_curve(self):
        joints_to_snap = self._model.snap_joints_to_curve
        return self._client.snap_joints_to_curve(num_joints=joints_to_snap)

    def set_joint_display_size(self):
        joints_display_size = self._model.joints_display_size
        return tp.Dcc.set_joint_display_size(joints_display_size)

    def select_hierarchy(self):
        return tp.Dcc.select_hierarchy()

    def mirror_all_joints(self):
        """
        Mirror all scene joints
        """

        return tp.Dcc.mirror_transform()

    def mirror_selected_joints(self):
        """
        Mirror selected joints
        """

        selected = tp.Dcc.selected_nodes_of_type('transform', full_path=False)
        if not selected:
            LOGGER.warning('Please select joints to mirror!')
            return

        return tp.Dcc.mirror_transform(transforms=selected)

    def mirror_hierarchy_joints(self):
        """
        Mirror selected joints and its hierarchy
        """

        all_xforms = list()
        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        for xform in selected:
            all_xforms.append(xform)
            children = tp.Dcc.list_children(full_path=False, children_type='transform')
            found = list()
            if children:
                for child in children:
                    if tp.Dcc.node_type(child).find('Constraint') > -1:
                        continue
                    found.append(child)
            all_xforms.extend(found)

        all_xforms = list(set(all_xforms))

        return tp.Dcc.mirror_transform(transforms=all_xforms)

    def mirror_create_joints(self):
        """
        Mirrors and create the selected joints
        """

        selected = tp.Dcc.selected_nodes_of_type(node_type='transform') or list()
        created = tp.Dcc.mirror_transform(transforms=selected, create_if_missing=True)
        if created and selected:
            LOGGER.warning('Only created transforms on the right side that were selected on the left')
        if created and not selected:
            LOGGER.info('Created transforms on the right side that were on the left')
        if not created:
            LOGGER.warning(
                'No transforms created. Check that are missing transforms on the right. '
                'Check your selected transforms is on the left!')

    def mirror_create_all_joints(self):
        """
        Mirrors and creates all joints
        """

        created = tp.Dcc.mirror_transform(create_if_missing=True)
        if created:
            LOGGER.info('Created transforms on the right side that were on the left')
        else:
            LOGGER.warning(
                'No transforms created. Check that are missing transforms on the right. '
                'Check your selected transforms is on the left!')

    def mirror_joints(self):
        """
        Mirror joints. If no joints are selected all scene joints will be mirrored; otherwise only selected joints will
        mirrored
        :return: bool, Whether the operation was successful or not
        """

        selected = tp.Dcc.selected_nodes_of_type(node_type='joint') or list()
        if selected and len(selected) > 0:
            oriented = self.mirror_selected_joints()
        else:
            oriented = self.mirror_all_joints()

        if oriented:
            LOGGER.info('Mirrored joints left to right!')
        else:
            LOGGER.warning('No joints mirrored. Check there are joints on the left that can mirror right!')

    def orient_all_joints(self, force_orient_attributes=True):
        """
        Orients all joints
        """

        return tp.Dcc.orient_joints(force_orient_attributes=force_orient_attributes)

    def orient_selected_joints(self, force_orient_attributes=True):
        """
        Orient selected joints
        :param force_orient_attributes: bool, Whether to force the orientation through OrientJointAttributes or not
        """

        selected = tp.Dcc.selected_nodes_of_type('joint', full_path=False)
        if not selected:
            LOGGER.warning('Please select joints to orient')
            return

        oriented = tp.Dcc.orient_joints(joints_to_orient=selected, force_orient_attributes=force_orient_attributes)

        tp.Dcc.select_node(selected)

        return oriented

    def orient_joints(self):
        """
        Orients all scene objects that have OrientJointAttributes added
        """

        selected = tp.Dcc.selected_nodes_of_type('joint', full_path=False)
        if selected and len(selected) > 0:
            oriented = self.orient_selected_joints()
        else:
            oriented = self.orient_all_joints()

        if oriented:
            LOGGER.info('Oriented all scene joints using OrientAttributes!')
        else:
            LOGGER.warning('No joints oriented. Check that there are joints with OrientAttributes!')

    def add_selected_orient_data(self):
        from tpDcc.dccs.maya.core import joint

        selected = tp.Dcc.selected_nodes_of_type('joint', full_path=False)
        if not selected:
            LOGGER.warning('Please select joints to add orient attributes to')
            return False

        joint.OrientJointAttributes.add_orient_attributes(selected)

        return True

    def add_all_orient_data(self):
        from tpDcc.dccs.maya.core import joint

        all_joints = tp.Dcc.list_nodes(node_type='joint', full_path=False)
        if not all_joints:
            LOGGER.warning('No joints found in the current scene')
            return False

        joint.OrientJointAttributes.add_orient_attributes(all_joints)

        return True

    def add_orient_data(self):
        """
        Add orient data from joints
        """

        if not tp.is_maya():
            LOGGER.warning('Add Orient data command is only available in Maya for now ...')
            return False

        selected = tp.Dcc.selected_nodes_of_type('joint', full_path=False)
        if selected and len(selected) > 0:
            removed = self.add_selected_orient_data()
        else:
            removed = self.add_all_orient_data()

        if removed:
            if selected:
                LOGGER.info('Added selected joints oriented data attributes!')
            else:
                LOGGER.info('Added all scene joints oriented data attributes!')
        else:
            LOGGER.warning('No orient data added!')

    def remove_selected_orient_data(self):
        from tpDcc.dccs.maya.core import joint

        selected = tp.Dcc.selected_nodes_of_type('joint', full_path=False)
        if not selected:
            LOGGER.warning.emit('Please select joints to remove orient attributes from')
            return False

        joint.OrientJointAttributes.remove_orient_attributes(selected)

        return True

    def remove_all_orient_data(self):
        from tpDcc.dccs.maya.core import joint

        all_joints = tp.Dcc.list_nodes(node_type='joint', full_path=False)
        if not all_joints:
            LOGGER.warning('No joints found in the current scene')
            return False

        joint.OrientJointAttributes.remove_orient_attributes(all_joints)

        return True

    def remove_orient_data(self):
        """
        Removes all orient data from joints
        """

        if not tp.is_maya():
            LOGGER.warning('Remove Orient data command is only available in Maya for now ...')
            return False

        selected = tp.Dcc.selected_nodes_of_type('joint', full_path=False)
        if selected and len(selected) > 0:
            removed = self.remove_selected_orient_data()
        else:
            removed = self.remove_all_orient_data()

        if removed:
            if selected:
                LOGGER.info('Removed selected joints oriented data attributes!')
            else:
                LOGGER.info('Removed all scene joints oriented data attributes!')
        else:
            LOGGER.warning('No orient data removed. Check that there are joints with OrientAttributes!')

    def zero_selected_joint_orient(self):
        selected = tp.Dcc.selected_nodes_of_type('joint', full_path=False)
        if not selected:
            LOGGER.warning('Please select joints to zero out orient joint of')
            return False

        return tp.Dcc.zero_orient_joint(selected)

    def zero_all_joint_orient(self):
        all_joints = tp.Dcc.list_nodes(node_type='joint', full_path=False)
        if not all_joints:
            LOGGER.warning('No joints found in the current scene')
            return False

        return tp.Dcc.zero_orient_joint(all_joints)

    def zero_joint_orient(self):
        """
        Zeroes joint orient orient
        """

        selected = tp.Dcc.selected_nodes_of_type('joint', full_path=False)
        if selected and len(selected) > 0:
            removed = self.zero_selected_joint_orient()
        else:
            removed = self.zero_all_joint_orient()

        if removed:
            if selected:
                LOGGER.warning('Zeroes selected joints joint orientation attributes!')
            else:
                LOGGER.info('Zeroed out all scene joints orientation attributes!')
        else:
            LOGGER.warning('No orientation zeroed out!')

    @tp.Dcc.undo_decorator()
    def toggle_all_local_rotation_axis(self, value=None):
        """
        Toggles the visibility of all joints local rotation axis
        """

        return tp.Dcc.set_joint_local_rotation_axis_visibility(value)

    def toggle_selected_local_rotation_axis(self, value=None):
        """
        Toggles the visibility of selected joints local rotation axis
        """

        selected = tp.Dcc.selected_nodes_of_type('joint', full_path=False)
        if not selected:
            LOGGER.warning('Please select joints to toggle local rotation axis from')
            return

        return tp.Dcc.set_joint_local_rotation_axis_visibility(value, joints_to_apply=selected)

    def toggle_local_rotation_axis(self):
        """
        Toggles the visibility of all (if the user has nothing selected) or all joints local rotation axis
        """

        selected = tp.Dcc.selected_nodes_of_type('joint', full_path=False)
        if selected and len(selected) > 0:
            toggled = self.toggle_selected_local_rotation_axis()
        else:
            toggled = self.toggle_all_local_rotation_axis()

        if toggled:
            LOGGER.info('Toggled joints local rotation axis!')
        else:
            LOGGER.warning('Impossible to toggle joints local rotation axis!')

    def open_joint_orient_tool(self):
        tp.ToolsMgr().launch_tool_by_id('tpRigToolkit-tools-jointorient')

    def toggle_xray(self):
        return tp.Dcc.toggle_xray()

    def toggle_selected_xray(self):
        return tp.Dcc.toggle_xray_on_selection()

    def toggle_xray_joints(self):
        return tp.Dcc.toggle_xray_joints()
