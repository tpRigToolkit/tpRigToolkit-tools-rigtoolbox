#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Average Vertex Weights Maya plugin implementation
"""

from __future__ import print_function, division, absolute_import

import sys

from maya.api import OpenMaya as OpenMaya


def maya_useNewAPI():
    pass


class AverageVertexWeightsCommand(OpenMaya.MPxCommand):

    commandName = 'tpAverageVertexWeights'

    def __init__(self):
        super(AverageVertexWeightsCommand, self).__init__()

        self._index_arg = ''
        self._weight_arg = None
        self._skin_cluster_arg = ''

        self._skin_fn = None
        self._components = None
        self._influence_indices = None
        self._dag_path = OpenMaya.MDagPath()
        self._old_weights = OpenMaya.MDoubleArray()

    @classmethod
    def command_creator(cls):
        return AverageVertexWeightsCommand()

    @staticmethod
    def syntax_creator():
        syntax = OpenMaya.MSyntax()
        syntax.addFlag('sc', 'skinCluster', OpenMaya.MSyntax.kString)
        syntax.addFlag('i', 'index', OpenMaya.MSyntax.kString)
        syntax.addFlag('w', 'weight', OpenMaya.MSyntax.kDouble)

        return syntax

    def isUndoable(self):
        return True

    def doIt(self, args):
        try:
            self._parse_args(args)
        except Exception as exc:
            OpenMaya.MGlobal.displayError('{} : invalid flag syntax'.format(self.commandName))
            return

        self._skin_fn = self._get_skin_cluster()
        if not self._skin_cluster_arg:
            OpenMaya.MGlobal.displayError('Select a mesh that contains a skinCluster node')

        self.redoIt()

    def undoIt(self):
        pass

    def redoIt(self):
        self._dag_path, self._components = self._get_mesh()

        surrounding_weights = OpenMaya.MDoubleArray()
        surrounding_vertex_array = OpenMaya.MIntArray()
        influences_count = 0
        influence = None

        vertex_iterator = OpenMaya.MItMeshVertex(self._dag_path, self._components)
        surrounding_vertex_array = vertex_iterator.getConnectedVertices()
        surrounding_components = OpenMaya.MFnSingleIndexedComponent().create(OpenMaya.MFn.kMeshVertComponent)
        OpenMaya.MFnSingleIndexedComponent(surrounding_components).addElements(surrounding_vertex_array)

        self._old_weights, influence = self._skin_fn.getWeights(self._dag_path, self._components)
        surrounding_weights, influence = self._skin_fn.getWeights(self._dag_path, surrounding_components)

        print(self._old_weights)
        print(surrounding_weights)
        print(influence)

    def _parse_args(self, args):
        args_data = OpenMaya.MArgDatabase(self.syntax(), args)
        if args_data.isFlagSet('sc'):
            self._skin_cluster_arg = args_data.flagArgumentString('sc', 0)
        if args_data.isFlagSet('i'):
            self._index_arg = args_data.flagArgumentString('i', 0)
        if args_data.isFlagSet('w'):
            self._weight_arg = args_data.flagArgumentString('w', 0)

    def _get_skin_cluster(self):
        selection_list = OpenMaya.MGlobal.getSelectionListByName(self._skin_cluster_arg)
        skin_fn = selection_list.getDependNode(0)

        return skin_fn

    def _get_mesh(self):
        selection_list = OpenMaya.MGlobal.getSelectionListByName(self._index_arg)
        dag_path = selection_list.getDagPath(0)
        components = selection_list.getComponent(0)

        return dag_path, components


def initializePlugin(mobj):
    mplugin = OpenMaya.MFnPlugin(mobj, 'Tomas Poveda', '1.0', 'Any')
    try:
        mplugin.registerCommand(
            AverageVertexWeightsCommand.commandName, AverageVertexWeightsCommand.command_creator,
            AverageVertexWeightsCommand.syntax_creator)
    except Exception as exc:
        sys.stderr.write('Failed to register command: {}'.format(AverageVertexWeightsCommand.commandName))
        sys.stderr.write('{}\n'.format(exc))


def uninitializePlugin(mobj):
    mplugin = OpenMaya.MFnPlugin(mobj)
    try:
        mplugin.deregisterCommand(AverageVertexWeightsCommand.commandName)
    except Exception as exc:
        sys.stderr.write('Failed to unregister command: {}'.format(AverageVertexWeightsCommand.commandName))
        sys.stderr.write('{}\n'.format(exc))
