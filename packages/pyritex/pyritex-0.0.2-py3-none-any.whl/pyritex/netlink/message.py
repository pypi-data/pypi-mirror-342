import struct
from typing import Optional

from abc import abstractmethod

from oxitrait.trait import Trait
from oxitrait.impl import Impl
from oxitrait.struct import Struct
from oxitrait.enum import Enum, auto
from oxitrait.runtime import requires_traits

from result import Result, Ok, Err

from pyritex.netlink.consts import *
from pyritex.netlink.rtnl.consts import *

#
# -------------------------------------------------------------------
# Constants / Format Strings
# -------------------------------------------------------------------

#
# -------------------------------------------------------------------
# 1) Traits
#
#    NetlinkHeaderTrait
#    RtMsgTrait
#    RouteMessageTrait
#
# -------------------------------------------------------------------
class NetlinkHeaderTrait(metaclass=Trait):
    """
    Trait describing the universal netlink header
    (analogous to `struct nlmsghdr`).
    """

    @abstractmethod
    def nlmsg_len(self) -> int:
        pass

    @abstractmethod
    def nlmsg_type(self) -> int:
        pass

    @abstractmethod
    def nlmsg_flags(self) -> int:
        pass

    @abstractmethod
    def nlmsg_seq(self) -> int:
        pass

    @abstractmethod
    def nlmsg_pid(self) -> int:
        pass

    @abstractmethod
    def to_bytes(self) -> Result[bytes, str]:
        """
        Serialize the netlink header to 16 bytes, returning a Result.
        """
        pass


class RtMsgTrait(metaclass=Trait):
    """
    Trait describing a minimal route header, analogous to `struct rtmsg`.
    """

    @abstractmethod
    def family(self) -> int:
        pass

    @abstractmethod
    def table(self) -> int:
        pass

    @abstractmethod
    def to_bytes(self) -> Result[bytes, str]:
        """
        Serialize the route header into bytes, returning a Result.
        Real code might have more fields: (dst_len, src_len, tos, scope, protocol, etc.)
        """
        pass

    @abstractmethod
    def __post_init__(self):
        pass


class RouteMessageTrait(metaclass=Trait):
    """
    Trait that describes the entire RouteMessage's behavior, e.g.:
      - how to build the final netlink message (header + route + attrs)
      - debug_info or other utility methods
    """

    @abstractmethod
    def to_bytes(self) -> Result[bytes, str]:
        """
        Return the combined header + route + attrs as raw bytes.
        """
        pass

    @abstractmethod
    def debug_info(self) -> str:
        pass


#
# -------------------------------------------------------------------
# 2) Impls
#
#    ImplNetlinkHeader
#    ImplRtMsg
#    ImplRouteMessage
#
# -------------------------------------------------------------------
class ImplNetlinkHeader(NetlinkHeaderTrait, metaclass=Impl, target="NetlinkHeader"):
    """
    Concrete implementation for NetlinkHeaderTrait on NetlinkHeader.
    """

    def nlmsg_len(self) -> int:
        return self.nlmsg_len

    def nlmsg_type(self) -> int:
        return self.nlmsg_type

    def nlmsg_flags(self) -> int:
        return self.nlmsg_flags

    def nlmsg_seq(self) -> int:
        return self.nlmsg_seq

    def nlmsg_pid(self) -> int:
        return self.nlmsg_pid

    def to_bytes(self) -> Result[bytes, str]:
        """
        Return Ok(...) with the packed 16-byte netlink header, or Err(...) on failure.
        """
        try:
            hdr = struct.pack(
                NLMSG_HDR_FORMAT,
                self.nlmsg_len,
                self.nlmsg_type,
                self.nlmsg_flags,
                self.nlmsg_seq,
                self.nlmsg_pid,
            )
            return Ok(hdr)
        except struct.error as e:
            return Err(f"Header pack error: {e}")


class ImplRtMsg(RtMsgTrait, metaclass=Impl, target="RtMsg"):
    """
    Implementation of route header logic for RtMsg.
    """

    def family(self) -> int:
        return self.family

    def table(self) -> int:
        return self.table

    def to_bytes(self) -> Result[bytes, str]:
        """
        Very simplified: pack 2 bytes for (family, table).
        """
        try:
            packed = struct.pack("BB", self.family, self.table)
            return Ok(packed)
        except struct.error as e:
            return Err(f"RtMsg pack error: {e}")

    def __post_init__(self):
        pass


class ImplRouteMessage(RouteMessageTrait, metaclass=Impl, target="RouteMessage"):
    """
    Implementation of the top-level route message logic,
    combining the netlink header, the route header, and any attributes.
    """

    def to_bytes(self) -> Result[bytes, str]:
        """
        Compose the final netlink message:
          netlink header + route header + attribute bytes
        """
        # First, pack the route portion
        route_res = self.route.to_bytes()
        if route_res.is_err():
            return route_res
        route_part = route_res.unwrap()

        total_len = NLMSG_HDR_SIZE + len(route_part) + len(self.attrs)

        pad_len = (4 - (total_len % 4)) % 4 
        final_padding = b'\x00' * pad_len

        self.header.nlmsg_len = total_len + pad_len

        # Now pack the netlink header
        print(self)
        hdr_res = self.header.to_bytes()
        if hdr_res.is_err():
            return hdr_res
        hdr_bytes = hdr_res.unwrap()

        # Combine all pieces
        raw_msg = hdr_bytes + route_part + self.attrs + final_padding
        return Ok(raw_msg)

    def debug_info(self) -> str:
        return (
            f"RouteMessage("
            f"type={self.header.nlmsg_type()}, "
            f"flags=0x{self.header.nlmsg_flags():X}, "
            f"seq={self.header.nlmsg_seq()}, "
            f"family={self.route.family()}, "
            f"table={self.route.table()}, "
            f"attrs_len={len(self.attrs)})"
        )

    def nlmsg_type(self) -> int:
        return RTM_GETROUTE

    def nlmsg_flags(self) -> int:
        return NLM_F_REQUEST | NLM_F_DUMP

#
# -------------------------------------------------------------------
# 3) Structs
#
#    NetlinkHeader
#    RtMsg
#    RouteMessage
#
# -------------------------------------------------------------------
class NetlinkHeader(metaclass=Struct):
    """
    A Struct for storing netlink header fields:
      - nlmsg_len  (total length)
      - nlmsg_type (which command/family)
      - nlmsg_flags
      - nlmsg_seq  (sequence #)
      - nlmsg_pid  (port ID, though often 0 for user->kernel)
    """
    nlmsg_len: int = 0
    nlmsg_type: int = 0
    nlmsg_flags: int = 0
    nlmsg_seq: int = 0
    nlmsg_pid: int = 0


class RtMsg(metaclass=Struct):
    """
    The route-specific header fields.
      - family
      - dst_len
      - src_len
      - tos
      - table
      - protocol
      - scope
      - rtm_type
      - flags
    """
    family: Optional[int] = None
    dst_len: Optional[int] = None
    src_len: Optional[int] = None
    tos: Optional[int] = None
    table: Optional[int] = None
    protocol: Optional[int] = None
    scope: Optional[int] = None
    rtm_type: Optional[int] = None
    flags: Optional[int] = None


class RouteMessage(metaclass=Struct):
    """
    A composed data structure referencing:
      - header: NetlinkHeader
      - route:  RtMsg
      - attrs:  raw bytes (in real code, you'd have a list of typed attributes)
    """
    header: NetlinkHeader
    route: RtMsg
    attrs: bytes

    def __post_init__(self):
        if self.attrs is None:
            self.attrs = b""
        if self.header.nlmsg_len is None:
            self.header.nlmsg_len = 0
        if self.header.nlmsg_seq is None:
            self.header.nlmsg_seq = 0
        if self.header.nlmsg_pid is None:
            self.header.nlmsg_pid = 0
        self.header.nlmsg_type = self.nlmsg_type()
        self.header.nlmsg_flags = self.nlmsg_flags()