# -*- coding: utf-8 -*-
# file: bvr/bvrprefs.py

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

"""Manage preference files read and write.

Preference read and write is splitted from BlenderVR properties, as
it dont save all properties needed at BlenderVR runtime console control.

For the xml configuration file read, see bvrconfig module.
"""

#TODO: Manage different prefs presets, with save as/select/remove? actions,
# creating ad-hoc sections in the .INI file (and have a "latest_prefs"
# key indicating what prefs to reload at startup).

import configparser
import logging
logger = logging.getLogger(__name__)


# Load our environment settings (include standard config access path).
from . import (
    RUNTIME,
    bvrenv,
    bvrprops,
    )

# To debug this module.
DEBUG = True and not RUNTIME

CONSOLE_SECTION = 'CONSOLE'

LOGGERNAME = "console"

# Note: if use another type than str or bool, update load/save functions.
PROPITEMS = [ ('profile_file', str, ""),
              ('config_file_path', str, ""),
              ('screen_setup', str, ""),
              ('blend_scene_file_path', str, ""),
              ('processor_file_path', str, ""),
              ('use_name_link', bool, False),
              ('auto_open_logs', bool, False),
            ]


def save_prefs(propertiesgroup, filepath):
    """Save the prefs part of a BlenderVRProps in a file."""
    logger.info("Saving prefs to %s", filepath)
    # Proceed in 3 steps to ensure to keep user comments in the file.
    # Step 1) load config content
    try:
        config = configparser.ConfigParser()
        config.read(filepath)
    except IOError as e:
        logger.exception("Error loading file %s", filepath)
        raise

    # Step 2) modify keys/values
    if not config.has_section(CONSOLE_SECTION):
        config.add_section(CONSOLE_SECTION)
    for p, t, d in PROPITEMS:   # Property, type, default
        if t is str:
            v = getattr(propertiesgroup, p)
        elif t is bool:
            v = config.get(CONSOLE_SECTION, p)
            v = repr(getattr(propertiesgroup, p))
        else:
            logger.error("Data type %s not supported.", t)
            raise RuntimeError("Unknown config data type.")
        config.set(CONSOLE_SECTION, p, v)

    # Step 3) write content
    try:
        with open(filepath, "w", encoding="utf8") as f:
            config.write(f)
    except IOError as e:
        logger.exception("Error writing file %s", filepath)
        raise


def load_prefs(filepath, propertiesgroup):
    """Load prefs from a file and update attributes in a BlenderVRProps."""
    logger.info("Loading prefs from %s", filepath)

    try:
        config = configparser.ConfigParser()
        config.read(filepath)
    except IOError as e:
        # Start from a clean empty config.
        config = configparser.ConfigParser()

    if not config.has_section(CONSOLE_SECTION):
        config.add_section(CONSOLE_SECTION)

    for p, t, d in PROPITEMS:   # Property, type, default
        if not config.has_option(CONSOLE_SECTION, p):
            v = d
        elif t is str:
            v = config.get(CONSOLE_SECTION, p)
        elif t is bool:
            v = config.getboolean(CONSOLE_SECTION, p)
        else:
            logger.error("Unknown config data type %s.", t)
            raise RuntimeError("Unknown config data type {}.".format(t))
        setattr(propertiesgroup, p, v)
        logger.info("Pref %s set to %r", p, v)
