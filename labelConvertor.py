import os
import json
import time

class LabelConvertor():
    def __init__(self, imgSize):
        self.width    = imgSize[0]
        self.height   = imgSize[1]
        self.tagsCount= {}
        self.newTagsCount = {}
        self.tagsmap  = {'vehicle': 0, 'pedestrain': 1, 'road sign': 2, 'bicycle': 3}
        self.count    = 0
    
    def toYolo(self, srcPath, dstPath):
        self.srcPath = srcPath
        self.dstPath  = dstPath
        if not os.path.exists(self.dstPath):
            print("dstPath doesn't exist, create it now")
            os.makedirs(self.dstPath)
        
        files = os.listdir(self.srcPath)
        data  = {}
        for f in files:
            data[f] = self.parseFile(f)
        i = 0
        for k in data:
            for obj in data[k]:
                if obj['tag'] in self.newTagsCount:
                    self.newTagsCount[obj['tag']] += 1
                else:
                    self.newTagsCount[obj['tag']]  = 1
                    i += 1
        print("Parse %d files" % len(data))
        print(self.tagsCount)
        print(self.newTagsCount)

        for k in data:
            self.toYoloObj(k, data[k])


    def parseFile(self, file):
        filePath = os.path.join(self.srcPath, file)
        dstFile  = os.path.join(self.dstPath , file)
        assert os.path.isfile(filePath) and filePath.split(".")[-1] == "json", "Wrong path: %s" % filePath
 
        objs = []
        with open(filePath, 'r') as f:
            d = json.load(f)
            for frame in d["frames"]:
                for obj in frame["objects"]:
                    o = None
                    if obj["category"] == "car" or obj["category"] == "bus" or obj["category"] == "truck" or obj["category"] == "motorcycle":
                        o = self.bddObj(obj, "vehicle")
                    elif obj["category"] == "traffic sign":
                        o = self.bddObj(obj, "road sign")
                    elif obj["category"] == "bike":
                        o = self.bddObj(obj, "bicycle")
                    elif obj["category"] == "person" or obj["category"] == "rider":
                        o = self.bddObj(obj, "pedestrain")
                    if o is not None:
                        if obj["category"] in self.tagsCount:
                            self.tagsCount[obj["category"]] += 1
                        else:
                            self.tagsCount[obj["category"]] = 1
                        objs.append(o)
        return objs

    def bddObj(self, data, category):
        obj = dict()
        obj['tag'] = category
        obj["l"]     = float(data["box2d"]["x1"])
        obj["r"]     = float(data["box2d"]["x2"])
        obj["t"]     = float(data["box2d"]["y1"])
        obj["b"]     = float(data["box2d"]["y2"])
        assert obj["l"] <= obj["r"] and obj["t"] <= obj["b"], "Error label box!"

        obj['xcenter'] = (obj['l'] + abs(obj['r'] - obj['l']) / 2) / self.width
        obj['ycenter'] = (obj['t'] + abs(obj['b'] - obj['t']) / 2) / self.height
        obj['width']   = abs(obj['r'] - obj['l']) / self.width
        obj['height']  = abs(obj['b'] - obj['t']) / self.height
        return obj
    
    def toYoloObj(self, f, objs):
        f = f.split(".")[0] + ".txt"
        dstFile = os.path.join(self.dstPath, f)
        with open(dstFile, 'w') as f:
            for obj in objs:
                f.write("%s %.6f %.6f %.6f %.6f\n" % (self.tagsmap[obj['tag']], obj['xcenter'], obj['ycenter'], obj['width'], obj['height']))
    
    def summary(self, srcPath):
        self.srcPath = srcPath
        train_path = os.path.join(self.srcPath, "train")
        val_path = os.path.join(self.srcPath, "val")
        for path in [train_path, val_path]:
            fs = os.listdir(path)
            print("%s has %d files" % (path, len(fs)))
            framesNum = 0
            tagsCount = {}
            for f in fs:
                assert f.split(".")[-1] == "json", "%s is not json!" % f
                with open(os.path.join(path, f), 'r') as file:
                    data = json.load(file)
                    framesNum += len(data["frames"])
                    for frame in data["frames"]:
                        for obj in frame["objects"]:
                            if obj["category"] in tagsCount:
                                tagsCount[obj["category"]] += 1
                            else:
                                tagsCount[obj["category"]]  = 1
            print("%s frame average is %f" % (path, framesNum / len(fs)))
            print(tagsCount)
            print("--------------------------------------")


if __name__ == '__main__':
    convertor = LabelConvertor((1280, 720))
    # convertor.toYolo("/home/zlc/hackathon/bdd100k/label20/train", "/home/zlc/hackathon/bdd100k/label20_yolo/train")
    # convertor.toYolo("/home/zlc/hackathon/bdd100k/label20/val", "/home/zlc/hackathon/bdd100k/label20_yolo/val")
    convertor.summary("/home/zlc/hackathon/bdd100k/label20")
