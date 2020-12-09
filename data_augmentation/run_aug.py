import json
from data_aug.data_aug import *
from data_aug.bbox_util import *
import numpy as np
import cv2
from tqdm import tqdm


def build_imgano(path, id, category_list, bbx):

    image = {}
    object_list = []
    for index in range(bbx.shape[0]):
        bbox = {}
        bbox['xmin'] = bbx[index][0]
        bbox['ymin'] = bbx[index][3]
        bbox['xmax'] = bbx[index][2]
        bbox['ymax'] = bbx[index][1]
        object = {}
        object['category'] = category_list[index]
        object['bbox'] = bbox
        object_list.append(object)
    image['path'] = path
    image['objects'] = object_list
    image['id'] = id
    return image
#useless
label_convert = {'i':0,'p':1,'w':2}

def check_bbx(bbx, image_size = 2048):
    for index in range(bbx.shape[0]):
        for j in range(4):
            if bbx[index][j]>=image_size or bbx[index][j]<0:
                return True
    return False

'''
dir1 = "./aug_images"
dir2 = "./aug_labels"
list1 = os.listdir(dir1)
list2 = os.listdir(dir1)
e_list = []
print(len(os.listdir(dir1)))
print(len(os.listdir(dir2)))
for img in list1:
    img_ = img.split('.')[0]
    img_ = img + '.txt'
    if img_ not in list2:
        e_list.append(img)
print(len(e_list))

file_path:origin annotation
train_img_path:original images
'''
file_path = "~/nanohackathon/data/annotations.json"
train_img_path = "~/nanohackathon/data/images/train"
train_aug_path = "~/nanohackathon/data/aug_images/train"
new_anno_json_path = "~/nanohackathon/data/train_aug_annotations.json"
skip_num = 0
train_img_list = [os.path.join(train_img_path, img_path) for img_path in os.listdir(train_img_path)]
aug_times = 10
new_anno = {}
class_0 = 0
class_1 = 0
class_2 = 0
with open(file_path, 'r', encoding='utf8') as f:
    data = json.load(f)
    anno = data['imgs']
    new_anno['imgs'] = {}
    new_anno['types'] = data['types']
    for train_img in tqdm(train_img_list):
        aug_image_num = len(os.listdir(train_aug_path))
        assert len(new_anno['imgs']) == aug_image_num
        flag0 = False
        flag1 = False
        flag2 = False
        img_id = train_img.split("/")[-1].split(".")[0]
        img_path = train_img
        img_anno = anno[img_id]
        bboxes = np.zeros((len(img_anno['objects']), 5))
        cat_list = []
        for index,obj in enumerate(img_anno['objects']):
            bboxes[index][0] = obj['bbox']['xmin']
            bboxes[index][1] = obj['bbox']['ymax']
            bboxes[index][2] = obj['bbox']['xmax']
            bboxes[index][3] = obj['bbox']['ymin']
            bboxes[index][4] = label_convert[obj['category'][:1]]
            cat_list.append(obj['category'])
            if bboxes[index][4] == 0:
                flag0 = True
            elif bboxes[index][4] == 2:
                flag1 = True
            else:
                flag2 = True
        #original image
        img_name = img_id + ".jpg"
       	save_path = train_aug_path
        save_path = os.path.join(save_path, img_name)
        imgano = build_imgano(save_path, img_id, cat_list, bboxes)
        new_anno['imgs'][img_id] = imgano
        img = cv2.imread(img_path)
        img_name = img_id + ".jpg"
        cv2.imwrite(save_path, img)
        if flag0 == False and flag1 == False:
            skip_num += 1
            print('skip image', skip_num) 
            with open(new_anno_json_path, "w") as f:
                f.write(json.dumps(new_anno, ensure_ascii=False, indent=4, separators=(',', ':')))
            continue
        #data aug
        for i in range(10):
            seq = Sequence(
                [RandomHSV(10, 10, 10), RandomHorizontalFlip(0.5), RandomScale(0.3), RandomTranslate(0.2)])
            augimg, augbboxes_ = seq(img.copy(), bboxes.copy())
            if(check_bbx(augbboxes_)):
                continue
            aug_id = img_id + "_" + str(i+1)
            aug_name = aug_id + ".jpg"
            aug_path = os.path.join(train_aug_path, aug_name)
            augimgano = build_imgano(aug_path, aug_id, cat_list, augbboxes_)
            new_anno['imgs'][aug_id] = augimgano
            cv2.imwrite(aug_path, augimg)
        with open(new_anno_json_path, "w") as f:
            f.write(json.dumps(new_anno, ensure_ascii=False, indent=4, separators=(',', ':')))

