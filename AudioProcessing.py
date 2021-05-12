import moviepy.editor as mpe
from Utils import HiddenPrints, count_frames
import os
import speech_recognition as sr
from MaskRCNN import wordInDict, index_dict


## This function takes the path to the video and creates an array where each element in the array denotes which objects to mask on that frame.
def get_objs_to_mask(videoPath):
    num_frames = count_frames(videoPath)
    #print(num_frames)
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
        try:
            allWords = r.recognize_google(r.record(source))
        except Exception:
            print("Audio could not be processed. Please make sure the audio is clear and words are being said before trying again.")
            exit()
        allWords = allWords.split(" ")

        if not (('abracadabra' in allWords) or ('Abracadabra' in allWords)):
            print("Magic word was never said. No magic can be done :(")
            print("If you believe this is an error, please make sure 'abracadabra' is said clearly and distinctly.")
            exit()

        for i in range(len(allWords)):
            try:
                if allWords[i].lower() == "abracadabra":
                    if wordInDict(allWords[i + 1]):
                        incomingMaskings.append(allWords[i + 1])
            except:
                print("ea sports. its in the game")
                pass

    if not incomingMaskings:
        print("The object(s) you are trying to mask are not currently supported. The list of supported objects are:")
        print(index_dict.keys())

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
        out_clip.close()
    #os.remove(outputVideoPath)
    return
