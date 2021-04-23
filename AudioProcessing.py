import moviepy.editor as mpe
from Utils import HiddenPrints, count_frames
import os
import speech_recognition as sr


def get_objs_to_mask(videoPath):
    num_frames = count_frames(videoPath)
    videoSound = mpe.AudioFileClip(videoPath)
    with HiddenPrints():
        videoSound.write_audiofile(videoPath[:-3] + "wav")

    with sr.WavFile(videoPath[:-3] + "wav") as source:
        file_duration = source.DURATION

    frame_duration = file_duration / num_frames

    sound = sr.AudioFile(videoPath[:-3] + "wav")
    r = sr.Recognizer()

    incomingMaskings = []
    with sound as source:
        allWords = r.recognize_google(r.record(source))
        allWords = allWords.split(" ")

        for i in range(len(allWords)):
            if allWords[i].lower() == "abracadabra":
                incomingMaskings.append(allWords[i + 1])

    confirmedMaskings = []
    objectsToMask = []

    for i in range(num_frames):
        with sound as source:
            try:
                spokenPhrase = r.recognize_google(r.record(sound, offset=(i * frame_duration)))
                #print(spokenPhrase + " " + str(i))
                confirmedMaskings, incomingMaskings = update_confirmed_maskings(incomingMaskings, spokenPhrase,
                                                                                confirmedMaskings)
            except Exception as e:
                spokenPhrase = ""
                confirmedMaskings, incomingMaskings = update_confirmed_maskings(incomingMaskings, spokenPhrase,
                                                                                confirmedMaskings)
                #print("Could not understand audio " + str(i))

        currentRoundMaskings = ""
        for entry in confirmedMaskings:
            currentRoundMaskings = currentRoundMaskings + entry + ","
        objectsToMask.append(currentRoundMaskings)
    os.remove(videoPath[:-3] + "wav")
    return objectsToMask

def update_confirmed_maskings(incoming, currentSound, confirmed):
    #print(currentSound, incoming)
    for word in incoming:
        if not word in currentSound:
            #print(word, currentSound)
            confirmed.append(word)
            incoming.remove(word)
    return confirmed, incoming


def get_audio(videoPath):
    return mpe.AudioFileClip(videoPath)


def add_audio_to_video(originalVideoPath, outputVideoPath, fps):
    orig_audio = get_audio(originalVideoPath)
    with HiddenPrints():
        out_clip = mpe.VideoFileClip(outputVideoPath)
        final_clip = out_clip.set_audio(orig_audio)
        final_clip.write_videofile(outputVideoPath[:-3] + 'mp4', fps=fps)
    #os.remove(outputVideoPath)
    return
