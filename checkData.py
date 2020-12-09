import os

class DatasetChecker:
    def __init__(self, path):
        self.path = path
    
    def check(self):
        image_train_path = os.path.join(self.path, "images", "train")
        image_val_path   = os.path.join(self.path, "images", "val")
        label_train_path = os.path.join(self.path, "labels", "train")
        label_val_path   = os.path.join(self.path, "labels", "val")

        assert os.path.exists(image_train_path), "%s not exist!" % image_train_path
        assert os.path.exists(image_val_path)  , "%s not exist!" % image_val_path
        assert os.path.exists(label_train_path), "%s not exist!" % label_train_path
        assert os.path.exists(label_val_path)  , "%s not exist!" % label_val_path

        image_train_files = set(os.listdir(image_train_path))
        image_val_files   = set(os.listdir(image_val_path))
        label_train_files = set(os.listdir(label_train_path))
        label_val_files   = set(os.listdir(label_val_path))

        assert len(image_train_files) == len(label_train_files), "train image and label number unconsistent! %d vs %d" % (len(image_train_files), len(label_train_files))
        assert len(image_val_files)   == len(label_val_files)  , "val image and label number unconsistent! %d vs %d" % (len(image_val_files), len(label_val_files))

        for f in image_train_files:
            name = f.split(".")[0]
            assert name + ".txt" in label_train_files, "train image %s with no label" % name

        for f in label_train_files:
            name = f.split(".")[0]
            assert name + ".jpg" in image_train_files, "train label %s with no image" % name

        for f in image_val_files:
            name = f.split(".")[0]
            assert name + ".txt" in label_val_files  , "val image %s with no label" % name

        for f in label_val_files:
            name = f.split(".")[0]
            assert name + ".jpg" in image_val_files  , "val label %s with no image" % name
        
        print("Everything is good!")
        return True


if __name__ == '__main__':
    c = DatasetChecker("/home/zlc/hackathon/bdd100k")
    c.check()