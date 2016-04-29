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

from os import path as osp
import logging
logger = logging.getLogger(__name__)

import bpy
from bpy.types import Operator

from . import (
    RUNTIME,
    bvrconsole,
    bvrprops,
    )

# To debug this module.
DEBUG = True and not RUNTIME


console = None


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
        elif act :
            self.report({'ERROR'}, 'action "{}" (in configfile) not defined yet'.format(act))
            return {'CANCELLED'}


    def execute_new(self, context):
        """Create a new VR system configuration file from scene description.
        """
        # TODO…
        self.report({'ERROR'}, 'currently unimplemented')
        return {'CANCELLED'}
        # cleanup before we start
        # bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}

    def execute_load(self, context):
        """Load console 
        """
        global console

        scene = context.scene
        props = scene.blendervr

        pickle_profile = osp.abspath(props.profile_file)
        xml_config = osp.abspath(props.config_file_path)
        
        if console is None:
            console = bvrconsole.BVRConsoleControler(pickle_profile)
            console.start()

        # Load XML configuration.
        logger.info("Loading XML VR device configuration file %s", xml_config)
        console.profile.setValue(['config', 'file'], xml_config)
        props.status_loaded_config_file = console.load_configuration_file()

        if not props.status_loaded_config_file:
            self.report({'ERROR'}, 'VR system configuration file load fail.')
            return {'CANCELLED'}

        print(console._screenSets.items())

        # TODO: setup screen sets.
        bvrprops.current_screens.clear()

        currentScreenSet = console.profile.getValue(['screen', 'set'])
        possibleScreenSets = list(OrderedDict(sorted(console._screenSets.items())).keys())

        self.report({'INFO'}, 'VR system configuration file loaded.')

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


class BlenderVRLaunchOperator(Operator):
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
            self.report({'ERROR'}, 'action "{}" (in launcher) not defined yet'.format(act))
            return {'CANCELLED'}

    def execute_startdaemons(self, context):
        """Start control daemons on rendering nodes."""
        global console

        scene = context.scene
        props = scene.blendervr

        logger.info("Starting daemons")

        if console is None:
            self.report({'ERROR'}, 'canot start daemons without a console')
            return {'CANCELLED'}

        console.profile.setValue(['screen', 'set'], props.screen_setup)
        console.profile.setValue(['files', 'blender'], props.blend_scene_file_path)
        console.profile.setValue(['files', 'processor'], props.processor_file_path)

        console.start_simulation()

        props.status_daemons_started = True
        return {'FINISHED'}

    def execute_stopdaemons(self, context):
        """Stop control daemons on rendering nodes."""
        scene = context.scene
        props = scene.blendervr

        logger.info("Stopping daemons")

        console.stop_simulation()

        props.status_daemons_started = False
        return {'FINISHED'}

    def execute_startplay(self, context):
        """Start playing scene on rendering nodes."""
        scene = context.scene
        props = scene.blendervr

        logger.info("Starting players")

        return {'FINISHED'}

    def execute_stopplay(self, context):
        """Stop playing scene on rendering nodes."""
        scene = context.scene
        props = scene.blendervr

        logger.info("Stopping players")

        return {'FINISHED'}

    def execute_debugwindow(self, context):
        """Open debugging window."""
        scene = context.scene
        props = scene.blendervr


        return {'FINISHED'}


# Following handler function is installed in scene_update_pre app handlers
# to have idle code running in blender general event loop.
@bpy.app.handlers.persistent
def idle_tasks(context):
    """Method called periodically by blender in its event loop.

    Manage background tasks for the Console management (mainly communication
    for UI status update and logs display).
    """
    import time
    #print("Called", time.time(), context)
    if console is not None:
        # Call idle processing code of console. 
        try:
            console.nonblocking_read()
        except:
            logger.exception("Exception in console.nonblocking_read")


# ======================================================================
def register():
    if DEBUG:
        logger.debug("Registering bvr.bvroperators classes.")
    bpy.utils.register_class(BlenderVRConfigFileOperator)
    bpy.utils.register_class(BlenderVRSceneLoadOperator)
    bpy.utils.register_class(BlenderVRLaunchOperator)

    bpy.app.handlers.scene_update_pre.append(idle_tasks) 

def unregister():
    if DEBUG:
        logger.debug("Unregistering bvr.bvroperators classes.")
    bpy.app.handlers.scene_update_pre.remove(idle_tasks)

    bpy.utils.register_class(BlenderVRLaunchOperator)
    bpy.utils.register_class(BlenderVRSceneLoadOperator)
    bpy.utils.register_class(BlenderVRConfigFileOperator)
