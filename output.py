import logging



GRAY, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(30, 38)

COLOR_SEQ = '\033[1;{color:d}m'
RESET_SEQ = '\033[0m'

COLORS = {
	logging.DEBUG: GRAY,
	logging.INFO: WHITE,
	logging.WARNING: YELLOW,
	logging.ERROR: RED,
	logging.CRITICAL: MAGENTA,
}


def colorize(s: str, color: int) -> str:
	return COLOR_SEQ.format(color = color) + s + RESET_SEQ


def logLevelColor(level: int):
	return COLORS.get(level, WHITE)
