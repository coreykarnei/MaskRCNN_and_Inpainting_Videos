from Utils import print_update, convert_frames_to_video
from Inpainting import inpaint_all_frames
from MaskRCNN import generate_masks_from_video
from AudioProcessing import add_audio_to_video
import os
import sys
import argparse
import warnings
from AudioProcessing import get_objs_to_mask
import time

warnings.filterwarnings("ignore", category=Warning)

parser = argparse.ArgumentParser()
parser.add_argument('--video', default='', type=str,
                    help='The location of the Video to be operated on.')
parser.add_argument('--inflation', default=5, type=int,
                    help='Number of pixels to inflate the object mask.')
parser.add_argument('--minConfidence', default=0.5, type=float,
                    help='The minimum confidence MaskRCNN needs to consider an object mask valid.')


if __name__ == "__main__":
    args, unknown = parser.parse_known_args()

    videoPath = args.video
    minConfidence = args.minConfidence
    inflation = args.inflation

    if not os.path.exists(videoPath):
        sys.exit("Could not locate video '" + videoPath + "'")

    try:
        os.mkdir('output/')
    except Exception:
        pass

    print("Looking for Magic Words in audio...")
    objectsToMask = get_objs_to_mask(videoPath)

    print("Magic Word(s) found. Masking objects from the video...")
    fps = generate_masks_from_video(videoPath, objectsToMask, minConfidence, inflation)

    print("Masking completed. Painting out masked objects...")
    inpaint_all_frames(videoPath)

    print("Inpainting completed. Compiling to video...")
    compiledPath = convert_frames_to_video(videoPath, fps)
    add_audio_to_video(videoPath, compiledPath, fps)

    #remove soundless video
    os.remove(compiledPath)

    print("Compiled! to " + compiledPath[:-3] + 'mp4')
