import cv2
import sys
import os
import glob
import natsort
import traceback

def convert_frames_to_video(videoPath, fps):
    videoName = videoPath.split(".")[0].split('/')[-1]
    filesLocation = "output/" + videoName + "/*"

    fileNames = []

    # get paths to frames for video
    for name in [os.path.normpath(i) for i in glob.glob(filesLocation)]:
        if name.split('.')[0][-3:] == "out":
            fileNames.append(name)

    fileNames = natsort.natsorted(fileNames)

    frame_array = []
    size = (256, 256)
    # combine frames and create video
    for filename in fileNames:
        img = cv2.imread(filename)
        # inserting the frames into an image array
        height, width, layers = img.shape
        size = (width, height)
        frame_array.append(img)
    outFName = "output/" + videoName + "_out.avi"

    out = cv2.VideoWriter(outFName, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        try:
            out.write(frame_array[i])
        except Exception:
            print(traceback.format_exception())
    out.release()
    return outFName


def print_update(objects_to_mask):
    bar = "Video loaded. Masking "

    toPrint = []
    for obj in objects_to_mask[-1]:

        if obj:
            toPrint.append(obj)

    if len(toPrint) == 1:
        foo = toPrint[0] + "(s)"
    elif len(toPrint) < 3:
        foo = toPrint[0] + "(s) and " + toPrint[1] + "(s)"
    else:
        foo = ""
        for i in range(len(toPrint)):
            if not i == len(toPrint) - 1:
                foo = foo + toPrint[i] + "(s), "
            else:
                foo = foo + "and " + toPrint[i] + "(s)"
    print(bar + foo + "...")
    return


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def count_frames(videoPath):
    cap = cv2.VideoCapture(videoPath)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    i = 0
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == False:
            break

        i = i + 1

    # When everything done, release the video capture object
    cap.release()

    return i
