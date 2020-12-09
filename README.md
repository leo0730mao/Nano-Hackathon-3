# Nano-Hackathon-3
#训练命令
python train.py --img 640 --batch 48 --epochs 50 --data ./data/hackathon.yaml --cfg ./models/hackathon.yaml --weights ./weights/yolov5s.pt --device 0,1,2
如果要修改用的模型，修改./models/hackathon.yaml,或者创建一个新的yaml文件，可以直接复制黏贴./models/下的其他对应的yaml文件，但是要和weights参数指定的预训练模型对应
