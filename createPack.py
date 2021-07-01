from random import randbytes
import os

def genrate(pkg):
    with open("game_patch_1.4.0.9999", 'ab') as f:
        f.write(randbytes(200000))
        f.close()
    os.system("cp game_patch_1.4.0.9999.pak -t /data/media/0/Android/data/{}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Paks/game_patch_1.4.0.9999.pak".format(pkg))
    os.system("rm game_patch_1.4.0.9999.pak")