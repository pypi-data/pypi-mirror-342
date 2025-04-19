import logging

# Create the global logger for Pyritex
logger = logging.getLogger("pyritex")

# Define TRACE level (below DEBUG)
TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")

def trace(self, message, *args, **kwargs):
    """Custom TRACE log level, more detailed than DEBUG."""
    if self.isEnabledFor(TRACE_LEVEL):  
        self._log(TRACE_LEVEL, message, args, **kwargs)

logging.Logger.trace = trace

# Default: Logging is silent unless the user enables it
logger.setLevel(logging.WARNING)

def set_log_level(level=logging.DEBUG):
    """Allows users to enable logging for Pyritex globally."""
    logger.setLevel(level)
