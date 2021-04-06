from Utils import print_update, convert_frames_to_video
from Inpainting import inpaint_all_frames
from MaskRCNN import generate_masks_from_video
import os
import sys
import argparse
import warnings

warnings.filterwarnings("ignore", category=Warning)

parser = argparse.ArgumentParser()
parser.add_argument('--video', default='', type=str,
                    help='The location of the Video to be operated on.')
parser.add_argument('--objects', default='', type=str,
                    help='The objects to mask from video, separated by a comma.')


if __name__ == "__main__":
    args, unknown = parser.parse_known_args()

    videoPath = args.video
    objectsToMask = args.objects
    objectsToMask = objectsToMask.split(",")
    for i in range(len(objectsToMask)):
        objectsToMask[i] = objectsToMask[i].strip()

    if not os.path.exists(videoPath):
        sys.exit("Could not locate video '" + videoPath + "'")

    try:
        os.mkdir('output/')
    except Exception:
        pass

    print_update(objectsToMask)
    fps = generate_masks_from_video(videoPath, objectsToMask)

    print("Masking completed. Painting out masked objects...")
    inpaint_all_frames(videoPath)

    print("Inpainting completed. Compiling to video...")
    compiledPath = convert_frames_to_video(videoPath, fps)

    print("Compiled! to " + compiledPath)
