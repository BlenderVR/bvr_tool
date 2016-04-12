# -*- coding: utf-8 -*-
# file: bvr/ui.py

# TODO: May have to make BlenderVR GPL to include in blender tools
# (see licence policies for such tools).

import bpy
from bpy.types import Panel

# ############################################################
# User Interface
# ############################################################

class BlenderVRUIBase:
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_description= ""
    bl_category = "BlenderVR"

class BlenderVRToolBar(BlenderVRUIBase, Panel):

    bl_label = "BlenderVR"

    @staticmethod
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        blendervr = scene.blendervr
        obj = context.object

        # ----------------------------------------------
        row = layout.row()
        row.label("BlenderVR Configuration:")

        # Configuration file
        col = layout.column()
        rowsub = col.row(align=True)
        rowsub.label("Select config file:")
        rowsub = col.row(align=True)
        rowsub.prop(blendervr, "config_file_path", text="")
        rowsub = col.row(align=True)
        rowsub.operator("bvr.loadconfigfile", text="Load").arg = 'load'
        rowsub.operator("bvr.loadconfigfile", text="Create New").arg = 'new'

        # Screen setup
        col = layout.column()
        rowsub = col.row(align=True)
        rowsub.label("Select screen setup:")
        rowsub = col.row(align=True)
        rowsub.prop(blendervr, "screen_setup", text="")

        # Blender scene
        col = layout.column()
        rowsub = col.row(align=True)
        rowsub.label("Select Blender scene:")
        rowsub = col.row()
        rowsub.prop(blendervr, "blend_scene_file_path", text="")
        rowsub = col.row(align=True)
        rowsub.operator("bvr.loadblenderscene", text="Use Current").arg = 'current'

        # Processor file
        col = layout.column()
        rowsub = col.row(align=True)
        rowsub.label("Select Processor File:")
        rowsub = col.row()
        rowsub.prop(blendervr, "processor_file_path", text="")
        rowsub = col.row(align=True)
        rowsub.operator("bvr.loadblenderscene", text="Name Link").arg = 'NameLink'

        # Launcher
        row = layout.row()
        row.label("BlenderVR Launcher:")
        rowsub = layout.row(align=True)
        rowsub.operator("bvr.launcher", text='Start').arg = 'start'
        rowsub.operator("bvr.launcher", text='Stop').arg = 'stop'

        # Debug Windows
        row = layout.row()
        row.label("Debug Windows:")
        rowsub = layout.row(align=True)
        rowsub.operator("bvr.launcher", text='Display Debug Windows').arg = 'debug.window'


class BVRDisplaySystemToolBar(BlenderVRUIBase, Panel):
    """Panel to select a Virtual Reality system to use and activate it."""
    bl_label = "VR Display System"
        layout = self.layout

        scene = context.scene
        blendervr = scene.blendervr
        obj = context.object

        # ----------------------------------------------
        row = layout.row()

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
        rowsub.operator("bvr.loadconfigfile", text="Reload").arg = 'load'
        rowsub.operator("bvr.loadconfigfile", text="Create New").arg = 'new'
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
        rowsub.operator("bvr.launcher", text="Start").arg = 'start'
        rowsub.operator("bvr.launcher", text="Stop").arg = 'stop'
        rowsub = col.row(align=True)
        rowsub.prop(blendervr, "auto_open_logs", text="")

class BVRSceneScriptsToolBar(BlenderVRUIBase, Panel):
    """Panel to select a scene file, processir, and to use it in VR system."""
    bl_label = "VR Scene And Scripts"
        layout = self.layout

        scene = context.scene
        blendervr = scene.blendervr
        obj = context.object

        # ----------------------------------------------
        row = layout.row()

        # Configuration file
        # A file selection field (with right button to open dialog)
        # followed by two action buttons, 
        col = layout.column()
        rowsub = col.row(align=True)
        rowsub.label("Configuration File:")
        rowsub = col.row(align=True)
        rowsub.prop(blendervr, "config_file_path", text="")
        rowsub = col.row(align=True)
        rowsub.operator("bvr.loadconfigfile", text="Reload").arg = 'load'
        rowsub.operator("bvr.loadconfigfile", text="Create New").arg = 'new'
        rowsub = col.row(align=True)
        rowsub.label("Screens Set:")
        rowsub = col.row(align=True)
        rowsub.prop(blendervr, "screen_setup", text="")

        
# ############################################################
# Un/Registration
# ############################################################

def register():
    #bpy.utils.register_class(BlenderVRToolBar)
    bpy.utils.register_class(BVRDisplaySystemToolBar)
    bpy.utils.register_class(BVRSceneScriptsToolBar)

def unregister():
    #bpy.utils.unregister_class(BlenderVRToolBar)
    bpy.utils.unregister_class(BVRDisplaySystemToolBar)
    bpy.utils.unregister_class(BVRSceneScriptsToolBar)
