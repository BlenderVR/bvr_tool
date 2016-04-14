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

from . import (
    bvrenv,         # Import first ! it setup our execution environment.
    )

# Note: as bvr is imported, normally package import of blender DONT start
# the 
from blendervr.tools import connector
from blendervr.tools import protocol


DEBUG = True


class BVRDaemonManager:
    """Control a (remote/local) BlenderVR daemon.
    
    :ivar callbacks: map of callable for some events related to daemons.
    :type callbacks: {str:[func]}
    """
    def __init__(self):
        self.callbacks = {}

    def register_callback(self, events, callback):
        """Install a callback for a set of events.
        """
        for e in events:
            self.callbacks.setdefault(e, []).append(callback)

    def reset_callbacks(self):
        # We use Python reference counting to "loose" all callbacks.
        # Else must go throught keys, and cleanup lists before removing them…
        self.callbacks = {}


class BVRLogCatcher:
    """Listen for BlenderVR daemons logs.
    
    Central logs Used to:
    1) 
    """
    def __init__(self):
        pass
