DEV_NUMBERS = "०१२३४५६७८९"
LAT_NUMBERS = "0123456789"

dev_to_lat_mapping_table = str.maketrans(DEV_NUMBERS, LAT_NUMBERS)
lat_to_dev_mapping_table = str.maketrans(LAT_NUMBERS, DEV_NUMBERS)


def lat_numeral_to_dev(lat_numeral: int) -> str:
	return DEV_NUMBERS[lat_numeral]


def dev_numeral_to_lat_int(dev_numeral: str) -> int:
	return DEV_NUMBERS.index(dev_numeral)


def dev_to_lat_trans(string_with_dev_numerals: str) -> str:
	return string_with_dev_numerals.translate(dev_to_lat_mapping_table)
