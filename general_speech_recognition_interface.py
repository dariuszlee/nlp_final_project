#!/usr/bin/env python3

from autocorrect import Speller
from tqdm import tqdm
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import csv
import speech_recognition as sr
from lyric_interface import get_all_lyrics_from_file
from deepspeech_interface import DeepSpeechModel
from os import path, listdir
import os.path

auto_corrector = Speller(lang='en')
output_dir = "output/"
prefix = "seg.1."
postfix = ".wav"

damp_dir = "damp_data/"

def get_sorted_segments(song):
    song_dir = song + "/"

    dat = listdir(output_dir + song + "/")
    dat2 = [ int(d[len(prefix):-len(postfix)]) for d in dat if d[0:3] == 'seg']
    dat2.sort()
    audio_files =  [path.join(path.dirname(path.realpath(__file__)), output_dir + song_dir + prefix + str(files) + postfix) for files in dat2]
    return audio_files

def read_segmented_directory(song):
    song_dir = song + "/"

    dat2 = get_sorted_segments(song)

    google_recognize_output = []
    for audio_file in dat2:
        sentence = recognize_google(audio_file)
        if sentence is not None:
            google_recognize_output.append(sentence)
    return google_recognize_output

def recognize_google(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)  # read the entire audio file

    try:
        recognition = r.recognize_google(audio)
        return recognition
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

def recognize_deepspeech(deepspeech_model, input_audio):
    recognition = deepspeech_model.infer(input_audio) 
    if recognition is not None:
        recognition = auto_corrector(recognition)
        return recognition
    return ""


def load_karoke():
    damp_data_files = [i for i in listdir(damp_dir) if i[0:2] == 'v3']
    damp_info = {}
    with open(damp_dir + "/info.txt") as f:
        csv_file = csv.reader(f, delimiter=' ')
        for line in csv_file:
            damp_info[line[0]] = line[1:]
    return damp_info, damp_data_files


def recognize_pocketsphinx(file_path):
    model_path = get_model_path()
    data_path = get_data_path()
    config = {
            'hmm': os.path.join(model_path, 'en-us'),
            'lm': os.path.join(model_path, 'en-us.lm.bin'),
            'dict': os.path.join(model_path, 'cmudict-en-us.dict')
            }
    psModel = Pocketsphinx(**config)
    psModel.decode(audio_file=file_path, buffer_size=2048, no_search=False, full_utt=False) 
    seq = psModel.hypothesis()
    return seq


def compare_sentences(ref, test):
    tfidf = TfidfVectorizer(min_df=1, stop_words="english").fit_transform([ref, test])
    # print(tfidf)
    similarity = tfidf * tfidf.T
    return similarity[0,1]




def tom_petty_analysis():
    deepspeech_model = DeepSpeechModel("./deepspeech-0.6.1-models/output_graph.pbmm")

    song_lyric_list = get_all_lyrics_from_file()
    
    count = 0
    google_total_score = 0
    deepspeech_total_score = 0
    for song in tqdm(song_lyric_list):
        song_name = song[0]
        song_lyrics = " ".join(song[1])
        segs = get_sorted_segments(song_name)

        deep_speech_lyrics = []
        google_speech_lyrics = []
        for audio_file in segs:
            deepsheech_out = recognize_deepspeech(deepspeech_model, audio_file)
            deep_speech_lyrics.append(deepsheech_out)
            google_out = recognize_google(audio_file)
            google_speech_lyrics.append(google_out)

        google_merged = " ".join(google_speech_lyrics)
        google_score = compare_sentences(song_lyrics, google_merged)
        google_total_score += google_score

        deepspeech_merged = " ".join(deep_speech_lyrics)
        deepspeech_score = compare_sentences(song_lyrics, deepspeech_merged)
        deepspeech_total_score += deepspeech_score

        count += 1
    
    deepspeech_averaged_score = deepspeech_total_score / count
    google_averaged_score = google_total_score / count
    with open("./results/tom_petty_results.txt", "w") as f:
        f.write("Deepspeech average {}\n".format(deepspeech_averaged_score))
        f.write("Google average {}\n".format(google_averaged_score))


def damp_data_analysis():
    count = 0
    google_total_score = 0
    deepspeech_total_score = 0
    pocketsphinx_total_score = 0

    deepspeech_model = DeepSpeechModel("./deepspeech-0.6.1-models/output_graph.pbmm")
    info, data = load_karoke()
    for f in tqdm(data):
        damp_song = damp_dir + f
        reference_out = " ".join(info[f[:-4]])

        google_out = recognize_google(damp_song) 
        google_diff = compare_sentences(reference_out, google_out)
        deepspeech_output = recognize_deepspeech(deepspeech_model, damp_song)    
        deepspeech_diff = compare_sentences(reference_out, deepspeech_output)
        pocketsphinx_out = recognize_pocketsphinx(damp_song) 
        pocketsphinx_diff = compare_sentences(reference_out, pocketsphinx_out)

        google_total_score += google_diff
        deepspeech_total_score += deepspeech_diff
        pocketsphinx_total_score += pocketsphinx_diff
        count += 1

    with open("./results/damp_results.txt", "w") as f:
        print("---- GOOGLE TOTAL SCORE ----", file=f)
        print(google_total_score / count, file=f)
        print("", file=f)
        print("", file=f)
        print("---- DEEPSPEECH TOTAL SCORE ----", file=f)
        print(deepspeech_total_score / count, file=f)
        print("", file=f)
        print("", file=f)
        print("---- POCKETSPHINX TOTAL SCORE ----", file=f)
        print(pocketsphinx_total_score / count, file=f)


def main():
    tom_petty_analysis()
    damp_data_analysis()


if __name__ == "__main__":
    main()
