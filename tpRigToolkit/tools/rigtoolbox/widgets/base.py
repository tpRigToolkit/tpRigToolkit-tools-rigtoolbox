#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base class for tpRigToolbox widgets
"""

from __future__ import print_function, division, absolute_import

from functools import partial

from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *

import tpDcc as tp
from tpDcc.libs.python import python
from tpDcc.libs.qt.widgets import layouts, buttons


class BaseRigToolBoxWidget(QFrame, object):

    emitInfo = Signal(str)
    emitWarning = Signal(str)
    emitError = Signal(str, object)
    setDescription = Signal(str)

    def __init__(self, title, parent=None):
        super(BaseRigToolBoxWidget, self).__init__(parent=parent)

        self._title = title
        self._menus = dict()

        self.main_layout = layouts.VerticalLayout(spacing=0, margins=(0, 0, 0, 0))
        self.main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.main_layout)

    @property
    def title(self):
        return self._title

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverEnter:
            description = obj.property('description') or obj.text()
            self.setDescription.emit(description)
        elif event.type() == QEvent.HoverLeave:
            self.setDescription.emit('')

        return super(BaseRigToolBoxWidget, self).eventFilter(obj, event)

    def _create_button(
            self, text, icon, fn, status=None, tooltip=None, description=None, actions=None, whats_this='',
            has_settings=False, settings_fn=None):
        """
        Internal function to easily create buttons for the box widget
        :param text:
        :param icon:
        :param fn:
        :param status:
        :param tooltip:
        :return:
        """

        new_btn = buttons.BaseButton(parent=self).small()
        if icon:
            new_btn.setIcon(icon)
        new_btn.setText(text)
        new_btn.setObjectName(text.replace(' ', '').lower() or description)
        new_btn.setStatusTip(status or text)
        new_btn.setToolTip(tooltip or text)
        new_btn.setProperty('description', description)
        new_btn.setStyleSheet('qproperty-iconSize: 20px 20px;')
        new_btn.setIconSize(QSize(20, 20))
        new_btn.setWhatsThis(whats_this or tooltip or text)
        new_btn.setContextMenuPolicy(Qt.CustomContextMenu)
        new_btn.installEventFilter(self)
        if fn:
            new_btn.clicked.connect(fn)
        new_btn.customContextMenuRequested.connect(self._on_show_context_menu)

        self._add_menu(new_btn, actions)

        if has_settings:
            settings_icon = tp.ResourcesMgr().icon('settings')
            buttons_widget = QWidget()
            buttons_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
            buttons_widget.setLayout(buttons_layout)
            options_btn = self._create_button(
                '', settings_icon, settings_fn, has_settings=False, description='{} Options'.format(description))
            new_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            new_btn.setStyleSheet(
                new_btn.styleSheet() + ';border-top-right-radius: 0px; border-bottom-right-radius: 0px; '
                                       'border-right: 0px;')
            new_btn.setMaximumWidth(28)

            options_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            options_btn.setMaximumWidth(18)
            options_btn.setStyleSheet(
                options_btn.styleSheet() + ';border-top-left-radius: 0px; border-bottom-left-radius: 0px; '
                                           'qproperty-iconSize: 12px 12px;')
            buttons_layout.addWidget(new_btn)
            buttons_layout.addWidget(options_btn)

            return buttons_widget, new_btn, options_btn

        return new_btn

    def _add_menu(self, button, actions=None):

        object_name = button.objectName()
        actions = python.force_list(actions)
        self._menus.setdefault(object_name, None)
        new_menu = QMenu(self)
        if actions:
            for action in actions:
                if action is None:
                    new_menu.addSeparator()
                else:
                    new_menu.addAction(action)
        else:
            whats_this_action = QAction("What's This?", new_menu)
            whats_this_action.triggered.connect(partial(self._on_show_whats_this, button.whatsThis()))
            new_menu.addAction(whats_this_action)

        self._menus[object_name] = new_menu

    def _on_show_whats_this(self, whats_this_text):
        pos = QCursor.pos()
        if not whats_this_text:
            return
        QWhatsThis.showText(pos, whats_this_text, self)

    def _on_show_context_menu(self):
        sender = self.sender()
        if not sender:
            return

        sender_name = sender.objectName()
        if sender_name not in self._menus:
            return

        self._menus[sender_name].exec_(QCursor.pos())
