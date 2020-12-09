import os
import shutil

if __name__ == '__main__':
    p = "/home/zlc/hackathon/bdd100k/label20_yolo"
    fs = os.listdir(p)
    for f in fs:
        if f.split(".")[-1] == "txt":
            fp = os.path.join(p, f)
            np = os.path.join(p, "val", f.split("\\")[-1])
            shutil.move(fp, np)
