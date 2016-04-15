# -*- coding: utf-8 -*-
# file: bvr/bvrprops.py

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

"""Storage of BlenderVR variables within Blender properties.
"""

# ===== Normal module imports.
# Load needed standard modules.
import os
import sys
from os import path as osp
import functools
import builtins     # Important: we modify builtins to add our stuff!
import logging
logger = logging.getLogger(__name__)

# Load necessary stuff from blender.
import bpy

#from bpy.props import (
#        StringProperty,
#        EnumProperty,
#        PointerProperty,
#        BoolProperty
#        )
#from bpy.types import (
#        PropertyGroup

# Load our environment settings (include standard config access path).
from . import (
    RUNTIME,
    bvrenv,
    bvrprefs,
    )

# To debug this module.
DEBUG = True and not RUNTIME

# TODO: If necessary, setup a generic callback for properties update, allowing to
# install handlers at late time (unless Blender has API for that), to manage
# GUI control updates.
# def propupdt_callback(propname, self, context):
# And use with:
# xxx = bpy.props.YYYProperty(…, update=functools.partial(propupdt_callback, propname=xxx))


# Manage properties update handlers via functions which can be bound at late time.
# This allow us to have ui/operators code initialized after props code and keep light
# coupling between both.
update_handlers = {}

def generic_update(propname, self, context):
    """Handle an update of a BlenderVRProps property.
    """
    if propname in update_handlers:
        update_handlers[propname](self, context)


# We tried to use functools.partial, but get the blender error:
# TypeError: update keyword: expected a function type, not a functools.partial
# So build ad-hoc on-demand functions with closure.
def make_update(name):
    """Create an update handler function associated to a widget name for late dispatch.
    """
    def specific_update(self, context):
        """Call generic update handler function with captured widget name.
        """
        generic_update(name, self, context)
    return specific_update


def register_update_handler(propname, handler):
    """Register a handler function for a BlenderVRProps property.

    The handler must be a callable with two parameters: self, context.
    """
    update_handlers[propname] = handler


# Keep a reference to returned string.
# 1) dont rebuild it if unnecessary.
# 2) see doc: «There is a known bug with using a callback, Python must keep 
#    a reference to the strings returned or Blender will crash.»
# Contains: [(identifier, name, description, icon, number), ...] 
# See
# https://www.blender.org/api/blender_python_api_2_77_release/bpy.props.html#bpy.props.EnumProperty
current_screens = [ 
    ('console', 'console', ""),
    ('split', 'split', "") ]

def screens_lister(self, context):
    """Retrieve screens from current XML configuration.
    """
    global current_screens
    if True:
        return current_screens


class BlenderVRProps(bpy.types.PropertyGroup):
    """properties for a BlenderVR blender's extension.
    
    We use:
        config_file_path
        screen_setup
        blend_scene_file_path
        processor_file_path
    """
    
    # Following properties are saved to and loaded from preferences file
    config_file_path = bpy.props.StringProperty(
        name="BlenderVR Configuration File Path",
        description="Path to the .xml configuration file describing physical VR installation.",
        default=osp.join(bvrenv.blendervr_config_dir, "main_pers1.1.xml"),
        maxlen=1024, subtype="FILE_PATH",
        update=make_update('config_file_path')
        )
    screen_setup = bpy.props.EnumProperty(
        name="Screens architecture",
        description="VR architecture screens setup within the choosen installation.",
        items=screens_lister,
        default=None,
        update=make_update('config_file_path')
        )
    blend_scene_file_path = bpy.props.StringProperty(
        name="Blender Scene File Path",
        description="Path to the blend scene to be rendered in the VR system.",
        default="//", 
        maxlen=1024, subtype="FILE_PATH",
        update=make_update('config_file_path')
        )
    processor_file_path = bpy.props.StringProperty(
        name="Processor File Path",
        description="Path to the processor file used for RV scene interaction logic.",
        default="//", 
        maxlen=1024, subtype="FILE_PATH",
        update=make_update('config_file_path')
        )
    use_name_link = bpy.props.BoolProperty(
        name="Use Name Link",
        description="Use <blend file>.processor.py by corresponding name.",
        default=False, 
        subtype="NONE",
        options={'HIDDEN'},
        update=make_update('config_file_path')
        )
    auto_open_logs = bpy.props.BoolProperty(
        name="Auto open logs",
        description="Automatically open log windows trigged on errors detection.",
        default=False, 
        subtype="NONE",
        update=make_update('config_file_path')
        )

    # Following properties are used for GUI interaction.
    status_daemons_started = bpy.props.BoolProperty(
        name="Daemons Started",
        description="Memorise status of daemons as started.",
        default=False, 
        subtype="NONE",
        options={'HIDDEN'},
        update=make_update('status_daemons_started')
        )

    status_valid_config_file = bpy.props.BoolProperty(
        name="Valid Configuration File",
        description="Memorise status of configuration file validity.",
        default=False, 
        subtype="NONE",
        options={'HIDDEN'},
        update=make_update('status_valid_config_file')
        )

    status_valid_display = bpy.props.BoolProperty(
        name="Valid Selection of Display System Parameters",
        description="Memorise status of validity of display system.",
        default=False, 
        subtype="NONE",
        options={'HIDDEN'},
        update=make_update('status_valid_display')
        )

    # Following properties are used at BlenderVR running time for feedback.



# See:
#https://www.blender.org/api/blender_python_api_2_62_0/bpy.app.handlers.html
@bpy.app.handlers.persistent    # Stay running across multilpe files.
def scene_load_post_handler(scene):
    """Load prefs content from ini file when the scene is loaded.

    This make use of latest configuration when loading a scene.
    """
    # ? dont know why, but scene is… None, so use bpy.context one.
    props = bpy.context.scene.blendervr
    bvrprefs.load_prefs(bvrenv.blendervr_config_file, props)


@bpy.app.handlers.persistent    # Stay running across multilpe files.
def scene_save_post_handler(scene):
    """Save prefs content to ini file when scene is saved.

    This save latest configuration to be used when loading another scene.
    """
    # ? dont know why, but scene is… None, so use bpy.context one.
    #props = bpy.context.scene.blendervr
    #bvrprefs.save_prefs(props, bvrenv.blendervr_config_file)


# ======================================================================
def register():
    """Register classes/handlers of this submodule."""
    if DEBUG:
        logger.debug("Registering bvr.bvrprops classes and app handlers.")

    bpy.utils.register_class(BlenderVRProps)

    # Register this tool properties object in blender Scene type.
    bpy.types.Scene.blendervr = bpy.props.PointerProperty(type=BlenderVRProps)

    bpy.app.handlers.load_post.append(scene_load_post_handler)
    bpy.app.handlers.save_post.append(scene_save_post_handler)

def unregister():
    """Unregister classes/handlers of this submodule."""
    if DEBUG:
        logger.debug("Unregistering bvr.bvrprops classes and app handlers.")

    bpy.app.handlers.load_post.remove(scene_load_post_handler)
    bpy.app.handlers.save_post.remove(scene_save_post_handler)

    bpy.utils.unregister_class(BlenderVRProps)


