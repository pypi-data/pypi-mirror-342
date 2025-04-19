import os
import sys
import select
import termios
import tty
import fcntl
import re

# Regular expression to remove ANSI escape sequences
ANSI_ESCAPE_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def set_raw_mode(fd):
    """Set terminal to raw mode."""
    old_attrs = termios.tcgetattr(fd)
    tty.setraw(fd)
    return old_attrs

def restore_mode(fd, old_attrs):
    """Restore terminal settings."""
    termios.tcsetattr(fd, termios.TCSADRAIN, old_attrs)

# Set stdin to non-blocking
fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

# Store original terminal settings
stdin_attrs = set_raw_mode(sys.stdin.fileno())

_master, _slave = os.openpty()  # Create a PTY pair
process_buffer = False

while True:
    ready, _, _ = select.select([sys.stdin.fileno(), _master], [], [], 0.5)

    if _master in ready:  # Read from PTY
        data = os.read(_master, 1024)
        if not data:
            break
        # Filter out ANSI escape sequences
        clean_data = ANSI_ESCAPE_RE.sub('', data.decode('utf-8'))
        os.write(sys.stdout.fileno(), clean_data.encode())

    char = b''
    if sys.stdin.fileno() in ready:  # Read from stdin
        while True:
            try:
                char += os.read(sys.stdin.fileno(), 1)
                char.decode('utf-8')  # Ensure it's a full character
                break
            except UnicodeDecodeError:
                continue

        if char == b'':
            break  # End of input

    process_buffer = False

# Restore terminal settings on exit
restore_mode(sys.stdin.fileno(), stdin_attrs)

