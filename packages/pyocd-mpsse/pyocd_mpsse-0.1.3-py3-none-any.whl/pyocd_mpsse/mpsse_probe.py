# PyOCD debug probe plugin for the MPSSE mode of FTDI chips
# Copyright (c) 2024 Andreas Fritiofson
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
from enum import Enum

import platform
import errno
import logging
from typing import List

from pyocd.probe.debug_probe import DebugProbe
from pyocd.probe.common import show_no_libusb_warning
from pyocd.core import exceptions
from pyocd.core.options import OptionInfo
from pyocd.core.plugin import Plugin
from pyocd.utility.mask import parity32_high

LOG = logging.getLogger(__name__)
#LOG.setLevel(logging.DEBUG)

POS_EDGE_OUT = 0x00
NEG_EDGE_OUT = 0x01
POS_EDGE_IN = 0x00
NEG_EDGE_IN = 0x04
MSB_FIRST = 0x00
LSB_FIRST = 0x08

DEFAULT_MODE = LSB_FIRST | POS_EDGE_IN | NEG_EDGE_OUT

class ChipType(Enum):
	FT2232C = 0,
	FT2232H = 1,
	FT4232H = 2,
	FT232H = 3,

class FtdiMPSSE(object):
	"""@brief Wrapper to handle MPSSE protocol engine and USB transfers.

	Exposes MPSSE command level functionality while hiding USB
	and protocol details.
	"""

	CLASS = 0xFF  # Vendor Specific

	RCV_HDR_LEN = 2  # Status header at beginning of every USB packet

	BUFFER_SIZE = 4096  # Size of buffers

	FTDI_DEVICE_OUT_REQTYPE = util.build_request_type(util.CTRL_OUT, util.CTRL_TYPE_VENDOR, util.CTRL_RECIPIENT_DEVICE)

	SIO_RESET_REQUEST             = 0x00
	SIO_SET_LATENCY_TIMER_REQUEST = 0x09
	SIO_SET_BITMODE_REQUEST       = 0x0B

	BITMODE_MPSSE = 0x02

	SIO_RESET_SIO = 0
	SIO_RESET_PURGE_RX = 1
	SIO_RESET_PURGE_TX = 2

	def __init__(self, dev):
		self._dev = dev
		self._probe_id = dev.serial_number or "Unknown Serial"
		self._vend = dev.manufacturer or "Unknown Manufacturer"
		self._prod = dev.product or "Unknown Product"
		# USB interface and endpoints, will be assigned in open()
		self._if = None
		self._wr_ep = None
		self._rd_ep = None
		self._type = None
		self._max_packet_size = None
		# Probe command queue
		self._queue = array("B")
		# Queue for endpoint read transactions
		self._read_length = 0
		self._read_queue = []


	def open(self, channel: int):
		# If we get here, the device should be accessible, and with a valid configuration
		# so, check for 'FTDIness'
		# Search the Vendor Specific interface in first configuration
		for i in self._dev[0]:
			if i.bInterfaceClass != FtdiMPSSE.CLASS:
				continue
			if i.bInterfaceNumber == channel:
				self._if = i
				break
		# Check for a missing device interface
		if self._if is None:
			raise exceptions.ProbeError()

		# Fix device busy error on WSL (Windows subsystem for linux)
		try:
			if (self._dev.is_kernel_driver_active(channel)):
				self._dev.detach_kernel_driver(channel)
		except core.USBError as e:
			raise exceptions.ProbeError("Could not detatch kernel driver from interface(%s): %s"%(channel, str(e)))
		except NotImplementedError:
			# Windows will cause not implemented error
			pass

		device_types = {
			0x500: ChipType.FT2232C,
			0x700: ChipType.FT2232H,
			0x800: ChipType.FT4232H,
			0x900: ChipType.FT232H
		}

		try:
			self._type = device_types[self._dev.bcdDevice]
		except(KeyError):
			raise exceptions.ProbeError("Unsupported FTDI chip type: 0x%04x"%self._dev.bcdDevice)

		LOG.debug("Detected FTDI %s", self._type)

		# Scan and assign Endpoints
		for e in self._if:
			if util.endpoint_direction(e.bEndpointAddress) == util.ENDPOINT_OUT:
				self._wr_ep = e
			else:
				self._rd_ep = e
				self._max_packet_size = e.wMaxPacketSize
		# Something is missing from this probe!
		if self._wr_ep is None or self._rd_ep is None:
			raise exceptions.ProbeError("Unrecognized FTDI interface")

		LOG.debug("open")

		self._dev.ctrl_transfer(self.FTDI_DEVICE_OUT_REQTYPE,
		                        self.SIO_RESET_REQUEST,
								self.SIO_RESET_SIO,
								channel + 1)

		self._dev.ctrl_transfer(self.FTDI_DEVICE_OUT_REQTYPE,
		                        self.SIO_SET_LATENCY_TIMER_REQUEST,
								255,
								channel + 1)

		self._dev.ctrl_transfer(self.FTDI_DEVICE_OUT_REQTYPE,
		                        self.SIO_SET_BITMODE_REQUEST,
		                        0x0b | (self.BITMODE_MPSSE << 8),
								channel + 1)
		self.purge()

	def close(self):
		# Reset cmd to port
		self._dev.ctrl_transfer(self.FTDI_DEVICE_OUT_REQTYPE,
		                        self.SIO_RESET_REQUEST,
								self.SIO_RESET_SIO,
								self._if.bInterfaceNumber + 1)
		# Clean tx and rx buffers
		self.purge()
	
		# Release interface
		self._dev._ctx.managed_release_interface(self._dev, self._if)
		
		# Reattach kernel driver
		try:
			self._dev.attach_kernel_driver(self._if.bInterfaceNumber)
		except (NotImplementedError, core.USBError):
			# Windows will cause not implemented error
			pass
		
		# Release device it self
		util.dispose_resources(self._dev)
		
		# Clean up other variables
		self._if = None
		self._wr_ep = None
		self._rd_ep = None

	@classmethod
	def enumerate_probes(cls, uid=None) -> List["FtdiMPSSE"]:
		"""@brief Find and return all MPSSE probes"""
		try:
			# Use a custom matcher to make sure the probe is an FTDI chip and accessible.
			return [
				FtdiMPSSE(probe)
				for probe in libusb_package.find(
					find_all=True, custom_match=FindMPSSEProbe(uid)
				)
			]
		except core.NoBackendError:
			show_no_libusb_warning()
			return []

	def _wq_space(self):
		return self.BUFFER_SIZE - len(self._queue) - 1 # Space for SEND_IMMEDIATE

	def _rq_space(self):
		return self.BUFFER_SIZE - self._read_length

	def _q_read_bytes(self, length):
		LOG.debug("queue read %s", length)
		self._read_length += length

	def _q_write_bytes(self, data):
		LOG.debug("queue write %s", data)
		if len(self._queue) + len(data) > self.BUFFER_SIZE:
			self.flush_queue()

		self._queue.extend(data)

	def is_high_speed(self):
		return self._type != ChipType.FT2232C

	def clock_data_out(self, out_data, length: int, mode: int = DEFAULT_MODE):
		mode |= 0x10
		data = out_data if type(out_data) is not int else out_data.to_bytes((length + 7) // 8, "little")
		out_offset = 0

		while length > 0:
			# Guarantee buffer space enough for a minimum size transfer
			if self._wq_space() + (length < 8) < 4:
				self.flush_queue()

			if length < 8:
				# Transfer remaining bits in bit mode
				self._q_write_bytes([0x02 | mode, length - 1])
				self._q_write_bytes(data[out_offset:out_offset+1])
				length = 0
			else:
				# Byte transfer
				this_bytes = length // 8
				# MPSSE command limit
				if (this_bytes > 65536):
					this_bytes = 65536
				# Buffer space limit. We already made sure there's space for the minimum transfer.
				if this_bytes + 3 > self._wq_space():
					this_bytes = self._wq_space() - 3

				if this_bytes > 0:
					self._q_write_bytes([mode, (this_bytes - 1) & 0xff, (this_bytes - 1) >> 8])
					self._q_write_bytes(data[out_offset:out_offset+this_bytes])
					out_offset += this_bytes
					length -= this_bytes * 8


	def clock_data_in(self, length: int, mode: int = DEFAULT_MODE):

		mode |= 0x20

		LOG.debug("clock_data_in %d bits", length)
		self._read_queue.append(length)

		while length > 0:
			# Guarantee buffer space enough for a minimum size transfer
			if self._wq_space() + (length < 8) < 3 or self._rq_space() < 1:
				self.flush_queue()

			if length < 8:
				# Transfer remaining bits in bit mode
				self._q_write_bytes([0x02 | mode, length - 1])
				self._q_read_bytes(1)
				length = 0
			else:
				# Byte transfer
				this_bytes = length // 8
				# MPSSE command limit
				if this_bytes > 65536:
					this_bytes = 65536
				# Buffer space limit. We already made sure there's space for the minimum transfer.
				if this_bytes > self._rq_space():
					this_bytes = self._rq_space()

				if this_bytes > 0:
					self._q_write_bytes([mode, (this_bytes - 1) & 0xff, (this_bytes - 1) >> 8])
					self._q_read_bytes(this_bytes)
					length -= this_bytes * 8

	def clock_tms_cs_out(self, out_data, out_offset: int, length: int, tdi: bool, mode: int = DEFAULT_MODE):
		pass

	def clock_tms_cs(self, out_data, out_offset: int, in_offset: int, length: int, tdi: bool, mode: int = DEFAULT_MODE):
		pass

	def set_data_bits_low_byte(self, data: int, dir: int):
		self._q_write_bytes([0x80, data, dir])

	def set_data_bits_high_byte(self, data: int, dir: int):
		self._q_write_bytes([0x82, data, dir])
		pass

	def read_data_bits_low_byte(self) -> int:
		pass

	def read_data_bits_high_byte(self) -> int:
		pass

	def loopback_config(self, enable: bool):
		pass

	def set_divisor(self, divisor: int):
		LOG.debug("Clock divisor: %d", divisor);
		self._q_write_bytes([0x86, divisor & 0xff, divisor >> 8])

	def divide_by_5_config(self, enable: bool) -> bool:
		if not self.is_high_speed():
			return False

		LOG.debug("Divide-by-5 %s", "on" if enable else "off")
		self._q_write_bytes([0x8b if enable else 0x8a])
		return True

	def rtck_config(self, enable: bool):
		if not self.is_high_speed():
			return False

		LOG.debug("RTCK %s", "on" if enable else "off")
		self._q_write_bytes([0x96 if enable else 0x97])
		return True

	def set_frequency(self, frequency: int) -> int:
		"""@brief Set the probe clock frequency"""
		LOG.debug("Target frequency %u", frequency)
		if frequency == 0:
			return self.rtck_config(True)

		self.rtck_config(False)

		if (frequency > (60000000 // 2 // 65536) and self.divide_by_5_config(False)):
			base_clock = 60000000
		else:
			self.divide_by_5_config(self, True)
			base_clock = 12000000

		divisor = (base_clock // 2 + frequency - 1) // frequency - 1;
		if divisor > 65535:
			divisor = 65535

		self.set_divisor(divisor)

		frequency = base_clock // 2 // (1 + divisor)
		LOG.debug("Actually %u Hz", frequency)

		return frequency

	def flush_queue(self):
		"""@brief Execute all the queued probe actions"""
		if self._read_length > 0:
			self._q_write_bytes([0x87])

		LOG.debug("flush %u bytes: %s", len(self._queue), self._queue)
		try:
			self._wr_ep.write(self._queue)
		except Exception:
			# Anything from the USB layer assumes probe is no longer connected
			raise exceptions.ProbeDisconnected("Cannot access probe " + self._probe_id)
		finally:
			# Make sure there are no leftovers
			self.start_queue()

	def purge(self):
		self.start_queue()
		self._read_length = 0
		self._read_queue = []
		self._dev.ctrl_transfer(self.FTDI_DEVICE_OUT_REQTYPE,
		                        self.SIO_RESET_REQUEST,
								self.SIO_RESET_PURGE_RX,
								self._if.bInterfaceNumber + 1)
		self._dev.ctrl_transfer(self.FTDI_DEVICE_OUT_REQTYPE,
		                        self.SIO_RESET_REQUEST,
								self.SIO_RESET_PURGE_TX,
								self._if.bInterfaceNumber + 1)

	def get_bits(self):
		"""@brief Execute all the queued probe actions and return read values"""
		self.flush_queue()
		LOG.debug("get_bits read %u bytes", self.BUFFER_SIZE)
		try:
			# TODO: Figure out how the read is terminated. Does FTDI always send a ZLP?
			# Or maybe we need to read exactly the expected size to avoid timeout if
			# it's a multiple of wMaxPacketSize.
			received = self._rd_ep.read(self.BUFFER_SIZE, timeout=10000)
		except Exception:
			# Anything from the USB layer assumes probe is no longer connected
			raise exceptions.ProbeDisconnected("Cannot access probe " + self._probe_id)

		LOG.debug("got %u bytes", len(received))
		# Check for correct length of received data
		remaining = self._read_length + self.RCV_HDR_LEN * (1 + self._read_length // (self._rd_ep.wMaxPacketSize - 2))
		if remaining != len(received):
			# Something went wrong, wrong number of bytes received
			self.purge()
			raise exceptions.ProbeError(
				"Mismatched header from %s: expected %u, received %u"
				% (self._probe_id, remaining, len(received))
			)

		data = [x for i,x in enumerate(received[:remaining]) if i % self._rd_ep.wMaxPacketSize >= 2]
		LOG.debug("read %s", data)

		result = []
		offset = 0

		for x in self._read_queue:
			value = 0
			length = (x + 7)//8
			if x % 8 > 0:
				data[offset+length-1] >>= (8 - x%8)
			value = int.from_bytes(data[offset:offset+length], 'little')
			offset += length

			result.append(value)

		self._read_length = 0
		self._read_queue = []

		LOG.debug("result: %s", result)
		return result

	def get_unique_id(self):
		return self._probe_id

	@property
	def vendor_name(self):
		return self._vend

	@property
	def product_name(self):
		return self._prod

	def start_queue(self):
		# Empty send queue and reset packet header
		del self._queue[:]


class FindMPSSEProbe(object):
	"""@brief Custom matcher to be used in core.find()"""
	SUPPORTED_VIDS_PIDS = [
		(0x403, 0x6010),  #FT2232C/D/L, FT2232HL/Q
		(0x403, 0x6011),  #FT4232HL/Q
		(0x403, 0x6014),  #FT232HL/Q
		(0x22B7, 0x150D), # Match for a isodebug 
	]

	def __init__(self, serial=None):
		"""@brief Create a new FindMPSSEprobe object with an optional serial number"""
		self._serial = serial

	def __call__(self, dev):
		"""@brief Return True if this is an FTDI device, False otherwise"""

		# Check if vid, pid and the device class are valid ones for an FTDI MPSSE probe.
		if (dev.idVendor, dev.idProduct) not in self.SUPPORTED_VIDS_PIDS:
			return False

		cfg = None
		# Make sure the device has an active configuration
		try:
			# This can fail on Linux if the configuration is already active.
			cfg = dev.get_active_configuration()
			
		except Exception:
			# But do no act on possible errors, they'll be caught in the next try: clause
			cfg = None

		try:
			# This raises when no configuration is set
			if cfg is None:
				dev.set_configuration()

			# Now read the serial. This will raise if there are access problems.
			serial = dev.serial_number

		except core.USBError as error:
			if error.errno == errno.EACCES and platform.system() == "Linux":
				msg = (
					"%s while trying to interrogate a USB device "
					"(VID=%04x PID=%04x). This can probably be remedied with a udev rule. "
					"See <https://github.com/pyocd/pyOCD/tree/master/udev> for help."
					% (error, dev.idVendor, dev.idProduct)
				)
				LOG.warning(msg)
			else:
				LOG.warning(
					"Error accessing USB device (VID=%04x PID=%04x): %s",
					dev.idVendor,
					dev.idProduct,
					error,
				)
			return False
		except (
			IndexError,
			NotImplementedError,
			ValueError,
			UnicodeDecodeError,
		) as error:
			LOG.debug(
				"Error accessing USB device (VID=%04x PID=%04x): %s",
				dev.idVendor,
				dev.idProduct,
				error,
			)
			return False

		# Check the passed serial number
		if self._serial is not None:
			if self._serial == "" and serial is None:
				return True
			if self._serial != serial:
				return False
		LOG.debug("open device")
		return True


class MPSSEProbe(DebugProbe):
	"""@brief Wraps a FtdiMPSSE link as a DebugProbe."""

	# Address of read buffer register in DP.
	RDBUFF = 0xC

	# SWD command format
	SWD_CMD_START = 1 << 0  # always set
	SWD_CMD_APnDP = 1 << 1  # set only for AP access
	SWD_CMD_RnW = 1 << 2  # set only for read access
	SWD_CMD_A32 = 3 << 3  # bits A[3:2] of register addr
	SWD_CMD_PARITY = 1 << 5  # parity of APnDP|RnW|A32
	SWD_CMD_STOP = 0 << 6  # always clear for synch SWD
	SWD_CMD_PARK = 1 << 7  # driven high by host

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
		ACK_WAIT: exceptions.TransferTimeoutError("MPSSEProbe: ACK WAIT received"),
		ACK_FAULT: exceptions.TransferFaultError("MPSSEProbe: ACK FAULT received"),
		ACK_ALL: exceptions.TransferError("MPSSEProbe: Protocol fault"),
	}

	GPIO_INIT = "ftdi.gpio_init_mask"
	GPIO_DIR = "ftdi.gpio_dir_mask"
	SRST = "ftdi.srst_mask"
	SWDIO_OE = "ftdi.swdio_oe_mask"
	SWD_EN = "ftdi.swd_en_mask"
	JTAG_EN = "ftdi.jtag_en_mask"
	CHANNEL_OPTION = "ftdi.channel"

	PARITY_BIT = 0x100000000

	@classmethod
	def get_all_connected_probes(cls, unique_id=None, is_explicit=False):
		return [cls(dev) for dev in FtdiMPSSE.enumerate_probes()]

	@classmethod
	def get_probe_with_id(cls, unique_id, is_explicit=False):
		probes = FtdiMPSSE.enumerate_probes(unique_id)
		if probes:
			return cls(probes[0])

	def __init__(self, FtdiMPSSE: FtdiMPSSE):
		super(MPSSEProbe, self).__init__()
		self._link = FtdiMPSSE
		self._is_connected = False
		self._is_open = False
		self._unique_id = self._link.get_unique_id()
		self._reset = False

	@property
	def description(self):
		return self.vendor_name + " " + self.product_name

	@property
	def vendor_name(self):
		return self._link.vendor_name

	@property
	def product_name(self):
		return self._link.product_name

	@property
	def supported_wire_protocols(self):
		return [DebugProbe.Protocol.DEFAULT, DebugProbe.Protocol.SWD]

	@property
	def unique_id(self):
		return self._unique_id

	@property
	def wire_protocol(self):
		"""@brief Only valid after connecting."""
		return DebugProbe.Protocol.SWD if self._is_connected else None

	@property
	def is_open(self):
		return self._is_open

	@property
	def capabilities(self):
		return {DebugProbe.Capability.SWJ_SEQUENCE, DebugProbe.Capability.SWD_SEQUENCE}

	def open(self):
		self._link.open(self.session.options.get(self.CHANNEL_OPTION))
		self._output = self.session.options.get(self.GPIO_INIT)
		self._direction = self.session.options.get(self.GPIO_DIR)
		self._link.set_data_bits_low_byte(self._output & 0xFF, self._direction & 0xFF)
		self._link.set_data_bits_high_byte(self._output >> 8, self._direction >> 8)
		self._link.flush_queue()
		self._is_open = True

	def close(self):
		# reset gpio to initial state before closing
		self._output = self.session.options.get(self.GPIO_INIT)
		self._direction = self.session.options.get(self.GPIO_DIR)
		self._link.set_data_bits_low_byte(self._output & 0xFF, self._direction & 0xFF)
		self._link.set_data_bits_high_byte(self._output >> 8, self._direction >> 8)
		self._link.flush_queue()
		
		self._link.close()
		self._is_open = False

	def connect(self, protocol=None):
		"""@brief Connect to the target via SWD."""
		LOG.debug("connect proto %s", protocol)
		# Make sure the protocol is supported
		if (protocol is None) or (protocol == DebugProbe.Protocol.DEFAULT):
			protocol = DebugProbe.Protocol.SWD

		# Validate selected protocol.
		if protocol != DebugProbe.Protocol.SWD:
			raise ValueError("unsupported wire protocol %s" % protocol)

		self._is_connected = True
		self.read_ap_multiple = self._safe_read_ap_multiple
		self.write_ap_multiple = self._safe_write_ap_multiple
		self._swd_en(True)
		self._swd_swdio_en(True)

	def swj_sequence(self, length, bits):
		LOG.debug("swj_sequence: %u, %s", length, bits)
		self._swd_swdio_en(True)
		self._link.clock_data_out(bits, length)

	def swd_sequence(self, sequences):
		"""@brief Send a sequences of bits on the SWDIO signal.

		Each sequence in the _sequences_ parameter is a tuple with 1 or 2 members in this order:
		- 0: int: number of TCK cycles from 1-64
		- 1: int: the SWDIO bit values to transfer. The presence of this tuple member indicates the sequence is
			an output sequence; the absence means that the specified number of TCK cycles of SWDIO data will be
			read and returned.

		@param self
		@param sequences A sequence of sequence description tuples as described above.

		@return A 2-tuple of the response status, and a sequence of bytes objects, one for each input
			sequence. The length of the bytes object is (<TCK-count> + 7) / 8. Bits are in LSB first order.
		"""
		LOG.debug("swd_sequence: %s", sequences)
		# Init lengths to pack and cmd queue
		reads_lengths = []
		self._link.start_queue()
		# Take each sequence 'seq' in sequences
		for seq in sequences:
			if len(seq) == 1:
				bits = seq[0]
				self._link.q_read_bits(bits)
				reads_lengths.append((bits + 7) // 8)
			elif len(seq) == 2:
				self._link.q_write_bits(seq[1], seq[0])
			else:
				# Ignore malformed entry, raise or return failure? Ignore for the moment.
				pass
		# Check if some read were queued
		if len(reads_lengths) == 0:
			# Just execute the queue
			self._link.flush_queue()
			return (0,)
		else:
			reads = self._link.get_bits()
			# Is there a status definition, no check in caller?
			return (0, [v.to_bytes(l, "little") for v, l in zip(reads, reads_lengths)])

	def disconnect(self):
		self._is_connected = False

	def set_clock(self, frequency):
		self._link.set_frequency(int(frequency))

	def reset(self):
		LOG.debug("reset")
		self.assert_reset(True)
		sleep(self.session.options.get("reset.hold_time"))
		self.assert_reset(False)
		sleep(self.session.options.get("reset.post_delay"))

	def assert_reset(self, asserted):
		LOG.debug("reset %u", asserted)
		self._set_reset(asserted)
		self._link.flush_queue()
		self._reset = asserted

	def is_reset_asserted(self):
		# No support for reading back the current state
		return self._reset

	def read_dp(self, addr, now=True):
		LOG.debug("read dp %x", addr)
		val = self._read_reg(addr, self.DP)

		# Return the result or the result callback for deferred reads
		def read_dp_result_callback():

			return val

		return val if now else read_dp_result_callback

	def write_dp(self, addr, value):
		LOG.debug("write dp %x=%08x", addr, value)
		self._write_reg(addr, self.DP, value)

	def read_ap(self, addr, now=True):
		LOG.debug("read ap %x", addr)
		(ret,) = self.read_ap_multiple(addr)

		def read_ap_cb():
			return ret

		return ret if now else read_ap_cb

	def write_ap(self, addr, value):
		LOG.debug("write ap %x=%08x", addr, value)
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

	def set_signal(self, set_mask, clear_mask):
		output = (self._output | set_mask) & ~clear_mask
		#LOG.debug("set output %04x dir %04x, set %04x, clear %04x", output, self._direction, set_mask, clear_mask)
		if output & 0xFF != self._output & 0xFF:
			self._link.set_data_bits_low_byte(output & 0xFF, self._direction & 0xFF)
		if output >> 8 != self._output >> 8:
			self._link.set_data_bits_high_byte(output >> 8, self._direction >> 8)
		self._output = output

	def _swd_en(self, enable: bool):
		LOG.debug("SWD %s", "enable" if enable else "disable")
		mask = self.session.options.get(self.SWD_EN)
		if mask != 0:
			self.set_signal(mask if enable else 0, 0 if enable else mask)

	def _swd_swdio_en(self, enable: bool):
		LOG.debug("SWDIO %s", "enable" if enable else "disable")
		mask = self.session.options.get(self.SWDIO_OE)
		if mask != 0:
			self.set_signal(mask if enable else 0, 0 if enable else mask)

	def _set_reset(self, enable: bool):
		mask = self.session.options.get(self.SRST)
		if mask != 0:
			self.set_signal(0 if enable else mask, mask if enable else 0)

	def _read_reg(self, addr, APnDP):
		LOG.debug("read reg")
		# This is a safe read
		# Send a command with a read AP/DP request
		self._swd_command(self.READ, APnDP, addr)
		try:
			self._read_check_swd_ack()
		except (exceptions.TransferFaultError, exceptions.TransferTimeoutError) as e:
			#in case ACK indicates error during read we need to clock one more time to transfare back bus controll to FTDI
			self._swd_swdio_en(False)
			self._link.clock_data_in(1) # on error need to clean up bus
			self._link.get_bits() #consume any remaining data
			raise e #rethrow exeption

		# Read + 32 (data) + 1 (parity) + 1 (Trn) bits
		self._swd_swdio_en(False)
		self._link.clock_data_in(32 + 1 + 1)
		# insert idle
		self._swd_swdio_en(True)
		self._link.clock_data_out(0, 3)

		reg = self._link.get_bits()[0]
		# Unpack the returned value
		val = reg & 0xFFFFFFFF
		# Remove the Trn bit
		par = reg & self.PARITY_BIT
		# Check for correct parity value
		if par != parity32_high(val):
			raise exceptions.ProbeError("Bad parity in SWD read")

		LOG.debug("result = %08x", val)
		return val

	def _write_reg(self, addr, APnDP, value):
		LOG.debug("write_reg")
		# Send a command with a write AP/DP request
		self._swd_command(self.WRITE, APnDP, addr)
		self._read_check_swd_ack()

		# Prepare the write buffer
		value |= parity32_high(value)

		# Send the value: 32 (data) + 1 (parity) bits (no Trn needed)
		# Insert also 3 bits of idle
		self._swd_swdio_en(True)
		self._link.clock_data_out(value, 32 + 1 + 3)
		self._link.flush_queue()

	def _swd_command(self, RnW, APnDP, addr):
		"""@brief Builds and queues an SWD command byte plus an ACK read"""
		cmd = (APnDP << 1) + (RnW << 2) + ((addr << 1) & self.SWD_CMD_A32)
		cmd |= parity32_high(cmd) >> (32 - 5)
		cmd |= self.SWD_CMD_START | self.SWD_CMD_STOP | self.SWD_CMD_PARK

		# Write the command to the probe
		self._swd_swdio_en(True)
		self._link.clock_data_out(cmd, 8)
		# Queue also ACK reading, plus TrN if needed
		self._swd_swdio_en(False)
		self._link.clock_data_in(1 + 3 + 1 - RnW)

	def _read_check_swd_ack(self):
		# Reads Trn + ACK, plus a following Trn bit if the cmd was a write
		ack = self._link.get_bits()
		self._check_swd_acks(ack)

	def _check_swd_acks(self, raw_acks):
		# Extract ACKs and collapse identical elements
		acks = set((ack >> 1) & self.ACK_ALL for ack in raw_acks)
		LOG.debug("acks: %s", acks)

		# Remove ACK OK only if present
		acks.difference_update({self.ACK_OK})

		# If there's something left, we had a problem.
		if len(acks) == 0:
			return
		else:
			try:
				# Raise the exception for the first problem found in set.
				e = self.ACK_EXCEPTIONS[acks.pop()]
			except KeyError:
				e = self.ACK_EXCEPTIONS[self.ACK_ALL]
			raise e


class MPSSEProbePlugin(Plugin):
	"""@brief Plugin class for FTDI MPSSE probes."""

	def load(self):
		return MPSSEProbe

	@property
	def name(self):
		return "mpsse"

	@property
	def description(self):
		return "FTDI MPSSE Probe"

	@property
	def options(self):
		"""@brief Returns FTDI MPSSE probe options."""
		return [
			OptionInfo(
				MPSSEProbe.CHANNEL_OPTION,
				int,
				0,
				"FTDI channel.",
			),
			OptionInfo(
				MPSSEProbe.GPIO_INIT,
				int,
				0x07f8,
				"GPIO initial output bitmask.",
			),
			OptionInfo(
				MPSSEProbe.GPIO_DIR,
				int,
				0xfffb,
				"GPIO initial direction bitmask.",
			),
			OptionInfo(
				MPSSEProbe.SWDIO_OE,
				int,
				0x0008,
				"SWDIO output enable pin bitmask.",
			),
			OptionInfo(
				MPSSEProbe.SRST,
				int,
				0x0400,
				"SRST bitmask.",
			),
			OptionInfo(
				MPSSEProbe.SWD_EN,
				int,
				0x1800,
				"SWD enable bitmask.",
			),
			OptionInfo(
				MPSSEProbe.JTAG_EN,
				int,
				0x0800,
				"JTAG enable bitmask.",
			),
		]
