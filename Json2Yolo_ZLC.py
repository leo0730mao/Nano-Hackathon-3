import json
import os

categorys = ['pedestrian', 'rider', 'car', 'truck', 'bus','motorcycle', 'bicycle', 'traffic sign']  #类别
path = "/home/zlc/hackathon/bdd100k/label20/train"    #原json文件
textpath = "/home/zlc/hackathon/bdd100k/label20_yolo/train"    #生成目标txt文件

files = []
for jsonFile in os.listdir(path):
	if not jsonFile.endswith("~") or not jsonFile == "":      # 返回指定的文件夹包含的文件或文件夹的名字的列表
		files.append(os.path.join(path, jsonFile))     # 把目录和文件名合成一个路径
		JsonPath = os.path.join(path, jsonFile)         #json文件路径
		JPath = JsonPath.replace('\\', '/')                 #右斜改左斜\\ 2 /
	
		print(JPath)
		f = open(JPath)
		
		of = json.load(f, strict=False)    #json文件load进来
		info = of['labels']
		name = of['name']
		
		Jname, suffix = os.path.splitext(name)
		txtname = textpath + "/" + Jname + '.txt'
		JsonTxt = open(txtname, 'a')
		for image_index in range(0, len(info)):
			strs = ""
			image = info[image_index]
		
			if image["category"] in categorys:
				dw = 1.0 / 1280
				dh = 1.0 / 720
				category_hackathon = 0
				
				if image["category"] == "car" or image["category"] == "bus" or image["category"] == "truck" or image["category"] == "motorcycle":
					category_hackathon = 0
				elif image["category"] == "traffic sign":
					category_hackathon = 2
				elif image["category"] == "bicycle":
					category_hackathon = 3
				elif image["category"] == "pedestrian" or image["category"] == "rider":
					category_hackathon = 1
				
				strs += str(category_hackathon)
				strs += " "
				strs += str(((image["box2d"]["x1"] + image["box2d"]["x2"]) / 2.0) * dw)
				strs += " "
				strs += str(((image["box2d"]["y1"] + image["box2d"]["y2"]) / 2.0) * dh)
				strs += " "
				strs += str(((image["box2d"]["x2"] - image["box2d"]["x1"])) * dw)
				strs += " "
				strs += str(((image["box2d"]["y2"] - image["box2d"]["y1"])) * dh)
				strs += "\n"
				#print(strs)
				JsonTxt.writelines(strs)
		JsonTxt.close()

    #print(strs)
    #return 0

