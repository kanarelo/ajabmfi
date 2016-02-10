def get_int_or_None(_str):
	try:
		return int(_str)
	except ValueError:
		return None