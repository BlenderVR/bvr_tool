# -*- coding: utf-8 -*-
# file: bvr/bvrconfig.py

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

"""Access to the XML configuration file of VR systems.

This is a layer on top of 
"""

import logging
logger = logging.getLogger(__name__)

# For blendervr usage of Configure's parent when it is a module…
_logger = logging.getLogger("blendervr-console")

# Load our environment settings (include standard config access path).
from . import (
    RUNTIME,
    bvrenv,
    bvrprops,
    )

# To debug this module.
DEBUG = True and not RUNTIME


# We rely on core BlenderVR configuration management, as it deal with
# special extensions to XML to allow some Python parts execution when
# building configuration values.
from blendervr.console.xml import Configure


def load_configuration(config_paths, config_file):
    """Return a blendervr Configure object corresponding to configuration file.

    :param config_file: bas XML configuration file.
    :type config_file: string
    :param config_paths: directories where other configuration file must be searched.
    :type config_paths: string
    :rtype: blendervr.console.xml.Configure
    :return: configuration object
    """
    # What is 'parent' (thanks to the NO documentation)
    # In the configuration object MainBase inherited class, parent can be a
    # MainBase or a module.
    # Dont know its usage (except that it use the _logger attribute), so
    # use this module as parent.
    parent = sys.modules[__name__]

    cfg = Config(parent, config_paths, config_file)

    return cfg

