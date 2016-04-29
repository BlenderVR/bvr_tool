# -*- coding: utf-8 -*-
# file: bvr/__init__.py

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

"""Blender tool to manage BlenderVR directly within Blender GUI.

This tool replace the BlenderVR console by a Blender Tool, removing
Qt / PySide dependancy, and making smooth integration with the 
modeling / animation / rendering software.

As it is started within a Blender GUI context, it duplicate necessary
initialisation code from original blendervr console script.
"""

# To disable DEBUG in all modules - this must be first, to be defined when
# bvr components import top module names.
RUNTIME = False

# To debug this module.
DEBUG = True and not RUNTIME

# Meta-data describe the tool for Blender tools GUI (provide informations, links
# for help, versions, etc).
bl_info = {
    "name": "BlenderVR",
    "author": "David Poirier-Quinot, Laurent Pointal",
    "version": (0, 2),
    "blender": (2, 7, 7),
    "location": "3D View > Toolbox",
    "description": "A collection of tools to configure and control your BlenderVR environment.",
    "warning": "",
    'tracker_url': 'https://github.com/BlenderVR/source/issues',
    "wiki_url": "http://blendervr.limsi.fr",
    'support': 'TESTING',
    "category": "Game Engine"
    }

# ===== Normal module imports.
# Load needed standard modules.
import os
from os import path as osp
import imp
import sys
import builtins     # Important: we modify builtins to add our stuff!
import pickle
import pprint
import logging
logger = logging.getLogger(__name__)

if 'BVR_LOADER_CREATION' not in os.environ:
    # Load necessary stuff from blender.
    import bpy

    # Load our package management
    from . import (
        bvrenv,         # Import first ! it setup our execution environment.
        bvrprops,
        bvrprefs,
        bvroperators,
        bvrui,
        bvrconsole,
        bvrconfig,
        )


# ======================================================================
def register():
    """Register the Blender GUI tools, and setup for BlenderVR console."""
    if 'BVR_LOADER_CREATION' not in os.environ:
        # Register classes of our submodules.
        bvrprops.register()
        bvroperators.register()
        bvrui.register()


def unregister():
    """Unregister the Blender GUI tools, and remove BlenderVR console stuff."""
    if 'BVR_LOADER_CREATION' not in os.environ:
        # Unregister classes of our submodules.
        bvrui.unregister()
        bvroperators.unregister()
        bvrprops.unregister()
