import subprocess
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import os.path

# Extract the audio
if not os.path.isfile('audio.wav'):
        command = 'ffmpeg -i aiyoutube.mp4 -ab 160k -ar 44100 -vn audio.wav'
        subprocess.call(command, shell=True)

# Setup Speech to Text Service
apikey = 'bzIPr03MI_7tfb7_VVyQTpofWFdeCh4KglyV-exz4Px2'
url = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/1bf6cb45-238b-4dc4-b0d4-c8f01bea69dd'

authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

# open audio source and convert
with open('audio.wav', 'rb') as f:
        res = stt.recognize(audio=f, content_type='audio/wav', model='en-AU_NarrowbandModel', continuous=True).get_result()


# if not pickleFile.is_file():
#         # if no pickle-file, open audio file and convert
#         print('no pickle file')
#         with open('audio.wav', 'rb') as f:
#                 res = stt.recognize(audio=f, content_type='audio/wav', model='en-AU_NarrowbandModel', continuous=True).get_result()
#         with open(pickleFile, 'wb') as pickle_handle:
#                 pickle.dump(res, pickle_handle)
# else:
#         print('pickle file exists')
#         # else extract results from dataset
#         with open(pickleFile, 'rb') as pickle_handle:
#                 res = pickle.load(pickle_handle)

print(json.dumps(res, sort_keys=True, indent=2) )

# process results and output to text
text = [result['alternatives'][0]['transcript'].rstrip() + '.\n' for result in res['results']]

# remove whitespace/ concatenate
text = [para[0].title() + para[1:] for para in text]
transcript = ''.join(text)
with open('output.text', 'w') as out:
        out.writelines(transcript)