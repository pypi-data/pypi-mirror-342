import pathlib
import torch
import torch.nn.functional as F
import cv2
import numpy as np

from yolo_inference.models.common import DetectMultiBackend
from yolo_inference.utils.general import check_img_size, Profile, non_max_suppression, scale_boxes, xyxy2xywh
from yolo_inference.utils.dataloaders import LoadImages
from yolo_inference.utils.augmentations import classify_transforms
from yolo_inference.utils.segment.general import process_mask
from yolo_inference.utils.torch_utils import select_device

# temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath

device = select_device(device='')


def mask2polygon(mask_values):
    """"""
    contours, hierarchy = cv2.findContours(mask_values.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    segmentation = []
    for contour in contours:
        contour_list = contour.flatten().tolist()
        if len(contour_list) > 4:
            segmentation.append(contour_list)
    return segmentation


class ObjectDetection:

    def __init__(self, weights):
        self.model = DetectMultiBackend(weights, device=device, dnn=False, fp16=False)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.img_size = check_img_size((640, 640), s=self.stride)
        self.model.warmup(imgsz=1)

    def inference(self, source):
        dataset = LoadImages(source, img_size=self.img_size, stride=self.stride, auto=self.pt, vid_stride=1)
        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
        for path, im, im0s, vid_cap, s in dataset:
            with dt[0]:
                im = torch.from_numpy(im).to(self.model.device)
                im = im.half() if self.model.fp16 else im.float()
                im /= 255
                if len(im.shape) == 3:
                    im = im[None]
            with dt[1]:
                pred = self.model(im, augment=False, visualize=False)
            with dt[2]:
                pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45, classes=None, agnostic=False,
                                           max_det=50)

            for i, det in enumerate(pred):
                seen += 1
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

                s += '%gx%g ' % im.shape[2:]
                # gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                # print(len(det))
                if len(det):
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                predictions = []
                for result in det:
                    prediction = {'pred_box': result[:4].tolist(), 'confidence_score': float(result[4]),
                                  'pred_class': int(result[5])}
                    predictions.append(prediction)
                return predictions


class Classification:

    def __init__(self, weights):
        self.model = DetectMultiBackend(weights, device=device, dnn=False, fp16=False)
        self.stride, self.names, pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size((224, 224), s=self.stride)
        self.model.warmup(imgsz=1)

    def inference(self, source):
        dataset = LoadImages(source, img_size=self.imgsz, transforms=classify_transforms(self.imgsz[0]), vid_stride=1)
        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
        for path, im, im0s, vid_cap, s in dataset:
            with dt[0]:
                im = torch.Tensor(im).to(self.model.device)
                im = im.half() if self.model.fp16 else im.float()  # uint8 to fp16/32
                if len(im.shape) == 3:
                    im = im[None]
            # Inference
            with dt[1]:
                results = self.model(im)
            # Post-process
            with dt[2]:
                pred = F.softmax(results, dim=1)  # probabilities
        # Process predictions
        predictions = []
        for i, prob in enumerate(pred):
            seen += 1
            top5i = prob.argsort(0, descending=True)[:5].tolist()
            for j in top5i:
                pred_dict = {'pred_class': self.names[j], 'confidence_score': float(prob[j])}
                predictions.append(pred_dict)
        return predictions


class Segmentation:

    def __init__(self, weights):
        self.model = DetectMultiBackend(weights, device=device, dnn=False, fp16=False)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size((640, 640), s=self.stride)  # check image size
        self.model.warmup(imgsz=1)

    def inference(self, source):
        image = cv2.imread(source)
        dataset = LoadImages(source, img_size=self.imgsz, stride=self.stride, auto=self.pt, vid_stride=1)

        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
        for path, im, im0s, vid_cap, s in dataset:
            with dt[0]:
                im = torch.from_numpy(im).to(self.model.device)
                im = im.half() if self.model.fp16 else im.float()
                im /= 255
                if len(im.shape) == 3:
                    im = im[None]
            with dt[1]:
                pred, proto = self.model(im, augment=False, visualize=False)[:2]
            with dt[2]:
                pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000, nm=32)
            for i, det in enumerate(pred):  # per image
                seen += 1
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
                if len(det):
                    masks = process_mask(proto[i], det[:, 6:], det[:, :4], im.shape[2:], upsample=True)
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
                pred_classes, scores, pred_boxes, polygons = [], [], [], []
                for index, det_ele in enumerate(det):
                    det_ele = det_ele.numpy()
                    pred_classes.append((int(det_ele[5])))
                    scores.append(str(det_ele[4]))
                    pred_boxes.append(det_ele[:4].astype('int').tolist())
                    resized_mask = cv2.resize(masks[index].numpy(), (image.shape[1], image.shape[0])).astype('int')
                    polygons.append(mask2polygon(resized_mask))
                results = {
                    'pred_class': pred_classes, 'score': scores, 'pred_boxes': pred_boxes, 'polygon': polygons
                }
                return results


class SegmentationGPU:

    def __init__(self, weights):
        self.model = DetectMultiBackend(weights, device=device, dnn=False, fp16=False)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size((640, 640), s=self.stride)  # check image size
        self.model.warmup(imgsz=(1 if self.pt else bs, 3, *self.imgsz))

    def inference(self, source):
        image = cv2.imread(source)
        dataset = LoadImages(source, img_size=self.imgsz, stride=self.stride, auto=self.pt, vid_stride=1)

        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
        for path, im, im0s, vid_cap, s in dataset:
            with dt[0]:
                im = torch.from_numpy(im).to(self.model.device)
                im = im.half() if self.model.fp16 else im.float()
                im /= 255
                if len(im.shape) == 3:
                    im = im[None]
            with dt[1]:
                pred, proto = self.model(im, augment=False, visualize=False)[:2]
            with dt[2]:
                pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000, nm=32)
            for i, det in enumerate(pred):  # per image
                seen += 1
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
                if len(det):
                    masks = process_mask(proto[i], det[:, 6:], det[:, :4], im.shape[2:], upsample=True)
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
                pred_classes, scores, pred_boxes, polygons = [], [], [], []
                for index, det_ele in enumerate(det):
                    det_ele = det_ele.cpu().numpy()
                    pred_classes.append((int(det_ele[5])))
                    scores.append(str(det_ele[4]))
                    pred_boxes.append(det_ele[:4].astype('int').tolist())
                    resized_mask = cv2.resize(masks[index].cpu().numpy(), (image.shape[1], image.shape[0])).astype('int')
                    polygons.append(mask2polygon(resized_mask))
                results = {
                    'pred_class': pred_classes, 'score': scores, 'pred_boxes': pred_boxes, 'polygon': polygons
                }
                return results

