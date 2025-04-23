import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
__version__ = "0.0.1"


def get_version():
	return __version__


def welcome_message():
	return "Hello"


def main():
	print(welcome_message())


__all__ = [
	"__version__",
	"get_version",
]
