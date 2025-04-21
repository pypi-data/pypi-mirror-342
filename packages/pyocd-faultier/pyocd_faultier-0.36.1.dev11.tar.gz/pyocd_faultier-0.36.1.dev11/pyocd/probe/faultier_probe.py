# pyOCD debugger
# Copyright (c) 2021 Federico Zuccardi Merli
# Copyright (c) 2021 Chris Reed
# Copyright (c) 2025 Thomas 'stacksmashing' Roth
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from array import array

from time import sleep
from usb import core, util
import libusb_package

import platform
import errno
import logging
from typing import List

from .debug_probe import DebugProbe
from .common import show_no_libusb_warning
from ..core import exceptions
from ..core.options import OptionInfo
from ..core.plugin import Plugin
from ..utility.mask import parity32_high

LOG = logging.getLogger(__name__)

import struct


TAMARIN_INVALID      = 0
TAMARIN_READ = 1
TAMARIN_WRITE = 2
TAMARIN_LINE_RESET = 3
TAMARIN_SET_FREQ = 4
TAMARIN_RESET = 5

class FaulLink(object):
    """@brief Wrapper to handle Faultier USB.

    Just to hide details of USB and Faultier command layer
    """

    CLASS = 0xFF    # Vendor Specific

    CMD_HDR_LEN = 6  # do not include pico packet header
    PKT_HDR_LEN = 4  # pico packet header
    HDR_LEN = PKT_HDR_LEN + CMD_HDR_LEN

    PROBE_INVALID = 0       # Invalid command
    PROBE_WRITE_BITS = 2    # Host wants us to write bits
    PROBE_READ_BITS = 1     # Host wants us to read bits
    PROBE_SET_FREQ = 4      # Set TCK
    PROBE_RESET = 5         # Reset all state: it's a no-op!
    PROBE_TARGET_RESET = 3  # Reset target (Hardware nreset)

    BUFFER_SIZE = 1024      # Size of buffers in the Faultier

    def __init__(self, dev):
        self._dev = dev
        self._probe_id = dev.serial_number
        self._vend = dev.manufacturer
        self._prod = dev.product
        # USB interface and endpoints, will be assigned in open()
        self._if = None
        self._wr_ep = None
        self._rd_ep = None
        # Progressive command id
        self._id = 0
        # Probe command queue
        self._queue = array('B', (0, 0, 0, 0))
        self._qulen = self.PKT_HDR_LEN
        # Buffer for endpoint reads
        self._bits = array('B', (0 for _ in range(self.BUFFER_SIZE)))

    # ------------------------------------------- #
    #          Faultier Access functions
    # ------------------------------------------- #
    def open(self):
        # On Faultier, the second interface (interface 1) is the picoprobe interface
        for i in self._dev[0]:
            if i.bInterfaceNumber == 1:
                self._if = i
                break
        # Check for a missing device interface
        if self._if is None:
            raise exceptions.ProbeError()
        # Scan and assign Endpoints
        for e in self._if:
            if util.endpoint_direction(e.bEndpointAddress) == util.ENDPOINT_OUT:
                self._wr_ep = e
            else:
                self._rd_ep = e
        # Something is missing from this probe!
        if self._wr_ep is None or self._rd_ep is None:
            raise exceptions.ProbeError("Unrecognized Faultier interface")

    def close(self):
        self._if = None
        self._wr_ep = None
        self._rd_ep = None

    @classmethod
    def enumerate_Faultiers(cls, uid=None) -> List["FaulLink"]:
        """@brief Find and return all Faultiers """
        try:
            # Use a custom matcher to make sure the probe is a Faultier and accessible.
            return [FaulLink(probe) for probe in libusb_package.find(find_all=True, custom_match=FindFaultier(uid))]
        except core.NoBackendError:
            show_no_libusb_warning()
            return []

    def set_swd_frequency(self, f):
        LOG.debug("Setting of SWD frequency currently ignored.")
        # self.start_queue()
        # # Write a packet with SET_FREQ and the new value, bypass the queue
        # self._queue_cmd_header(self.PROBE_SET_FREQ, f)
        # self.flush_queue()

    def assert_target_reset(self, state):
        self.start_queue()
        # Write a packet with PROBE_TARGET_RESET and the reset pin state
        self._queue_cmd_header(self.PROBE_TARGET_RESET, state)
        self.flush_queue()

    def get_unique_id(self):
        return self._probe_id

    @property
    def vendor_name(self):
        return self._vend

    @property
    def product_name(self):
        return self._prod

    # ------------------------------------------- #
    #          Faultier intenal functions
    # ------------------------------------------- #
    def _next_id(self):
        """@brief Returns a progressive id for a Faultier command"""
        id = self._id
        self._id = (self._id + 1) % 0x100
        return id

class FindFaultier(object):
    """@brief Custom matcher for Faultier to be used in core.find() """

    VID_PID_CLASS = (0x37de, 0xfffe, 0x0)  # Match for a Faultier

    def __init__(self, serial=None):
        """@brief Create a new FindFaultier object with an optional serial number"""
        self._serial = serial

    def __call__(self, dev):
        """@brief Return True if this is a Faultier device, False otherwise"""

        if (dev.idVendor, dev.idProduct, dev.bDeviceClass) != self.VID_PID_CLASS:
            return False
        # print("MATCHING")

        # Make sure the device has an active configuration
        try:
            # This can fail on Linux if the configuration is already active.
            dev.set_configuration()
        except Exception:
            # But do no act on possible errors, they'll be caught in the next try: clause
            pass

        try:
            # This raises when no configuration is set
            dev.get_active_configuration()

            # Now read the serial. This will raise if there are access problems.
            serial = dev.serial_number

        except core.USBError as error:
            if error.errno == errno.EACCES and platform.system() == "Linux":
                msg = ("%s while trying to interrogate a USB device "
                       "(VID=%04x PID=%04x). This can probably be remedied with a udev rule. "
                       "See <https://github.com/pyocd/pyOCD/tree/master/udev> for help." %
                       (error, dev.idVendor, dev.idProduct))
                LOG.warning(msg)
            else:
                LOG.warning("Error accessing USB device (VID=%04x PID=%04x): %s",
                            dev.idVendor, dev.idProduct, error)
            return False
        except (IndexError, NotImplementedError, ValueError, UnicodeDecodeError) as error:
            LOG.debug("Error accessing USB device (VID=%04x PID=%04x): %s",
                      dev.idVendor, dev.idProduct, error)
            return False

        # Check the passed serial number
        if self._serial is not None:
            # Faultier serial will be "123456" (older FW) or an actual unique serial from the flash.
            if self._serial == "" and serial is None:
                return True
            if self._serial != serial:
                return False
        return True


class FaultierProbe(DebugProbe):
    """@brief Wraps a FaulLink link as a DebugProbe. """

    # Address of read buffer register in DP.
    RDBUFF = 0xC

    # Bitmasks for AP/DP register address field.
    A32 = 0x0000000c

    # SWD command format
    SWD_CMD_START = (1 << 0)    # always set
    SWD_CMD_APnDP = (1 << 1)    # set only for AP access
    SWD_CMD_RnW = (1 << 2)      # set only for read access
    SWD_CMD_A32 = (3 << 3)      # bits A[3:2] of register addr
    SWD_CMD_PARITY = (1 << 5)   # parity of APnDP|RnW|A32
    SWD_CMD_STOP = (0 << 6)     # always clear for synch SWD
    SWD_CMD_PARK = (1 << 7)     # driven high by host

    tamarin_queue = []

    # APnDP constants.
    DP = 0
    AP = 1

    # Read and write constants.
    READ = 1
    WRITE = 0

    # ACK values
    ACK_OK = 0b001
    ACK_WAIT = 0b010
    ACK_FAULT = 0b100
    ACK_ALL = ACK_FAULT | ACK_WAIT | ACK_OK

    ACK_EXCEPTIONS = {
        ACK_OK: None,
        ACK_WAIT: exceptions.TransferTimeoutError("Faultier: ACK WAIT received"),
        ACK_FAULT: exceptions.TransferFaultError("Faultier: ACK FAULT received"),
        ACK_ALL: exceptions.TransferError("Faultier: Protocol fault"),
    }

    SAFESWD_OPTION = 'FaultierProbe.safeswd'

    PARITY_BIT = 0x100000000

    @ classmethod
    def get_all_connected_probes(cls, unique_id=None, is_explicit=False):
        return [cls(dev) for dev in FaulLink.enumerate_Faultiers()]

    @ classmethod
    def get_probe_with_id(cls, unique_id, is_explicit=False):
        probes = FaulLink.enumerate_Faultiers(unique_id)
        if probes:
            return cls(probes[0])

    def __init__(self, FaulLink):
        super(FaultierProbe, self).__init__()
        self._link = FaulLink
        self._is_connected = False
        self._is_open = False
        self._unique_id = self._link.get_unique_id()
        self._reset = False

    @ property
    def description(self):
        return self.vendor_name + " " + self.product_name

    @ property
    def vendor_name(self):
        return self._link.vendor_name

    @ property
    def product_name(self):
        return self._link.product_name

    @ property
    def supported_wire_protocols(self):
        return [DebugProbe.Protocol.DEFAULT, DebugProbe.Protocol.SWD]

    @ property
    def unique_id(self):
        return self._unique_id

    @ property
    def wire_protocol(self):
        """@brief Only valid after connecting."""
        return DebugProbe.Protocol.SWD if self._is_connected else None

    @ property
    def is_open(self):
        return self._is_open

    @ property
    def capabilities(self):
        return {DebugProbe.Capability.SWJ_SEQUENCE, DebugProbe.Capability.SWD_SEQUENCE}

    def open(self):
        self._link.open()
        self._is_open = True

    def close(self):
        self._link.close()
        self._is_open = False

    # ------------------------------------------- #
    #          Target control functions
    # ------------------------------------------- #
    def connect(self, protocol=None):
        """@brief Connect to the target via SWD."""
        # Make sure the protocol is supported
        if (protocol is None) or (protocol == DebugProbe.Protocol.DEFAULT):
            protocol = DebugProbe.Protocol.SWD

        # Validate selected protocol.
        if protocol != DebugProbe.Protocol.SWD:
            raise ValueError("unsupported wire protocol %s" % protocol)

        self._is_connected = True
        # Use the bulk or safe read and write functions according to option
        self.read_ap_multiple = self._safe_read_ap_multiple
        self.write_ap_multiple = self._safe_write_ap_multiple
        # Do I need to do anything else here?
        # SWJ switch sequence is handled externally...

    def swj_sequence(self, length, bits):
        # This also performs the SWJ sequence
        tamarin_cmd = self._create_tamarin_cmd_hdr(0, TAMARIN_LINE_RESET, 0, 0, 0)
        
        self.tamarin_queue.append(tamarin_cmd)
        self._link._wr_ep.write(tamarin_cmd)
        # We do a read and ignore the result
        self._link._rd_ep.read(6)
        return

    def swd_sequence(self, sequences):
        LOG.debug("SWD sequence currently ignored.")

    def disconnect(self):
        self._is_connected = False

    def set_clock(self, frequency):
        self._link.set_swd_frequency(int(frequency) // 1000)

    def reset(self):
        LOG.debug("RESET currently ignored.")
        return
        self.assert_reset(True)
        sleep(self.session.options.get('reset.hold_time'))
        self.assert_reset(False)
        sleep(self.session.options.get('reset.post_delay'))

    def assert_reset(self, asserted):
        self._link.assert_target_reset(asserted)
        self._reset = asserted

    def is_reset_asserted(self):
        # No support for reading back the current state
        return self._reset

    # ------------------------------------------- #
    #          DAP Access functions
    # ------------------------------------------- #
    def read_dp(self, addr, now=True):
        val = self._read_reg(addr, self.DP)

        # Return the result or the result callback for deferred reads
        def read_dp_result_callback():

            return val
        return val if now else read_dp_result_callback

    def write_dp(self, addr, value):
        self._write_reg(addr, self.DP, value)

    def read_ap(self, addr, now=True):
        (ret,) = self.read_ap_multiple(addr)

        def read_ap_cb():
            return ret
        return ret if now else read_ap_cb

    def write_ap(self, addr, value):
        self.write_ap_multiple(addr, (value,))

    def _safe_read_ap_multiple(self, addr, count=1, now=True):
        # Send a read request for the AP, discard the stale result
        self._read_reg(addr, self.AP)
        # Read count - 1 new values
        results = [self._read_reg(addr, self.AP) for n in range(count - 1)]
        # and read the last result from the RDBUFF register
        results.append(self.read_dp(self.RDBUFF))

        def read_ap_multiple_result_callback():
            return results

        return results if now else read_ap_multiple_result_callback

    def _safe_write_ap_multiple(self, addr, values):
        # Send repeated read request for the AP
        for v in values:
            self._write_reg(addr, self.AP, v)

    # ------------------------------------------- #
    #          Internal implementation functions
    # ------------------------------------------- #

    def _read_reg(self, addr, APnDP):
        command_byte = self._swd_command_byte(self.READ, APnDP, addr)
        tamarin_cmd = self._create_tamarin_cmd_hdr(0, TAMARIN_READ, command_byte, 0, 0)
        
        self.tamarin_queue.append(tamarin_cmd)
        self._link._wr_ep.write(tamarin_cmd)
        received = self._link._rd_ep.read(6)
        result = struct.unpack("<BBI", received)
        # TODO: Check result
        return result[2]

    def _write_reg(self, addr, APnDP, value):
        # print(f"write {hex(addr)} {APnDP}  {hex(value)}")
        command_byte = self._swd_command_byte(self.WRITE, APnDP, addr)
        # print(f"command byte {command_byte}")
        tamarin_cmd = self._create_tamarin_cmd_hdr(0, TAMARIN_WRITE, command_byte, value, 16)
        # print(f"write reg Tamarin cmd {tamarin_cmd}")
        self.tamarin_queue.append(tamarin_cmd)
        self._link._wr_ep.write(tamarin_cmd)
        received = self._link._rd_ep.read(6)
        result = struct.unpack("<BBI", received)
        # TODO: Check result

    def _swd_command_byte(self, RnW, APnDP, addr):
        cmd = (APnDP << 1) + (RnW << 2) + ((addr << 1) & self.SWD_CMD_A32)
        cmd |= parity32_high(cmd) >> (32 - 5)
        # Equal to | 0x81 
        cmd |= self.SWD_CMD_START | self.SWD_CMD_STOP | self.SWD_CMD_PARK
        return cmd

    def _change_options(self, notification):
        # Only this option, ATM
        if notification.event == self.SAFESWD_OPTION:
            if notification.data.new_value:
                self.read_ap_multiple = self._safe_read_ap_multiple
                self.write_ap_multiple = self._safe_write_ap_multiple
            else:
                self.read_ap_multiple = self._bulk_read_ap_multiple
                self.write_ap_multiple = self._bulk_write_ap_multiple

    def _create_tamarin_cmd_hdr(self, id=0, cmd=0, request=0, data=0, idle_cycles=0):
        """
        Create a tamarin_cmd_hdr structure as defined in the C struct.
        
        Args:
            id (int): Currently unused field (uint8_t)
            cmd (int): One of TAMARIN_CMDS (uint8_t)
            request (int): The full SWD command (uint8_t)
            data (int): The data for writes (uint32_t)
            idle_cycles (int): Number of idle cycles to perform after this op (uint8_t)
        
        Returns:
            bytes: Packed binary representation of the tamarin_cmd_hdr structure
        """
        # Format string explanation:
        # B = unsigned char (uint8_t)
        # I = unsigned int (uint32_t)
        # < = little-endian byte order
        format_string = '<BBBIB'
        
        # Pack the structure according to the defined format
        packed_struct = struct.pack(format_string, 
                                id & 0xFF,          # uint8_t
                                cmd & 0xFF,         # uint8_t
                                request & 0xFF,     # uint8_t
                                data & 0xFFFFFFFF,  # uint32_t
                                idle_cycles & 0xFF) # uint8_t
        
        return packed_struct


class FaultierPlugin(Plugin):
    """@brief Plugin class for Faultier."""

    def load(self):
        return FaultierProbe

    @ property
    def name(self):
        return "Faultier"

    @ property
    def description(self):
        return "stacksmashing's Faultier"

    @ property
    def options(self):
        """@brief Returns Faultier options."""
        return [
            OptionInfo(FaultierProbe.SAFESWD_OPTION, bool, True,
                       "Use safe but slower SWD transfer functions with Faultier.")]
