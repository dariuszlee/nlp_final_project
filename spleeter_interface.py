from tqdm import tqdm
import os
import subprocess

from silence_removal.segment import segmentize

def main():
    """TODO: Docstring for main.

    :arg1: TODO
    :returns: TODO

    """
    output_path = "output/"
    data_path = "data/"

    proc_exits = []
    for song in tqdm(os.listdir(data_path)):
        song_path = data_path + song
        to_run = "spleeter separate -i {path} -p spleeter:2stems -o {output_path}".format(path=song_path, output_path=output_path).split(" ")
        p = subprocess.Popen(to_run)
        exit_code = p.wait()
        proc_exits.append((exit_code, song_path))

        output_song_directory = (output_path + song)[:-4]
        output_song_vocals = output_song_directory + "/vocals.wav"
        if exit_code == 0:
            segmentize(output_song_vocals, output_song_directory + "/seg") 

if __name__ == "__main__":
    main()
