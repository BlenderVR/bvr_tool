# -*- coding: utf-8 -*-
# file: bvr/operator.py

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

"""Manage settings file read and write and internal settings object.

Where this object is stored within Blender objects, where the file is
stored in the file system are managed by callers.
"""

# ===== Normal module imports.
# Load needed standard modules.
import os
from os import path as osp
import functools

# Load our environment settings (include standard config access path).
from . import (
        bvrenv,
        bvrprops,
        )


# TODO: Save configuration as some readable .INI file
def save_config(varsconfig, filepath):
    """Save a configuration part of a BlenderVRVars in a file."""
    # TODO
    # 1) load config content
    # 2) modify keys/values
    # 3) write content
    # This to ensure to keep user comments in the file.
    try:
        with open(filepath, 'wb') as cfgfile:
            pickle.dump(node, cfgfile)
    except IOError as e:
        print('Configuration save error:', filepath, e)


def load_config(filepath, varsconfig):
    """Load a configuration from a file and update attributes in a BlenderVRVars."""
    try:
        with open(filepath, 'rb') as cfgfile:
            config = pickle.load(cfgfile)
            if DEBUG:
                print("Consoleuration:")
                pprint.pprint(consoleuration)
        return config
    except IOError as e:
        print('Configuration load error:', filepath, e)

