# -*- coding: utf-8 -*-
# file: bvr/bvrenv.py

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

"""Manage BlenderVR environment.

This module prepare the environment for using BlenderVR console,
it setup globals to reference ad-hoc directories (preferences/config
location, installation path for blendervr, etc), install global names 
in Python builtins, and adjust python path to access blendervr package.
"""

import os
import sys
from os import path as osp
import functools
import builtins     # Important: we modify builtins to add our stuff!
import logging
logger = logging.getLogger(__name__)

# Note: this module is Blender and blendervr agnostic!

from . import (
    RUNTIME,
    )

# To debug this module.
DEBUG = True and not RUNTIME

# Constants.
CONFIG_FILENAME = "profile_1.1.ini"

# Enable out logging debug.
if not RUNTIME:
    logging.basicConfig(filename=osp.join(osp.expanduser('~'), 'bvr_logs.txt'),
                        filemode="w",   # Ensure overwrite the log file.
                        level=logging.DEBUG)

# Globals (ajusted in setup_environment())
user_config_dir = ""
blendervr_config_dir = ""
blendervr_config_file = ""

def setup_environment():
    """Prepare the environment to work with blendervr console.
    
    This setup some files and directories, adjust the Python PATH of
    current process to make blendervr importable, and inject requested
    blendervr magic names into builtins.
    """
    global user_config_dir
    global blendervr_config_dir
    global blendervr_config_file

    package_dir = osp.dirname(osp.abspath(__file__))

    # --- Find root of config directory for the system.
    if 'XDG_CONFIG_HOME' in os.environ:
        user_config_dir = os.environ['XDG_CONFIG_HOME']
    elif sys.platform.startswith('win'):
        user_config_dir = osp.join(os.environ['APPDATA'])
    elif sys.platform == 'darwin':
        user_config_dir = osp.join(osp.expanduser('~'), 'Library',
                                            'Application Support')
    elif sys.platform == 'linux':
        user_config_dir = osp.join(osp.expanduser('~'), ".config")
    else:
        user_config_dir = osp.join(osp.expanduser('~'), ".config")
    logger.debug("user_config_dir: %s", user_config_dir)
    # Use a subdirectory blender/vr.
    blendervr_config_dir = osp.join(user_config_dir, "blender", "vr")
    logger.debug("blendervr_config_dir: %s", blendervr_config_dir)
    if not osp.isdir(blendervr_config_dir):         # Ensure it exists.
        os.makedirs(blendervr_config_dir)

    # Currently we use a fixed configuration file name.
    blendervr_config_file = osp.join(blendervr_config_dir, CONFIG_FILENAME)

    # Ensure we have a modules/ subdirectory in preferences, make it available to blendervr.
    # TODO: rename modules_dir to pofiles_dir ?
    modules_dir = os.path.join(blendervr_config_dir, "modules")
    if not osp.isdir(modules_dir): 
        os.makedirs(modules_dir)
    # /!\ Inject BlenderVR_profilePath in builtins
    builtins.BlenderVR_profilePath = modules_dir

    # TODO: (or not) retrieve root path from command-line… from configuration file.
    root_dir = osp.join(package_dir, "source")
    blendervr_dir = osp.join(root_dir, "modules")
    # /!\ Inject BlenderVR_root in builtins
    builtins.BlenderVR_root = root_dir

    # Allow to import and use blendervr package.
    if blendervr_dir not in sys.path:
        sys.path.append(blendervr_dir)


if 'BVR_LOADER_CREATION' in os.environ:
    logger.info("Running as loader creation.")

# This is called immediatly to benefit from globals values in our
# Blender objects definitions.
setup_environment()
