# netlink/rtnl/consts.py
#
# Python equivalents of various RTNETLINK constants and macros
# extracted from linux/rtnetlink.h
#
# NOTE: This file provides Python definitions of the RTM_*, RTN_*,
#       RTPROT_*, and so on. Macros like RTA_ALIGN(), RTNH_ALIGN() are
#       implemented as Python functions. The struct definitions in
#       rtnetlink.h are not directly replicated here, as they don't
#       translate directly to Python. If needed, consider creating
#       Python classes or ctypes structures separately.

# --------------------------------------------------------------------
# RTM message base and types
# --------------------------------------------------------------------
RTM_BASE = 16

RTM_NEWLINK     = 16
RTM_DELLINK     = 17
RTM_GETLINK     = 18
RTM_SETLINK     = 19

RTM_NEWADDR     = 20
RTM_DELADDR     = 21
RTM_GETADDR     = 22

RTM_NEWROUTE    = 24
RTM_DELROUTE    = 25
RTM_GETROUTE    = 26

RTM_NEWNEIGH    = 28
RTM_DELNEIGH    = 29
RTM_GETNEIGH    = 30

RTM_NEWRULE     = 32
RTM_DELRULE     = 33
RTM_GETRULE     = 34

RTM_NEWQDISC    = 36
RTM_DELQDISC    = 37
RTM_GETQDISC    = 38

RTM_NEWTCLASS   = 40
RTM_DELTCLASS   = 41
RTM_GETTCLASS   = 42

RTM_NEWTFILTER  = 44
RTM_DELTFILTER  = 45
RTM_GETTFILTER  = 46

RTM_NEWACTION   = 48
RTM_DELACTION   = 49
RTM_GETACTION   = 50

RTM_NEWPREFIX   = 52

RTM_GETMULTICAST= 58

RTM_GETANYCAST  = 62

RTM_NEWNEIGHTBL = 64
RTM_GETNEIGHTBL = 66
RTM_SETNEIGHTBL = 67

RTM_NEWNDUSEROPT= 68

RTM_NEWADDRLABEL= 72
RTM_DELADDRLABEL= 73
RTM_GETADDRLABEL= 74

RTM_GETDCB      = 78
RTM_SETDCB      = 79

# The next enum value was __RTM_MAX, used for RTM_MAX:
# #define RTM_MAX (((__RTM_MAX + 3) & ~3) - 1)
# We'll define them with the typical formula:
# According to the kernel, __RTM_MAX is the last in the enum, so let's
# assume it was 80, making RTM_MAX:
#   = (((80 + 3) & ~3) - 1) => 83
# This is approximate. We replicate the kernel logic.
__RTM_MAX = 80  # internal guess
RTM_MAX = (((__RTM_MAX + 3) & ~3) - 1)

RTM_NR_MSGTYPES = (RTM_MAX + 1 - RTM_BASE)
RTM_NR_FAMILIES = (RTM_NR_MSGTYPES >> 2)

def RTM_FAM(cmd: int) -> int:
    """
    #define RTM_FAM(cmd) (((cmd) - RTM_BASE) >> 2)
    """
    return ((cmd - RTM_BASE) >> 2)


# --------------------------------------------------------------------
# RTA (rtattr) alignment macros
# --------------------------------------------------------------------
RTA_ALIGNTO = 4

def RTA_ALIGN(length: int) -> int:
    """
    #define RTA_ALIGN(len) ( ((len)+RTA_ALIGNTO-1) & ~(RTA_ALIGNTO-1) )
    """
    return ((length + RTA_ALIGNTO - 1) & ~(RTA_ALIGNTO - 1))

def RTA_LENGTH(length: int) -> int:
    """
    #define RTA_LENGTH(len) (RTA_ALIGN(sizeof(struct rtattr)) + (len))
    We assume sizeof(struct rtattr) = 4 bytes (2 shorts).
    """
    # The kernel's struct rtattr is 4 bytes, so we do:
    return RTA_ALIGN(4) + length

def RTA_SPACE(length: int) -> int:
    """
    #define RTA_SPACE(len) RTA_ALIGN(RTA_LENGTH(len))
    """
    return RTA_ALIGN(RTA_LENGTH(length))

def RTA_OK(rta_len: int, total_len: int) -> bool:
    """
    #define RTA_OK(rta,len) ((len) >= (int)sizeof(struct rtattr) && \
                             (rta)->rta_len >= sizeof(struct rtattr) && \
                             (rta)->rta_len <= (len))
    In Python, we can't directly check rta->rta_len. Typically you'd parse.
    This is more of a conceptual check. We'll provide a placeholder.
    """
    # We'll just do a simplified check that the total_len >= 4
    # and rta_len <= total_len. Real code must parse the rtattr struct.
    return (total_len >= 4) and (rta_len <= total_len)

# Macros RTA_NEXT, RTA_DATA, RTA_PAYLOAD are typically used while parsing
# raw memory. In Python, you'd parse with a library or struct. We'll just
# define placeholders if needed:

def RTA_DATA_OFFSET() -> int:
    """
    #define RTA_DATA(rta) ((void*)(((char*)(rta)) + RTA_LENGTH(0)))
    For Python, just note that data starts after 4 bytes + alignment.
    """
    return RTA_LENGTH(0)  # Typically 4, aligned to 4.

def RTA_PAYLOAD(rta_len: int) -> int:
    """
    #define RTA_PAYLOAD(rta) ((int)((rta)->rta_len) - RTA_LENGTH(0))
    We'll accept rta_len and compute the leftover after header + alignment.
    """
    return rta_len - RTA_LENGTH(0)


# --------------------------------------------------------------------
# RTN_xxx route types
# --------------------------------------------------------------------
RTN_UNSPEC     = 0
RTN_UNICAST    = 1
RTN_LOCAL      = 2
RTN_BROADCAST  = 3
RTN_ANYCAST    = 4
RTN_MULTICAST  = 5
RTN_BLACKHOLE  = 6
RTN_UNREACHABLE= 7
RTN_PROHIBIT   = 8
RTN_THROW      = 9
RTN_NAT        = 10
RTN_XRESOLVE   = 11
__RTN_MAX      = 12
RTN_MAX        = (__RTN_MAX - 1)

# --------------------------------------------------------------------
# rtm_protocol
# --------------------------------------------------------------------
RTPROT_UNSPEC   = 0
RTPROT_REDIRECT = 1
RTPROT_KERNEL   = 2
RTPROT_BOOT     = 3
RTPROT_STATIC   = 4
RTPROT_GATED    = 8
RTPROT_RA       = 9
RTPROT_MRT      = 10
RTPROT_ZEBRA    = 11
RTPROT_BIRD     = 12
RTPROT_DNROUTED = 13
RTPROT_XORP     = 14
RTPROT_NTK      = 15
RTPROT_DHCP     = 16

# --------------------------------------------------------------------
# rt_scope_t
# --------------------------------------------------------------------
RT_SCOPE_UNIVERSE = 0
RT_SCOPE_SITE     = 200
RT_SCOPE_LINK     = 253
RT_SCOPE_HOST     = 254
RT_SCOPE_NOWHERE  = 255

# --------------------------------------------------------------------
# rtm_flags
# --------------------------------------------------------------------
RTM_F_NOTIFY   = 0x100
RTM_F_CLONED   = 0x200
RTM_F_EQUALIZE = 0x400
RTM_F_PREFIX   = 0x800

# --------------------------------------------------------------------
# rt_class_t (routing table identifiers)
# --------------------------------------------------------------------
RT_TABLE_UNSPEC   = 0
RT_TABLE_COMPAT   = 252
RT_TABLE_DEFAULT  = 253
RT_TABLE_MAIN     = 254
RT_TABLE_LOCAL    = 255
RT_TABLE_MAX      = 0xFFFFFFFF

# --------------------------------------------------------------------
# RTA_xxx types
# --------------------------------------------------------------------
RTA_UNSPEC     = 0
RTA_DST        = 1
RTA_SRC        = 2
RTA_IIF        = 3
RTA_OIF        = 4
RTA_GATEWAY    = 5
RTA_PRIORITY   = 6
RTA_PREFSRC    = 7
RTA_METRICS    = 8
RTA_MULTIPATH  = 9
RTA_PROTOINFO  = 10  # no longer used
RTA_FLOW       = 11
RTA_CACHEINFO  = 12
RTA_SESSION    = 13  # no longer used
RTA_MP_ALGO    = 14  # no longer used
RTA_TABLE      = 15
__RTA_MAX      = 16
RTA_MAX        = (__RTA_MAX - 1)

# --------------------------------------------------------------------
# RTNH flags
# --------------------------------------------------------------------
RTNH_F_DEAD      = 1
RTNH_F_PERVASIVE = 2
RTNH_F_ONLINK    = 4

# RTNH alignment macros
RTNH_ALIGNTO = 4
def RTNH_ALIGN(length: int) -> int:
    """#define RTNH_ALIGN(len) ( ((len)+RTNH_ALIGNTO-1) & ~(RTNH_ALIGNTO-1) )"""
    return ((length + RTNH_ALIGNTO - 1) & ~(RTNH_ALIGNTO - 1))

# --------------------------------------------------------------------
# RTM_CACHEINFO, RTM_METRICS, etc. (some rely on rtattr expansions)
# --------------------------------------------------------------------

# For RTAX_*
RTAX_UNSPEC     = 0
RTAX_LOCK       = 1
RTAX_MTU        = 2
RTAX_WINDOW     = 3
RTAX_RTT        = 4
RTAX_RTTVAR     = 5
RTAX_SSTHRESH   = 6
RTAX_CWND       = 7
RTAX_ADVMSS     = 8
RTAX_REORDERING = 9
RTAX_HOPLIMIT   = 10
RTAX_INITCWND   = 11
RTAX_FEATURES   = 12
RTAX_RTO_MIN    = 13
__RTAX_MAX      = 14
RTAX_MAX        = (__RTAX_MAX - 1)

RTAX_FEATURE_ECN       = 0x00000001
RTAX_FEATURE_SACK      = 0x00000002
RTAX_FEATURE_TIMESTAMP = 0x00000004
RTAX_FEATURE_ALLFRAG   = 0x00000008

# --------------------------------------------------------------------
# prefix information
# --------------------------------------------------------------------
PREFIX_UNSPEC     = 0
PREFIX_ADDRESS    = 1
PREFIX_CACHEINFO  = 2
__PREFIX_MAX      = 3
PREFIX_MAX        = (__PREFIX_MAX - 1)

# --------------------------------------------------------------------
# Traffic control messages
# --------------------------------------------------------------------
TCA_UNSPEC   = 0
TCA_KIND     = 1
TCA_OPTIONS  = 2
TCA_STATS    = 3
TCA_XSTATS   = 4
TCA_RATE     = 5
TCA_FCNT     = 6
TCA_STATS2   = 7
TCA_STAB     = 8
__TCA_MAX    = 9
TCA_MAX      = (__TCA_MAX - 1)

# --------------------------------------------------------------------
# NDUSEROPT constants
# --------------------------------------------------------------------
NDUSEROPT_UNSPEC = 0
NDUSEROPT_SRCADDR= 1
__NDUSEROPT_MAX  = 2
NDUSEROPT_MAX    = (__NDUSEROPT_MAX - 1)

# --------------------------------------------------------------------
# RTMGRP_xxx - older-style netlink multicast groups
# --------------------------------------------------------------------
RTMGRP_LINK        = 1
RTMGRP_NOTIFY      = 2
RTMGRP_NEIGH       = 4
RTMGRP_TC          = 8

RTMGRP_IPV4_IFADDR = 0x10
RTMGRP_IPV4_MROUTE = 0x20
RTMGRP_IPV4_ROUTE  = 0x40
RTMGRP_IPV4_RULE   = 0x80

RTMGRP_IPV6_IFADDR = 0x100
RTMGRP_IPV6_MROUTE = 0x200
RTMGRP_IPV6_ROUTE  = 0x400
RTMGRP_IPV6_IFINFO = 0x800

RTMGRP_DECnet_IFADDR= 0x1000
RTMGRP_DECnet_ROUTE = 0x4000
RTMGRP_IPV6_PREFIX  = 0x20000

# --------------------------------------------------------------------
# rtnetlink_groups
# --------------------------------------------------------------------
RTNLGRP_NONE         = 0
RTNLGRP_LINK         = 1
RTNLGRP_NOTIFY       = 2
RTNLGRP_NEIGH        = 3
RTNLGRP_TC           = 4
RTNLGRP_IPV4_IFADDR  = 5
RTNLGRP_IPV4_MROUTE  = 6
RTNLGRP_IPV4_ROUTE   = 7
RTNLGRP_IPV4_RULE    = 8
RTNLGRP_IPV6_IFADDR  = 9
RTNLGRP_IPV6_MROUTE  = 10
RTNLGRP_IPV6_ROUTE   = 11
RTNLGRP_IPV6_IFINFO  = 12
RTNLGRP_DECnet_IFADDR= 13
# RTNLGRP_NOP2 = 14 (Unused placeholder)
RTNLGRP_DECnet_ROUTE = 15
RTNLGRP_DECnet_RULE  = 16
# RTNLGRP_NOP4 = 17
RTNLGRP_IPV6_PREFIX  = 18
RTNLGRP_IPV6_RULE    = 19
RTNLGRP_ND_USEROPT   = 20
RTNLGRP_PHONET_IFADDR= 21
RTNLGRP_PHONET_ROUTE = 22
__RTNLGRP_MAX        = 23
RTNLGRP_MAX          = (__RTNLGRP_MAX - 1)

# --------------------------------------------------------------------
# End of netlink/rtnl/consts.py
# --------------------------------------------------------------------

