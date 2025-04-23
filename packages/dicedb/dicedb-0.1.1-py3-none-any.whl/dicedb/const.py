"""Constants for the Dicedb project."""

MAX_REQUEST_SIZE = 32 * 1024 * 1024
IO_BUFFER_SIZE = 16 * 1024

# command
EXPIRE_OPTIONS = {'NX', 'XX'}
EXPIRE_AT_OPTIONS = {'NX', 'XX', 'GT', 'LT'}

GETEX_OPTIONS = {'EX', 'PX', 'EXAT', 'PXAT', 'PERSIST'}