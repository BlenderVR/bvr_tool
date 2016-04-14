# -*- coding: utf-8 -*-
# file: bvr/bvroperators.py

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

An operator object is created for each operations when binding the
operator within the interface. You must set the operator's object action
property.
"""

import bpy
from bpy.types import Operator


class BlenderVRConfigFileOperator(Operator):
    """Load/reload/create BlenderVR configuration file.

    When the file is loaded, its available screens sets is used to
    refresh tool ui (list of screens sets).

    """
    bl_label = "Manipulate BlenderVR Configuration File"
    bl_idname = 'bvr.configfile'
    bl_options = {'REGISTER'}

    # Execute action is given as a property of the object itself.
    action = bpy.props.StringProperty(options={'HIDDEN'}, default="undefined")

    def execute(self, context):

        act = self.action    # Retrieve string.

        if act == "new":
            return self.execute_new(context)
        elif act == "load":
            return self.execute_load(context)
        elif act == "reload":
            return self.execute_reload(context)
        elif act :
            self.report({'ERROR'}, 'action "{}" (in configfile) not defined yet'.format(action))
            return {'CANCELLED'}


    def execute_new(self, context):
        # cleanup before we start
        # bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}

    def execute_load(self, context):


        # get file path
        scene = context.scene
        props = scene.blendervr
        filepath = bpy.path.abspath(props.config_file_path)
        # file_path = bpy.path.ensure_ext(filepath, ".x3d")

        # get console
        # bpy.ops.screen.new()
        # bpy.ops.screen.area_dupli()
        # bpy.ops.screen.userpref_show()
        print('configuration file: ' + filepath)


        return {'FINISHED'}

    def execute_reload(self, context):
        return {'FINISHED'}



class BlenderVRSceneLoadOperator(Operator):
    """"""
    bl_label = "Load Configuration File"
    bl_idname = 'bvr.blenderscene'
    bl_options = {'REGISTER', 'UNDO'}

    action = bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):

        act = self.action    # Retrieve string.

        if act == "usecurrent":
            return self.execute_usecurrent(context)
        elif act == "loadscene":
            return self.execute_loadscene(context)
        elif act == "usenamelink":
            return self.execute_usenamelink(context)
        elif act :
            raise RuntimeError("BlenderVRSceneLoadOperator - Bug, you miss to set action property")
        else:
            raise RuntimeError("BlenderVRSceneLoadOperator - Bug, unknown action {}".format(act))

    def execute_usecurrent(self, context):
        """Use the currently opened scene as VR system target scene."""
        bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}

    def execute_loadscene(self, context):
        """Use an external providen .blend file as VR system target scene."""
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}
    
    def execute_usenamelink(self, context):
        """Use processor file based on selected scene file."""
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}


class BlenderVRLaunchOperator(bpy.types.Operator):
    """"""
    bl_label = "BlenderVR Launcher"
    bl_idname = 'bvr.launcher'
    bl_options = {'REGISTER', 'UNDO'}

    action = bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):

        act = self.action    # Retrieve string.


        if act == 'startdaemons':
            return self.execute_startdaemons(context)
        elif act == 'stopdaemons':
            return self.execute_stopdaemons(context)
        elif act == 'startplay':
            return self.execute_startplay(context)
        elif act == 'stopplay':
            return self.execute_stopdaemons(context)
        elif act == 'debugwindow':
            return self.execute_debugwindow(context)
        else:
            self.report({'ERROR'}, 'action "{}" (in launcher) not defined yet'.format(action))
            return {'CANCELLED'}

    def execute_startdaemons(self, context):
        """Start control daemons on rendering nodes."""

         # get file path
        scene = context.scene
        props = scene.blendervr
        # tryout, start blenderplayer
        # bpy.ops.wm.blenderplayer_start()

        import subprocess
        args = ['python3', '/Users/AstrApple/WorkSpace/Blender_Workspace/addons/blendervr/source/blenderVR', 'controller']
        props.proc = subprocess.Popen(args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        print('opened',props.proc)

        # outs, errs = props.proc.communicate(timeout=15)
        outs, errs = props.proc.communicate()
        print('first words: \n', outs,errs)

        return {'FINISHED'}

    def execute_stopdaemons(self, context):
        """Stop control daemons on rendering nodes."""

        scene = context.scene
        props = scene.blendervr

        props.proc.kill()
        outs, errs = props.proc.communicate()
        print('subprocess killed, last words:')
        print(outs,errs)

        return {'FINISHED'}

    def execute_startplay(self, context):
        """Start playing scene on rendering nodes."""

         # get file path
        scene = context.scene
        props = scene.blendervr
        # tryout, start blenderplayer
        # bpy.ops.wm.blenderplayer_start()

        import subprocess
        args = ['python3', '/Users/AstrApple/WorkSpace/Blender_Workspace/addons/blendervr/source/blenderVR', 'controller']
        props.proc = subprocess.Popen(args,stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        print('opened',props.proc)

        # outs, errs = blendervr.proc.communicate(timeout=15)
        outs, errs = props.proc.communicate()
        print('first words: \n', outs,errs)

        return {'FINISHED'}

    def execute_stopplay(self, context):
        """Stop playing scene on rendering nodes."""

        scene = context.scene
        props = scene.blendervr



        return {'FINISHED'}

    def execute_debugwindow(self, context):
        """Open debugging window."""
        scene = context.scene
        props = scene.blendervr


        return {'FINISHED'}

# ======================================================================
def register():
    bpy.utils.register_class(BlenderVRConfigFileOperator)
    bpy.utils.register_class(BlenderVRSceneLoadOperator)
    bpy.utils.register_class(BlenderVRLaunchOperator)

def unregister():
    bpy.utils.register_class(BlenderVRLaunchOperator)
    bpy.utils.register_class(BlenderVRSceneLoadOperator)
    bpy.utils.register_class(BlenderVRConfigFileOperator)
