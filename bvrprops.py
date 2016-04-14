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
        bvrenv,
        )


DEBUG = True

# TODO: If necessary, setup a generic callback for properties update, allowing to
# install handlers at late time (unless Blender has API for that), to manage
# GUI control updates.
# def propupdt_callback(propname, self, context):
# And use with:
# xxx = bpy.props.YYYProperty(…, update=functools.partial(propupdt_callback, propname=xxx))

class BlenderVRProps(bpy.types.PropertyGroup):
    """properties for a BlenderVR blender's extension.
    
    We use:
        config_file_path
        screen_setup
        blend_scene_file_path
        processor_file_path
    """
    
    # Following properties are saved and loaded from configuration file
    config_file_path = bpy.props.StringProperty(
        name="BlenderVR Configuration File Path",
        description="Path to the .xml configuration file describing physical VR installation.",
        default=osp.join(bvrenv.blendervr_config_dir, "main_pers1.1.xml"),
        maxlen=1024, subtype="FILE_PATH",
        )
    screen_setup = bpy.props.EnumProperty(
        name="Screens architecture",
        description="VR architecture screens setup within the choosen installation.",
        items=(('console_debug', "Console Debug", ""),
                ('dk2_debug', "DK2 Debug", "")),
        default='console_debug',
        )
    blend_scene_file_path = bpy.props.StringProperty(
        name="Blender Scene File Path",
        description="Path to the blend scene to be rendered in the VR system.",
        default="//", 
        maxlen=1024, subtype="FILE_PATH",
        )
    processor_file_path = bpy.props.StringProperty(
        name="Processor File Path",
        description="Path to the processor file used for RV scene interaction logic.",
        default="//", 
        maxlen=1024, subtype="FILE_PATH",
        )
    use_name_link = bpy.props.BoolProperty(
        name="Use Name Link",
        description="Use <blend file>.processor.py by corresponding name.",
        default=False, 
        subtype="NONE",
        options={'HIDDEN'},
        )
    auto_open_logs = bpy.props.BoolProperty(
        name="Auto open logs",
        description="Automatically open log windows trigged on errors detection.",
        default=False, 
        subtype="NONE",
        )

    # Following properties are used for GUI interaction.
    
    
    # Following properties are used at BlenderVR running time for feedback.
    


# ======================================================================
def register():
    """Register classes of this submodule."""
    bpy.utils.register_class(BlenderVRProps)

    print(dir(BlenderVRProps.auto_open_logs))

def unregister():
    """Unregister classes of this submodule."""
    bpy.utils.unregister_class(BlenderVRProps)

