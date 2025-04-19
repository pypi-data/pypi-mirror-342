import trio
import struct

from toolz.curried import pipe, map, filter, reduceby, concat
from typing import Optional
from trio import move_on_after, MemorySendChannel, MemoryReceiveChannel
from trio.socket import socket, SOCK_RAW

from abc import abstractmethod

from oxitrait.trait import Trait
from oxitrait.impl import Impl
from oxitrait.struct import Struct
from oxitrait.enum import Enum, auto
from oxitrait.runtime import requires_traits

from result import Result, Ok, Err

from pyritex import logger
from pyritex.netlink.consts import *
from pyritex.netlink.rtnl.consts import *
from pyritex.netlink.message import NetlinkHeaderTrait

class NetlinkSyncContextTrait(metaclass=Trait):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

class NetlinkAsyncContextTrait(metaclass=Trait):
    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

class NetlinkSocketTrait(metaclass=Trait):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __post_init__(self):
        pass

    @abstractmethod
    async def initialize(self, nursery: trio.Nursery) -> Result[None, str]:
        """
        Open/bind the socket, spawn any needed background tasks.
        """
        pass

    @abstractmethod
    async def send_message(self, message: NetlinkHeaderTrait) -> Result[None, str]:
        """
        Serialize and send a netlink message.
        """
        pass

    @abstractmethod
    async def receive_message(self, timeout: float = 5.0) -> Result[NetlinkHeaderTrait, str]:
        """
        Retrieve one netlink message from the buffer (populated by a background task).
        """
        pass

    @abstractmethod
    async def close(self) -> Result[None, str]:
        """
        Cancel any background tasks and close the underlying socket.
        """
        pass

#
# 2) Provide the Implementation for that Trait
#
class ImplNetlinkSocket(NetlinkSocketTrait, metaclass=Impl, target="NetlinkSocket"):
    """
    Implementation for the NetlinkSocket struct.
    """

    def __init__(self, protocol = 0, socket = None):
        self.protocol = protocol
        self.socket = socket
        if not self.inbound_send or not self.inbound_recv:
            send_chan, recv_chan = trio.open_memory_channel[NetlinkHeaderTrait](max_buffer_size=100)
            self.inbound_send = send_chan
            self.inbound_recv = recv_chan
        if not self._message_buffer:
            self._message_buffer: dict[int, list[bytes]] = {}

    def __post_init__(self):
        """
        Called after the Struct is created. Here we can set up a memory channel
        for inbound messages.
        """
        if not self.inbound_send or not self.inbound_recv:
            send_chan, recv_chan = trio.open_memory_channel[NetlinkHeaderTrait](max_buffer_size=100)
            self.inbound_send = send_chan
            self.inbound_recv = recv_chan
        if not self._message_buffer:
            self._message_buffer: dict[int, list[bytes]] = {}

    async def initialize(self, nursery: trio.Nursery) -> Result[None, str]:
        """
        Initialize the netlink socket, then spawn _read_loop in the given nursery.
        The caller is responsible for providing an open nursery, which remains
        alive until we want to shut down.
        """
        logger.trace("Entering initialize()")
        if self.sock is not None:
            # Already initialized
            return Ok(None)

        try:
            # Create the raw netlink socket
            self.sock = trio.socket.socket(AF_NETLINK, SOCK_RAW, self.protocol)
            # Typical netlink bind: (nl_pid=0 => auto-assign, nl_groups=0 => no groups)
            await self.sock.bind((0, 0))

            self._running = True
            logger.debug(f"Is self running in initialize? Answer: {self._running}")

            # Store the provided nursery for later cancellation/cleanup
            self.nursery = nursery
            # Spawn the background read loop in the provided nursery
            nursery.start_soon(self._read_loop)
            logger.trace("Exiting initialize()")

            return Ok(None)

        except Exception as e:
            return Err(f"Failed to initialize socket: {e}")

    def _handle_message(self, message: dict):
        """
        Routes a parsed Netlink message to the appropriate handler.
        """
        msg_type = message["type"]

        if msg_type == 24:  # RTM_GETROUTE
            self._handle_route_message(message)

        elif msg_type == 16:  # RTM_NEWLINK (Interface update)
            self._handle_link_message(message)

        else:
            logger.warning(f"Unhandled Netlink message type: {msg_type}")


    def _parse_full_message(self, raw_data: bytes) -> Result[dict, str]:
        """
        Parses a full Netlink message from raw bytes.

        Returns:
            Ok(parsed_data) on success, or Err(error_msg) on failure.
        """
        logger.trace("Entering _parse_full_message()")

        try:
            # Parse Netlink header
            nlmsg_len, nlmsg_type, nlmsg_flags, nlmsg_seq, nlmsg_pid = struct.unpack_from(NLMSG_HDR_FORMAT, raw_data)

            # Extract payload (skipping header)
            payload = raw_data[16:]  # Netlink header is 16 bytes

            parsed_data = {
                "len": nlmsg_len,
                "type": nlmsg_type,
                "flags": nlmsg_flags,
                "seq": nlmsg_seq,
                "pid": nlmsg_pid,
                "payload": payload,
            }

            logger.debug(f"Parsed full Netlink message: {parsed_data}")
            return Ok(parsed_data)

        except Exception as e:
            return Err(f"Parsing failed: {e}")

    async def _dispatch(self, full_message: list[bytes]):
        """
        Handles a fully received Netlink message sequence.

        This function:
          - Combines message fragments into one structure
          - Parses it
          - Pushes the full parsed message into the inbound channel
        """
        if not full_message:
            logger.warning("_dispatch() called with empty message buffer!")
            return

        # Concatenate all message fragments
        raw_data = b"".join(full_message)

        # Attempt to parse the full message
        result = self._parse_full_message(raw_data)
        if result.is_err():
            logger.error(f"Failed to parse Netlink message: {result.unwrap_err()}")
            return

        parsed_message = result.unwrap()
        logger.debug(f"Successfully parsed Netlink message: {parsed_message}")

        # Store in the inbound queue for retrieval by receive_message()
        await self.inbound_send.send(parsed_message)

    async def send_message(self, message: NetlinkHeaderTrait) -> Result[None, str]:
        """
        Trait-bound to take in a serialized NetlinkMessage and send it via self.sock.
        """
        if not self.sock:
            return Err("Socket not initialized. Call initialize() first.")

        try:
            await self.sock.send(message)
            return Ok(None)
        except Exception as e:
            return Err(f"Send error: {e}")

    async def receive_message(self, timeout: float = 1.0) -> Result[dict, str]:
        """
        Retrieve one Netlink message from the inbound queue, subject to timeout.
        """
        if not self.inbound_recv:
            return Err("Socket not initialized. inbound_recv channel is missing.")

        with move_on_after(timeout) as cancel_scope:
            try:
                msg = await self.inbound_recv.receive()
                if cancel_scope.cancelled_caught:
                    return Err("Timeout occurred waiting for Netlink message.")
                return Ok(msg)
            except trio.EndOfChannel:
                return Err("No messages left in the buffer!")

    async def close(self) -> Result[None, str]:
        """
        Stop the background loop, close the socket, and clean up channels.
        """
        self._running = False
        if self.sock:
            try:
                await self.sock.close()
            except Exception as e:
                return Err(f"Close error: {e}")
            finally:
                self.sock = None

        # If you want to also terminate the read loop more definitively:
        if self.nursery:
            self.nursery.cancel_scope.cancel()
            self.nursery = None

        # Close the memory channel
        if self.inbound_send:
            await self.inbound_send.close()

        return Ok(None)

    #
    # Message parsing helper function
    #
    async def _parse_peek(self, data: bytes, offset: int) -> Result [tuple[int, dict], str]:
        """
        Read netlink header from data[offset:], returning:
          Ok((nlmsg_len, nlmsg_seq, raw_msg_bytes))
        or Err(...) if invalid.
        """
        logger.trace("Entering _parse_peek()")

        # Check we have at least a netlink header
        if len(data) - offset < NLMSG_HDR_SIZE:
            return Err(f"Truncated netlink header at offset={offset}")

        try:
            logger.trace("Entering _parse_peek try block")
            # Unpack the netlink header fields
            nlmsg_len, nlmsg_type, nlmsg_flags, nlmsg_seq, nlmsg_pid = struct.unpack_from(
                NLMSG_HDR_FORMAT, data, offset
            )
            logger.trace("Exiting _parse_peek try block")
        except Exception as e:
            logger.error(f"Unable to unpack data for reason: {e}")
            return Err(f"Unable to unpack data for reason: {e}") 

        # Validate
        logger.trace("Entering _parse_peek() validation region")
        if nlmsg_len < NLMSG_HDR_SIZE:
            return Err(f"Invalid nlmsg_len={nlmsg_len} < header size")
        logger.trace("Exiting _parse_peek() validation region")

        end_pos = offset + nlmsg_len
        if end_pos > len(data):
            return Err(f"Message extends beyond buffer (end={end_pos}, data_len={len(data)})")

        info = {
            "len": nlmsg_len,
            "type": nlmsg_type,
            "flags": nlmsg_flags,
            "seq": nlmsg_seq,
        }
        logger.debug(f"Message Info: {info}")
        logger.trace("Exiting _parse_peek()")
        return Ok((nlmsg_len, info))

    #
    # Internal background read loop
    #
    # 1) side‑effect source → async generator of raw bytes
    @staticmethod
    async def _rx_chunks(sock):
        while True:
            try:
                yield await sock.recv(65536)          # ← only blocking call
            except (trio.ClosedResourceError, trio.Cancelled):
                break
            
    # 2) pure helpers
    @staticmethod
    def split_frames(chunk: bytes):
        off = 0
        while off < len(chunk):
            hdr = struct.unpack_from(NLMSG_HDR_FORMAT, chunk, off)
            ln = hdr[0]
            yield chunk[off : off + ln]
            off += ln

    @staticmethod
    def parse_header(frame: bytes) -> Result[tuple[dict, bytes], str]:
        try:
            ln, ty, fl, seq, pid = struct.unpack_from(NLMSG_HDR_FORMAT, frame)
            return Ok(({"len": ln, "type": ty, "flags": fl, "seq": seq}, frame[NLMSG_HDR_SIZE:ln]))
        except Exception as e:
            return Err(str(e))

    # 3) functional reducer to group by seq until NLMSG_DONE
    @staticmethod
    def accumulate(buf, tpl):
        hdr, payload = tpl
        buf.append(payload)
        return [] if hdr["type"] == 3 else buf          # flush when NLMSG_DONE

    # 4) the new read‑loop is just plumbing
    async def _read_loop(self):
        async for chunk in self._rx_chunks(self.sock):
            frames = pipe(
                chunk,
                self.split_frames,          # bytes → Iterable[bytes]
                map(self.parse_header),     # validate to Result
                filter(lambda r: r.is_ok()),
                map(Result.unwrap)          # drop errors early
            )

            by_seq = reduceby(
                lambda t: t[0]["seq"],       # key = seq
                lambda acc, item: self.accumulate(acc, item),
                frames,                      # Iterable[(hdr,payload)]
                initial=[]                   # start per‑seq buffer
            )
            # dispatch completed sequences
            for seq, payloads in by_seq.items():
                if payloads:                 # complete message only
                    await self.inbound_send.send(b"".join(payloads))

class ImplNetlinkSyncContext(NetlinkSyncContextTrait, metaclass=Impl, target="NetlinkSocket"):
    def __enter__(self):
        self.sock = socket.socket(AF_NETLINK, SOCK_RAW, self.protocol)
        return self  # Allow `with NetlinkSocket() as pyr:`

    def __exit__(self, exc_type, exc_value, traceback):
        if self.sock:
            self.sock.close()

class ImplNetlinkAsyncContext(NetlinkAsyncContextTrait, metaclass=Impl, target="NetlinkSocket"):
    async def __aenter__(self):
        self.sock = trio.socket.socket(AF_NETLINK, SOCK_RAW, self.protocol)
        await self.sock.bind((0, 0))

        self._running = True

        # Use provided nursery or create a temporary one
        if self.nursery is not None:
            self.nursery.start_soon(self._read_loop)
        else:
            self.nursery = trio.open_nursery()
            self.nursery.start_soon(self._read_loop)
        
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self._running = False

        if self.sock:
            self.sock.close()

class NetlinkSocket(metaclass=Struct):
    """
    A concrete struct (dataclass) that includes:
      - protocol: the netlink protocol to use (e.g., NETLINK_ROUTE)
      - sock: the actual Trio socket object
      - a background nursery
      - channels for buffering inbound messages
      - a running flag
    """

    protocol: int
    sock: Optional[trio.socket.socket] = None
    nursery: Optional[trio.Nursery] = None
    _running: bool = False
    _message_buffer: Optional[dict[int, list[bytes]]] = None

    inbound_send: Optional[MemorySendChannel[NetlinkHeaderTrait]] = None
    inbound_recv: Optional[MemoryReceiveChannel[NetlinkHeaderTrait]] = None
