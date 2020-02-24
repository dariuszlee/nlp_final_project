from tqdm import tqdm
import os
import subprocess

def main():
    """TODO: Docstring for main.

    :arg1: TODO
    :returns: TODO

    """
    proc_exits = []
    for song in tqdm(os.listdir("./data/")):
        song_path = "./data/" + song
        to_run = "spleeter separate -i {path} -p spleeter:2stems -o output".format(path=song_path).split(" ")
        print(to_run)
        p = subprocess.Popen(to_run)
        proc_exits.append(p.wait())

if __name__ == "__main__":
    main()
