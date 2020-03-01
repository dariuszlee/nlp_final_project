# Set-Up and Run (requires conda latest (python 3.7.6 at this time))

1. conda create -n spleeter -c conda-forge spleeter-gpu (remove '-gpu' if you don't have a gpu)

    - conda activate spleeter

    - pip install tqdm

    - source activate spleeter 

    - python ./spleeter_interface.py

2. conda create -n tensor_flow tensorflow-gpu cudatoolkit=10.0 (remove '-gpu' if you don't have a gpu)

        - pip install deepspeech

        - pip install tqdm

        - pip install SpeechRecognition
        
        - pip install bs4

        - pip install sklearn

        - pip install autocorrect

        - pip install ntlk

        - pip install sox
        
        - wget https://github.com/mozilla/DeepSpeech/releases/download/v0.6.1/deepspeech-0.6.1-models.tar.gz

        - tar -xf ./deepspeech-0.6.1-models.tar.gz

        - cd ./damp_data && unzip *.zip

        - python ./general_speech_recognition_interface.py

3. Once completed, you should see the two test statistics in the result folder


# Some Data Sources

1. Tom Petty Greatest Hits

2. Karaoke training set:
https://drive.google.com/drive/folders/1hGuE0Drv3tbN-YNRDzJJMHfzKH6e4O2A

