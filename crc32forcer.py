import sys, zlib, struct, os, hashlib
author = "Ruler King"

def crc32v2(fileName):
	fd = open(fileName,"rb")
	crc = 0

	while True:
		buffer = fd.read(1024 * 1024)
		if len(buffer) == 0:
			fd.close()
			if sys.version_info[0] < 3 and crc < 0:
				crc += 2 ** 32
			return crc
		crc = zlib.crc32(buffer, crc)


def crc32_i(fileName):
	iHash = crc32v2(fileName)
	if sys.version_info[0] < 3 and iHash < 0:
		iHash += 2 ** 32
	return iHash

def crc32_s(fileName):
	iHash = crc32v2(fileName)
	if sys.version_info[0] < 3 and iHash < 0:
		iHash += 2 ** 32
	sHash = '%08X' % iHash
	return sHash


def itos(iHash):
	return '%08X' % iHash


def stoi(sHash):
	return int(sHash, base=16)


def calcNewContents(targetCRC, originalCRC):
	CRCPOLY = 0xEDB88320
	CRCINV = 0x5B358FD3
	INITXOR = 0xFFFFFFFF
	FINALXOR = 0xFFFFFFFF

	targetCRC ^= FINALXOR
	originalCRC ^= FINALXOR
	newContents = 0x00000000

	for i in range(0, 32):
		# reduce modulo CRCPOLY
		if (newContents & 1) != 0:
			newContents = (newContents >> 1) ^ CRCPOLY
		else:
			newContents >>= 1
		# add CRCINV if corresponding bit of operand is set
		if (targetCRC & 1) != 0:
			newContents ^= CRCINV

		targetCRC >>= 1

	# finally add old crc
	newContents ^= originalCRC

	return newContents


def appendContents(fileName, number):
	fd = open(fileName, 'ab')
	#ar = number.to_bytes(4, byteorder='little', signed=False)
	ar = struct.pack("<I", number)
	fd.write(ar)
	fd.close()


def changeCRC(fileName, targetCRC):
	originalCRC = crc32_i(fileName)
	newContents = calcNewContents(targetCRC, originalCRC)
	appendContents(fileName, newContents)


def getMd5(filename):
	try:
		md5_hash = hashlib.md5()
		a_file = open(filename, "rb")
		content = a_file.read()
		md5_hash.update(content)
		digest = md5_hash.hexdigest()
		return digest
	except Exception as e:
		return e


def printReadme():
	# Print user manual
	print("Error: ask the way to run from owner {}".format(author))


def access(targetArea, targetCrc):
	
	fileName = targetArea
	first_crc = itos(crc32_i(fileName))
	first_md5 = getMd5(fileName)
	targetCRCs = targetCrc

	validTargetCRC = True
	crc_max = int("FFFFFFFF", base=16)
	crc_min = int("00000000", base=16)
	try:
		targetCRC = int(targetCRCs, base=16)
		if targetCRC > crc_max or targetCRC < crc_min:
			validTargetCRC = False
	except:
		validTargetCRC = False

	if validTargetCRC:
		if os.path.isfile(fileName):
			originalCRC = crc32_i(fileName)
			targetCRC = int(targetCRCs, base=16)
			print('Original V32: %s' % itos(originalCRC))
			print(f'Original M5: {first_md5}')
			print('Target V32:   %s' % itos(targetCRC))

			newContents = calcNewContents(targetCRC, originalCRC)
			print('Four bytes to append (hex): %s' % itos(newContents))

			appendContents(fileName, newContents)

			finalCRC = crc32_i(fileName)
			print('Final V32:    %s' % itos(finalCRC))
			print(f'Final M5: {getMd5(fileName)}')

			if finalCRC == targetCRC:
				print('Done.')
			else:
				print('Failed.')
		else:
			print("Input file inaccessible.")
	else:
		# print("Invalid target CRC-32.")
		printReadme()
		sys.exit(-1)
