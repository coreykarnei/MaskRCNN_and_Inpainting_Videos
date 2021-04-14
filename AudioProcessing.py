import moviepy.editor as mpe
from Utils import HiddenPrints

def get_audio(videoPath):
    return mpe.AudioFileClip(videoPath)


def add_audio_to_video(originalVideoPath, outputVideoPath, fps):
    orig_audio = get_audio(originalVideoPath)
    with HiddenPrints():
        out_clip = mpe.VideoFileClip(outputVideoPath)
        final_clip = out_clip.set_audio(orig_audio)
        final_clip.write_videofile(outputVideoPath[:-3] + 'mp4', fps=fps)
    return
