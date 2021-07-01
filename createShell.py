import os, time
def shell(pkg):
    os.system("su -c chmod -R 777 /data/media/0/Android/data/{}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Paks/".format(pkg))
    time.sleep(1)
    os.system("rm -rf /data/media/0/Android/data/{}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/game_patch_1.4.0.9999.pak".format(pkg))
    os.system("rm -rf /data/media/0/Android/data/{}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/LightData".format(pkg))
    os.system("rm -rf /data/media/0/Android/data/{}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Logs".format(pkg))
    os.system("rm -rf /data/media/0/Android/data/{}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/PufferEifs0".format(pkg))
    os.system("rm -rf /data/media/0/Android/data/{}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/PufferEifs1".format(pkg))


