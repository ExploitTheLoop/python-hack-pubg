from crc32forcer import access
from crc32Getter import getter
from random import randbytes
import os

def changeLib(data):
    libtersafe = f"{data}libtersafe.so"
    os.system(f"cp {libtersafe} -t /storage/emulated/0/RulerKing/")
    global CurrentCrc32
    CurrentCrc32 = getter(libtersafe)
    with open(libtersafe, "ab") as lw:
        lw.seek(20000000)
        lw.write(randbytes(200000000))
        lw.close()
    access(libtersafe, CurrentCrc32)

def default(data):
    libtersafe = f"{data}libtersafe.so"
    os.system(f"rm -rf {libtersafe}")
    os.system("cp /storage/emulated/0/RulerKing/libtersafe.so -t {}".format(data))
