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
import socket
import select
from collections import namedtuple
import logging
logger = logging.getLogger(__name__)

from . import (
    RUNTIME,
    bvrenv,         # Import first ! it setup our execution environment.
    )

# Note: as bvr is imported, normally package import of blender DONT start
# their main() functions - this may 

from blendervr.tools import connector
from blendervr.tools import protocol
from blendervr.console.base import ConsoleBase
from blendervr.console.logic.console import ConsoleLogic
from blendervr.console import profile
from blendervr.tools import logger as blendervr_logger
from blendervr.console import screens
from blendervr.plugins import getPlugins
from blendervr import plugins   # Needed by xml parsing code.


A VOIR
#comment les plugins sont utilisés par le loader XML et est-ce qu'il
#retrouve ses petits pour être capable de libre le fichier dans son ensemble?



# To debug this module.
DEBUG = True and not RUNTIME

# Communication protocol transmit the message length in a header of this size:
SIZE_LEN = connector.Common.SIZE_LEN
# And the buffer for read is defined here:
BUFFER_LEN = connector.Common.BUFFER_LEN


# For blendervr usage of Configure's parent when it is a module…
_logger = logging.getLogger("BlenderVR")
# For blendervr usage of _profile parent when it is a module…
# Late bind in BVRConsoleControler construction.
_profile = None

# Storage of items for socket listen/read management.
SocketCallback = namedtuple('SocketCallback', "socket_, callback, data")

# Storage of pending data when reading messages.
PendingRead = namedtuple('PendingRead', "remain_size, data")

# This module is based on blendervr.console.console module, adapted to
# our blender tool context.
# In our usage, it is the _main_running_module for bendervr objects.
# getConsole() and getMainRunningModule() return this module.
class BVRConsoleControler(ConsoleBase, ConsoleLogic):
    """Interface to logic part of console code.

    :ivar socket_listeners: filenos of sockets to listen.
    :type socket_listeners: [int]
    :ivar listeners_callbacks: map of fileno to socket management items.
    :type listeners_callbacks: [int: SocketCallback]
    """
    def __init__(self, profile_file):
        global _profile

        self.socket_listeners = []
        self.listeners_callbacks = {}
        self.pending_read = {}

        # Following attributes are managed by ConsoleLogic:
        #   _possibleScreenSets = None
        #   _anchor = None
        #   _previous_state = None
        #   _common_processors = []
        # TODO: some attributes are not set in the constructor but
        # in load_configuration_file() method, so they may NOT be set if
        # there is an error in the 
        # And are "automagically" used by GUI.
        self._blender_file = None
        self._loader_file = None
        self._processor_files = None
        self._processor = None
        self._update_loader_script = "/".join((BlenderVR_root, 'utils',
                                                    'update_loader.py'))
        self._profile = profile.Profile(profile_file)
        # Bind to module global for blendervr to find it.
        _profile = self._profile
        self._logger = blendervr_logger.getLogger('BlenderVR')

        # In the blendervr class system, the parent can be another object
        # or a module.
        # Note: this is the object returned as 
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


    def display_screen_sets(self, possibleScreenSets):
        # TODO: feed current_screens in bvrprops 
        print("possibleScreenSets:", repr(possibleScreenSets)) 
        pass

    # ==================== ADAPTED GUI METHODS ========================
    # Method called from logic to activate GUI code.
    def addListenTo(self, socket_, callback, data=None):
        """Add a socket listener to notify a callable when some data is ready to read.

        :param socket_: network socket object to monitor for reading.
        :type socket_: socket.Socket
        :return: a tag data used to remove socket monitoring (the socket fileno).
        :rtype: int
        """
        # Note: blendervr/console/logic/screen.py has been modified to transmit
        # a Socket object and not its fileno in case of usage with bvr package.

        # Store socket and memorize its callback.
        socknum = socket_.fileno()
        if socknum not in self.socket_listeners:
            self.socket_listeners.append(socknum)
        else:
            raise RuntimeError("Socket used more than once")
        self.listeners_callbacks[socknum] =  SocketCallback(socket_, callback, data)
        return socknum  # Enough to manage late removing

    def removeListenTo(self, tag):
        """Remove a socket listener.
        """
        if tag not in self.listeners_callbacks:
            self.logger.error("Unknown fileno %r to un-listen socket.", tag)
            return
        del self.listeners_callbacks[tag]
        self.socket_listeners.remove(tag)


    # ==================== NETWORK SOCKET MONITORING ========================
    def nonblocking_read(self):
        """Management of sockets read and message processing in an event loop context.
        """
        #TODO: Move all possible code to a background working thread, and just manage
        # communication of some events between that thread and the blender event loop.
        # May have one thread per socket to listen (and work with blocking select).
        if not self.socket_listeners:
            #self.logger.debug("No socket active")
            return
        # As we work in a blender event loop, dont block on sockets (timeout=0)
        rready, _, _ = select.select(
                        self.socket_listeners, 
                        [],
                        [],
                        0)

        if not rready:
            #self.logger.debug("No socket ready")
            return

        for socknum in rready:
            self.logger.debug("Socket operations…")
            rawdata = None  # In case of error.
            cb = self.listeners_callbacks[socknum]
            # Detect if we are beginning to read a message or reading next
            # parts of a previous message read.
            begin_message = socknum not in self.pending_read
            if begin_message:
                readsize = SIZE_LEN
            else:
                readsize = self.pending_read[socknum].remain_size

            rawdata = cb.socket_.recv(readsize)

            if begin_message:
                # Retrieved message size.
                if readsize == len(rawdata):
                    messagesize = int(rawdata)
                    self.pending_read[socknum] = PendingRead(messagesize, "")
                else:
                    # We fail to retrieve the message length!
                    # What to do ???? Maybe we are unsynchronized on some
                    # datagram.
                    # We retrieve pending data, hoping to cleanup the socket.
                    cb.socket_.recv(BUFFER_LEN)
                    pass
            else:
                # Retrieve data (or part of data).
                remain_size = self.pending_read[socknum].remain_size - len(rawdata)
                rawdata = self.pending_read[socknum].data + rawdata
                if remain_size > 0:
                    self.pending_read[socknum] = PendingRead(remain_size, "")
                else:
                    # Have a complete message, process it.
                    del self.pending_read[socknum] 
                    try:
                        message_parts = protocol.decomposeMessage(rawdata)
                        self.logger.debug("Received message %r", message_parts)
                        cd.callback(*message_parts)
                    except:
                        self.logger.exception("Exception in message processing %r", rawdata)

