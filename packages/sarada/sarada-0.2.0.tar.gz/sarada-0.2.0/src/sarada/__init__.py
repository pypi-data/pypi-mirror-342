import logging
from sarada.meta import __version__

logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_version():
	return __version__


def welcome_message():
	return "welcome to sarada"


def main():
	print(welcome_message())


__all__ = [
	"__version__",
	"get_version",
]
