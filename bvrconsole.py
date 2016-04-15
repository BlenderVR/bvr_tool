# -*- coding: utf-8 -*-
# file: bvr/bvrconsole.py

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

"""Management of BlenderVR Console functionnalities without GUI.

The tools here provide possible callbacks for some GUI interaction,
but
"""

import os
import sys
from os import path as osp
import functools
import builtins     # Important: we modify builtins to add our stuff!
import logging
logger = logging.getLogger(__name__)

from . import (
    RUNTIME,
    bvrenv,         # Import first ! it setup our execution environment.
    )

# Note: as bvr is imported, normally package import of blender DONT start
# their main() functions - this may 

#from blendervr.tools import connector
#from blendervr.tools import protocol
from blendervr.console.base import ConsoleBase
from blendervr.console.logic.console import ConsoleLogic
from blendervr.console import profile
from blendervr.tools import logger as blendervr_logger
from blendervr.console import screens
from blendervr.plugins import getPlugins

# To debug this module.
DEBUG = True and not RUNTIME


# This module is based on blendervr.console.console module, adapted to
# our blender tool context.
class BVRConsoleControler(ConsoleBase, ConsoleLogic):
    """Interface to initial (Qt based) console code.
    
    """
    def __init__(self):
        self._blender_file = None
        self._loader_file = None
        self._processor_files = None
        self._processor = None
        self._update_loader_script = "/".join((BlenderVR_root, 'utils',
                                                    'update_loader.py'))
        self._profile = profile.Profile(profile_file)
        self._logger = blendervr_logger.getLogger('BlenderVR')

        # In the blendervr class system, the parent can be another object
        # or a module.
        parent = sys.modules[__name__]
        ConsoleBase.__init__(self, parent)
        ConsoleLogic.__init__(self)

        self._screens = screens.Screens(self)
        self._plugins = getPlugins(self, self._logger)

        self.profile.setDefault({'config': {'file': '',
                                            'path': []},
                                 'files': {'blender': '',
                                            'processor': '',
                                            'link': True},
                                 'screens': {'display': False},
                                 'window': {'geometry': [0, 0, 0, 0]},
                                 'processor': {'toggle': True}})


    @property
    def profile(self):
        return self._profile

    @property
    def logger(self):
        return self._logger

    @property
    def plugins(self):
        return self._plugins

    # 
    def display_screen_sets(self, possibleScreenSets):
        # TODO: feed current_screens in bvrprops 
        print("possibleScreenSets:", repr(possibleScreenSets)) 
        pass
