# -*- coding: utf-8 -*-
# file: bvr/bvrui.py

## Copyright (C) LIMSI-CNRS (2016)
##
## contributor(s) : Jorge Gascon, Damien Touraine, David Poirier-Quinot,
## Laurent Pointal, Julian Adenauer,
##
## This software is a computer program whose purpose is to distribute
## blender to render on Virtual Reality device systems.
##
## This software is governed by the CeCILL  license under French law and
## abiding by the rules of distribution of free software.  You can  use,
## modify and/ or redistribute the software under the terms of the CeCILL
## license as circulated by CEA, CNRS and INRIA at the following URL
## "http://www.cecill.info".
##
## As a counterpart to the access to the source code and  rights to copy,
## modify and redistribute granted by the license, users are provided only
## with a limited warranty  and the software's author,  the holder of the
## economic rights,  and the successive licensors  have only  limited
## liability.
##
## In this respect, the user's attention is drawn to the risks associated
## with loading,  using,  modifying and/or developing or reproducing the
## software by the user in light of its specific status of free software,
## that may mean  that it is complicated to manipulate,  and  that  also
## therefore means  that it is reserved for developers  and  experienced
## professionals having in-depth computer knowledge. Users are therefore
## encouraged to load and test the software's suitability as regards their
## requirements in conditions enabling the security of their systems and/or
## data to be ensured and,  more generally, to use and operate it in the
## same conditions as regards security.
##
## The fact that you are presently reading this means that you have had
## knowledge of the CeCILL license and that you accept its terms.

# <pep8 compliant>

"""
"""

from os import path as osp
import logging
logger = logging.getLogger(__name__)

import bpy

# Load our environment settings (include standard config access path).
from . import (
    RUNTIME,
    bvrenv,
    bvrprops,
    )

# To debug this module.
DEBUG = True and not RUNTIME

# ############################################################
# User Interface
# ############################################################

# Define common sidebar location for all our panels.
class BlenderVRUIBase:
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_description= "Blender Virtuel Reality integration within Game Engine."
    bl_category = "BlenderVR"   # The side tab name where toolbar must be displayed.

    @classmethod
    def poll(cls, context):
        """Return True if the user interface is compatible with current mode.
        """
        return True
        # TODO: return False if used in BGE mode by example. ?
        rd = context.scene.render
        return rd.engine in cls.COMPAT_ENGINES


# Note: some row/column layouts are created just to manage enable/disable
# on widgets.
class BVRDisplaySystemToolBar(BlenderVRUIBase, bpy.types.Panel):
    """Panel to select a Virtual Reality display system to use and activate it."""
    bl_label = "VR System"

    @staticmethod
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        blendervr = scene.blendervr
        obj = context.object

        # ----------------------------------------------
        #row = layout.row()

        # Configuration file
        # A file selection field (with right button to open dialog)
        # followed by two action buttons, to reload or create 
        # a configuration using current scene objects geometry.
        col = layout.column()
        rowsub = col.row(align=True)
        rowsub.label("Configuration File:")
        rowsub = col.row(align=True)
        rowsub.prop(blendervr, "config_file_path", text="")

        # TODO: must load the file content when it is valid (to update
        # widgets status upon that content and its validity).
        rowsub = col.row(align=True)
        rowsub.operator("bvr.configfile", text="Reload").action = 'load'
        rowsub.enabled = blendervr.status_exists_config_file
        #rowsub.operator("bvr.configfile", text="Create New").action = 'new'
        rowsub = col.row(align=True)

        # A selection list to select a screens set from those listed in
        # the selected configuration file.
        # TODO: must update the list when configuration file change.
        rowsub.label("Screens Set:")
        rowsub = col.row(align=True)
        rowsub.prop(blendervr, "screen_setup", text="")

        # Two buttons to manage start and stop of daemons, and a checkbox
        # to have an automatic open of logs on error.
        rowsub = col.row(align=True)
        rowsub.label("RV Daemons:")
        rowsub = col.row(align=True)
        #rowsub.enabled = blendervr.status_valid_display
        colsub = rowsub.column()
        colsub.operator("bvr.launcher", text="Start").action = 'startdaemons'
        colsub.enabled = not blendervr.status_daemons_started
        colsub = rowsub.column()
        colsub.operator("bvr.launcher", text="Stop").action = 'stopdaemons'
        colsub.enabled = blendervr.status_daemons_started


        rowsub = col.row(align=True)
        rowsub.prop(blendervr, "auto_open_logs", "Auto open logs")

def config_file_path_updated(self, context):
    """Manage updating of configuration file path field.
    
    Check if the file exists, if it exists, load it immediatly.
    This trig the screen set update too.
    Method registered for config_file_path property update.
    """
    newpath = self.config_file_path
    self.status_exists_config_file = osp.isfile(newpath)
    if self.status_exists_config_file:
        bpy.ops.bvr.configfile(action='load')

bvrprops.register_update_handler('config_file_path', config_file_path_updated)

class BVRSceneScriptsToolBar(BlenderVRUIBase, bpy.types.Panel):
    """Panel to select a scene file, processir, and to use it in VR system."""
    bl_label = "VR Scene & Scripts"

    @staticmethod
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        blendervr = scene.blendervr
        obj = context.object

        # ----------------------------------------------
        #row = layout.row()

        # Blender scene
        col = layout.column()
        rowsub = col.row(align=True)
        rowsub.label("Blender Scene:")
        rowsub = col.row()
        rowsub.prop(blendervr, "blend_scene_file_path", text="")
        rowsub = col.row(align=True)
        rowsub.operator("bvr.blenderscene", text="Use Current").action = 'usecurrent'

        # Processor file
        col = layout.column()
        rowsub = col.row(align=True)
        rowsub.label("Processor File:")
        rowsub = col.row()
        rowsub.prop(blendervr, "processor_file_path", text="")
        rowsub = col.row(align=True)
        rowsub.operator("bvr.blenderscene", text="Name Link").action = 'usenamelink'


        # Two buttons to manage start and stop of blenderplayers.
        rowsub = col.row(align=True)
        rowsub.label("Scene Play:")
        rowsub = col.row(align=True)
        rowsub.operator("bvr.launcher", text="Start").action = 'startplay'
        rowsub.operator("bvr.launcher", text="Stop").action = 'stopplay'


class BVRStatusToolBar(BlenderVRUIBase, bpy.types.Panel):
    """Panel to show current daemons / renderers status and interact."""
    bl_label = "VR Status"

    @staticmethod
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        blendervr = scene.blendervr
        obj = context.object

        # ----------------------------------------------
        row = layout.row()
        col = layout.column()
        rowsub = col.row(align=True)
        rowsub.label("Daemons &  Players status:")

        # Add a menu to allow grouped operations on ALL daemons/players.
        
        # For each daemon/player, add sets of grouped items with each containing:
            # Maybe a label (?)
            # An colored icon / text? representing the state
            # An interaction menu




# ======================================================================
def register():
    if DEBUG:
        logger.debug("Registering bvr.bvrui classes.")
    bpy.utils.register_class(BVRDisplaySystemToolBar)
    bpy.utils.register_class(BVRSceneScriptsToolBar)
    bpy.utils.register_class(BVRStatusToolBar)

def unregister():
    if DEBUG:
        logger.debug("Unregistering bvr.bvrui classes.")
    bpy.utils.unregister_class(BVRDisplaySystemToolBar)
    bpy.utils.unregister_class(BVRSceneScriptsToolBar)
    bpy.utils.unregister_class(BVRStatusToolBar)
