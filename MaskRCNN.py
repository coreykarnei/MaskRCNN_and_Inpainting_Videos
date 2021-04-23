import mxnet as mx
from gluoncv import model_zoo, data, utils
import cv2
import os
import numpy as np
from Utils import HiddenPrints
import copy

THRESHOLD = 0.2   # This value indicates the minimum confidence that a given mask needs for the model to consider it valid
INFLATE_SIZE = 5  # This value is the size of the circle that will be drawn on each pixel of the mask in order to inflate it

index_dict = {'person': 0, 'bicycle': 1, 'car': 2, 'motorcycle': 3, 'airplane': 4, 'bus': 5, 'train': 6, 'truck': 7,
              'boat': 8, 'traffic light': 9, 'fire hydrant': 10, 'stop sign': 11,
              'parking meter': 12, 'bench': 13, 'bird': 14, 'cat': 15, 'dog': 16, 'horse': 17, 'sheep': 18, 'cow': 19,
              'elephant': 20, 'bear': 21, 'zebra': 22, 'giraffe': 23, 'backpack': 24, 'umbrella': 25,
              'handbag': 26, 'tie': 27, 'suitcase': 28, 'frisbee': 29, 'skis': 30, 'snowboard': 31, 'sports ball': 32,
              'kite': 33, 'baseball bat': 34, 'baseball glove': 35, 'skateboard': 36, 'surfboard': 37,
              'tennis racket': 38,
              'bottle': 39, 'wine glass': 40, 'cup': 41, 'fork': 42, 'knife': 43, 'spoon': 44, 'bowl': 45, 'banana': 46,
              'apple': 47, 'sandwich': 48, 'orange': 49, 'broccoli': 50, 'carrot': 51, 'hot dog': 52, 'pizza': 53,
              'donut': 54,
              'cake': 55, 'chair': 56, 'couch': 57, 'potted plant': 58, 'bed': 59, 'dining table': 60, 'toilet': 61,
              'tv': 62, 'laptop': 63, 'mouse': 64, 'remote': 65, 'keyboard': 66, 'cell phone': 67, 'microwave': 68,
              'oven': 69,
              'toaster': 70, 'sink': 71, 'refrigerator': 72, 'book': 73, 'clock': 74, 'vase': 75, 'scissors': 76,
              'teddy bear': 77, 'hair drier': 78, 'toothbrush': 79}


def generate_masks_from_video(videoPath, objectsToMask):
    with HiddenPrints():
        mrcnn = model_zoo.get_model("mask_rcnn_fpn_resnet101_v1d_coco", pretrained=True)

    cap = cv2.VideoCapture(videoPath)

    fps = cap.get(cv2.CAP_PROP_FPS)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    # Read until video is completed

    frameName = videoPath.split(".")[0].split('/')[-1]

    try:
        os.mkdir('output/' + frameName)
    except Exception:
        pass

    i = 0
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == False:
            break

        generate_mask_from_image(frame, objectsToMask[i], frameName, i, mrcnn)

        i = i + 1

    # When everything done, release the video capture object
    cap.release()

    return fps


def generate_mask_from_image(frame, objectsToMask, frameName, frameIndex, model):
    ## Inputs:
    ##       image_path: string path to image to be operated on
    ##       objects_to_remove: list of object names to be masked
    ##       model: the MaskRCNN model
    ## Outputs:
    ##       input image
    ##       mask image
    ## both images serve as input to the inpainting model

    height, width, channels = frame.shape

    frame = mx.nd.array(frame)
    x, orig_img = data.transforms.presets.rcnn.transform_test(frame, short=256)

    #print(objectsToMask)
    if objectsToMask == "":
        frameNameFrameIndex = frameName + str(frameIndex)
        cv2.imwrite('output/' + frameName + '/' + frameNameFrameIndex + '_input.png', orig_img)
        blackFrame = copy.deepcopy(orig_img)
        j = 0
        for row in blackFrame:
            i = 0
            for element in row:
                row[i] = [0,0,0]
                i = i + 1
            # print(row)
            j = j + 1
        cv2.imwrite('output/' + frameName + '/' + frameNameFrameIndex + '_mask.png', blackFrame)

    else:
        objectsToMask = objectsToMask.split(",")
        for i in range(len(objectsToMask)):
            objectsToMask[i] = objectsToMask[i].strip()



        # inference is done here
        ids, scores, bboxes, masks = [xx[0].asnumpy() for xx in model(x)]

        for i in range(scores.size):
            if (scores[i] > THRESHOLD) & (scores[i] < 0.5):
                scores[i] = 0.51

        ids, scores, bboxes, masks = remove_undesired_objects(objectsToMask, ids, scores, bboxes, masks)

        width, height = orig_img.shape[1], orig_img.shape[0]
        masks = utils.viz.expand_mask(masks, bboxes, (width, height), scores)

        # masked_img = create_mask_img(masks, orig_img)
        input_img, masked_img = create_input_for_inpainting(masks, orig_img)

        frameNameFrameIndex = frameName + str(frameIndex)

        # input_img, masked_img = cv2.resize(input_img, desiredOutputSize ), cv2.resize(masked_img, desiredOutputSize)

        cv2.imwrite('output/' + frameName + '/' + frameNameFrameIndex + '_mask.png', masked_img)
        cv2.imwrite('output/' + frameName + '/' + frameNameFrameIndex + '_input.png', input_img)


def remove_undesired_objects(objects_to_remove, ids, scores, bboxes, masks):
    desired_object_ids = []
    for obj in objects_to_remove:
        if obj:
            desired_object_ids.append(index_dict.get(obj))

    ids_to_remove = []

    for i in range(ids.size):
        if desired_object_ids.count(int(ids[i])) == 0:
            ids_to_remove.append(i)

    ids = np.delete(ids, ids_to_remove)
    scores = np.delete(scores, ids_to_remove)
    bboxes = np.delete(bboxes, ids_to_remove, 0)
    masks = np.delete(masks, ids_to_remove, 0)
    return ids, scores, bboxes, masks


def create_input_for_inpainting(masks, original_image):
    img_pre_output = original_image.copy()
    for mask in masks:
        j = 0
        for row in img_pre_output:
            i = 0
            for element in row:
                if (mask[j, i] != 0):
                    row[i] = [255, 255, 255]
                i = i + 1
            # print(row)
            j = j + 1
    img_output = img_pre_output.copy()
    j = 0
    for row in img_pre_output:
        i = 0
        for element in row:
            if np.array_equal(element, [255, 255, 255]):
                if not only_one_white_pixel(img_pre_output, i, j):
                    img_output = cv2.circle(img_output, (i, j), INFLATE_SIZE, (255, 255, 255), 0)
            i = i + 1
        j = j + 1

    mask_output = img_output.copy()
    j = 0
    for row in mask_output:
        i = 0
        for element in row:
            if not np.array_equal(element, [255, 255, 255]):
                row[i] = [0, 0, 0]
            i = i + 1
        # print(row)
        j = j + 1

    return img_output, mask_output


def only_one_white_pixel(img, i, j):
    try:
        if np.array_equal( img[j+1][i],  [255,255,255]):
            return False
    except:
        pass
    try:
        if np.array_equal( img[j-1][i],  [255,255,255]):
            return False
    except:
        pass
    try:
        if np.array_equal( img[j][i+1],  [255,255,255]):
            return False
    except:
        pass
    try:
        if np.array_equal( img[j][i-1],  [255,255,255]):
            return False
    except:
        pass

    return True
