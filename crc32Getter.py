import binascii
def getter(fileName):
	with open(fileName, 'rb') as f:
		w = f.read()
	return '%08X' % binascii.crc32(w)