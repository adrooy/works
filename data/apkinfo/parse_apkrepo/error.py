import logging

# from scapy
log_andro = logging.getLogger("andro")
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
log_andro.addHandler(console_handler)
log_runtime = logging.getLogger("andro.runtime")          # logs at runtime
log_interactive = logging.getLogger("andro.interactive")  # logs in interactive functions
log_loading = logging.getLogger("andro.loading")          # logs when loading andro

def set_debug() :
    log_andro.setLevel( logging.DEBUG )

def get_debug() :
    return log_andro.getEffectiveLevel() == logging.DEBUG

def warning(x):
    log_runtime.warning(x)

def error(x) :
    log_runtime.error(x)
    raise()

def debug(x) :
    log_runtime.debug(x)
