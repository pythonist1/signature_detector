import cv2
import torch
import pathlib
import numpy as np

from word_detector_original_package.src.dataloader import DataLoaderImgFile, DataLoaderItem
from word_detector_original_package.src.eval import evaluate
from word_detector_original_package.src.net import WordDetectorNet

from signature_detector.domain import AbstractWordDetectorAdapter

path = str(pathlib.Path(__file__).parent)


class DataLoaderImgBytes(DataLoaderImgFile):
    def __init__(self, image_bytes, input_size, device, max_side_len=1024):
        self.fn_imgs = [image_bytes]
        self.input_size = input_size
        self.device = device
        self.max_side_len = max_side_len

    def __getitem__(self, item):
        image_np = np.frombuffer(self.fn_imgs[item], np.uint8)
        orig = cv2.imdecode(image_np, cv2.IMREAD_GRAYSCALE)
        f = min(self.max_side_len / orig.shape[0], self.max_side_len / orig.shape[1])
        if f < 1:
            orig = cv2.resize(orig, dsize=None, fx=f, fy=f)
        img = np.ones((self.ceil32(orig.shape[0]), self.ceil32(orig.shape[1])), np.uint8) * 255
        img[:orig.shape[0], :orig.shape[1]] = orig

        img = (img / 255 - 0.5).astype(np.float32)
        imgs = img[None, None, ...]
        imgs = torch.from_numpy(imgs).to(self.device)
        return DataLoaderItem(imgs, None, None)


class WordDetectorAdapter(AbstractWordDetectorAdapter):
    def __init__(self):
        net = WordDetectorNet()
        net.load_state_dict(torch.load(path + '/model/weights', map_location='cpu'))
        net.eval()
        net.to('cpu')
        self._net = net

    def detect_signatures(self, image_bytes):
        loader = DataLoaderImgBytes(image_bytes, self._net.input_size, 'cpu')
        res = evaluate(self._net, loader, max_aabbs=1000)

        for i, (img, aabbs) in enumerate(zip(res.batch_imgs, res.batch_aabbs)):
            return len(aabbs)
