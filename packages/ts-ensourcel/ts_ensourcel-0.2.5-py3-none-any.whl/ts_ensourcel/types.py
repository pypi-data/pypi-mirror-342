# Types for stufff
from dataclasses import dataclass
import enum


class KandaIndex(enum.IntEnum):
	"""
	Kandas for KYV range from 1-7, inclusive.
	"""

	ONE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	SIX = 6
	SEVEN = 7


class PrapathakaIndex(enum.IntEnum):
	"""
	Prapathakas for KYV range from 1-7, although not all kandas have 8 prapathakas.
	"""

	ONE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	SIX = 6
	SEVEN = 7
	EIGHT = 8


# Metadata we can use to tell the num prapathakas for each kanda.
# The number is the actual count, but the keys here are Kanda indexes
# for 1 to 7, the numbers are 8, 6, 5, 7, 7, 6, 5
num_prapathakas_per_kanda = {
	KandaIndex.ONE: 8,
	KandaIndex.TWO: 6,
	KandaIndex.THREE: 5,
	KandaIndex.FOUR: 7,
	KandaIndex.FIVE: 7,
	KandaIndex.SIX: 6,
	KandaIndex.SEVEN: 5,
}


@dataclass
class Kanda:
	index: KandaIndex


@dataclass
class Prapathaka:
	# number from 1-7 incl. for which prapathaka
	index: int
