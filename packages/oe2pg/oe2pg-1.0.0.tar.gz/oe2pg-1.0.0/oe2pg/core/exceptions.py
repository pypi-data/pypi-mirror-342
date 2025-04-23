#================================================================================
#
#   ╔═╗═╗ ╦╔═╗╔═╗╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
#   ║╣ ╔╩╦╝║  ║╣ ╠═╝ ║ ║║ ║║║║╚═╗
#   ╚═╝╩ ╚═╚═╝╚═╝╩   ╩ ╩╚═╝╝╚╝╚═╝
#
#--------------------------------------------------------------------------------
#
#   Author:  Benjamin Cance (KC8BWS)
#   Email:   canceb@gmail.com
#   Date:    22-04-2025
#
#--------------------------------------------------------------------------------
#
#   OE2PG Database Mirroring Tool
#   exceptions.py
#
#   Custom exception hierarchy for handling specific error conditions
#   throughout the mirroring process.
#
#================================================================================

class MirrorError(Exception):
    """Base exception for the DB Mirror package."""
    pass

class ConnectionError(MirrorError):
    """Raised when there are connection issues."""
    pass

class SyncError(MirrorError):
    """Raised when there are synchronization issues."""
    pass

class ConfigError(MirrorError):
    """Raised when there are configuration issues."""
    pass

class AuthorizationError(MirrorError):
    """Raised when there are authorization issues."""
    pass