import os

class LabelConvertor():
    def __init__(self, dataPath, dstPath, imgSize):
        self.dataPath = dataPath
        self.dstPath  = dstPath
        self.imgSize  = imgSize
    
    def toYolo(self):
        if !os.path.exists(self.dstPath):
            print("dstPath doesn't exist, create it now")
            os.mkdir(self.dstPath)
        files = os.listdir(self.dataPath)
        data  = {}
        for f in files:
            data[f] = self.parseFile(f)
        self.tags  = {}
        for k in data:
            for obj in data[k]:
                if obj['tag'] in tags:
                    tags[obj['tag']] += 1
                else:
                    tags[obj['tag']]  = 1
        print(tags)
        for k in data:
            self.toYoloObj(k, data[k])


    def parseFile(self, file):
        filePath = os.path.join(self.dataPath, file)
        dstFile  = os.path.join(dstPath, file)
        assert(!os.path.isfile(filePath) or filePath.split(".")[-1] != "txt", "Wrong path: %s" % filePath)
 
        objs = []
        with open(filePath, 'r') as f:
            lines = f.read().strip().split("\n")
            for line in lines:
                objs.append(self.bddObj(line))

        return objs

    def bddObj(self, s):
        attrs = s.strip().split(" ")
        assert(len(attrs) == 15)

        obj['tag'] = attr[0]
        obj['x1'] = float(attr[4])
        obj['y1'] = float(attr[5])
        obj['x2'] = float(attr[6])
        obj['y2'] = float(attr[7])
        obj['xcenter'] = (obj['x1'] + abs(obj['x2'] - obj['x1']) / 2) / self.imgSize[0]
        obj['ycenter'] = (obj['y1'] + abs(obj['y2'] - obj['y1']) / 2) / self.imgSize[1]
        obj['width']   = abs(obj['x2'] - obj['x1']) / self.imgSize[0]
        obj['height']  = abs(obj['y2'] - obj['y1']) / self.imgSize[1]
        return obj
    
    def toYoloObj(self, f, objs):
        dstFile = os.path.join(self.dstPath, f)
        with open(dstFile, 'w') as f:
            for obj in objs:
                f.write("%s %.6f %.6f %.6f %.6f\n" % (obj['tag'], obj['xcenter'], obj['ycenter'], obj['width'], obj['height']))

if __name__ == '__main__':
    convertor = LabelConvertor("/home/zlc/hackathon/Data/images/newlabel", "/home/zlc/hackathon/Data/images/test", (1280, 720))
    convertor.toYolo()