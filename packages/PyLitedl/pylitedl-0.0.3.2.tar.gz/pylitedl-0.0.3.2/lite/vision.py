import cv2
import numpy as np
from tensor import Tensor
import os

# Image Transformations
class Resize:
    def __init__(self, size):
        self.size = size

    def __call__(self, img):
        return cv2.resize(img, self.size)

class ToGray:
    def __call__(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

class Normalize:
    def __call__(self, img):
        return img / 255.0

class ToTensor:
    def __call__(self, img):
        return Tensor(img)

class Compose:
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, img):
        for t in self.transforms:
            img = t(img)
        return img

# Datasets
class ImageFolder:
    def __init__(self, root, transform=None):
        self.samples = []
        self.transform = transform
        classes = sorted(os.listdir(root))
        self.class_to_idx = {cls: i for i, cls in enumerate(classes)}

        for cls in classes:
            path = os.path.join(root, cls)
            for file in os.listdir(path):
                if file.lower().endswith(('.jpg', '.png')):
                    self.samples.append((os.path.join(path, file), self.class_to_idx[cls]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = cv2.imread(path)
        if self.transform:
            img = self.transform(img)
        return img, label
