"""--------------------------------------------------------
Copyer:ZLC
<<获取文件列表>>
(1) os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
这个列表以字母顺序。 它不包括 '.' 和'..' 即使它在文件夹中。只支持在
Unix, Windows 下使用。
(2) os.path.join(path1[, path2[, ...]])    把目录和文件名合成一个路径
---------------------------------------------------------"""
import os
data_dir = "/home/zlc/hackathon/bdd100k/label20/detection20/train"      #需要切割的json文件

def getRawFileList(path):
    files = []
    for f in os.listdir(path):
        if not f.endswith("~") or not f == "":      # 返回指定的文件夹包含的文件或文件夹的名字的列表
            files.append(os.path.join(path, f))     # 把目录和文件名合成一个路径
            JsonPath = os.path.join(path, f)
            JPath = JsonPath.replace('\\', '/')

            import json
            from pprint import pprint
            tempi = 1
            with open(JPath) as json_file:
             resp = json.loads(json_file.read())
            imgnum = len(resp)
            print('Data Size:',imgnum)

            #import os
            for i in range(0, imgnum):
             trainurl = "/home/zlc/hackathon/bdd100k/label20/train/" + resp[i]['name']   #目标文件路径加一个/
             portion = os.path.splitext(trainurl)
             jsonname = portion[0] + ".json"
             with open(jsonname, "a+") as dump_f:
              json.dump(resp[i], dump_f, indent=4)
             if i % 1000 == 0:
              print('Loading: No.',i)
    return 0

files = getRawFileList(data_dir)
