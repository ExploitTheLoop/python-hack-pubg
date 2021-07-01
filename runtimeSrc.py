import os
from crc32Getter import getter
from crc32forcer import access

CurrentCrc32 = ""
def changeSrc(pkg):
    fileName = f"/data/media/0/Android/data/{pkg}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SrcVersion.ini"
    filepath = f"/data/media/0/Android/data/{pkg}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/"
    CurrentCrc32 = getter(fileName)
    if os.path.exists("/storage/emulated/0/RulerKing"):
        pass
    else:
        os.system("mkdir /storage/emulated/0/RulerKing")
    os.system("cp {} -t /storage/emulated/0/RulerKing/".format(fileName))
    os.system(f"rm -rf {fileName}")
    os.system(f"rm -rf /data/media/0/Android/data/{pkg}/files/TGPA/")
    os.system(f"rm -rf /data/media/0/Android/data/{pkg}/cache/")
    os.system("cp SrcVersion.ini -t {}".format(filepath))
    access(fileName, CurrentCrc32)

def replace(pkg):
    fileName = f"/data/media/0/Android/data/{pkg}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SrcVersion.ini"
    filepath = f"/data/media/0/Android/data/{pkg}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/"
    os.system(f"rm -rf {fileName}")
    os.system("cp /storage/emulated/0/RulerKing/SrcVersion.ini -t {}".format(filepath))
    global CurrentCrc32
    access(fileName, CurrentCrc32)
    


