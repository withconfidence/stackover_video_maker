# TextToSpeech.py
# Called in run.py after RedditScrape.py has scraped all of the content 
# Creates an audio file for each scraped post 
#
#





#including the text to speech API: subject to change
from gtts import gTTS

import os
import sys
sys.path.append("../")


class TextToSpeech:

    def __init__(self):
        self.audio_path = '../audio/' 
        self.create_dir() # Creates the directory to hold audio if not already specified 


    def create_dir(self):
        '''Creates the dir to hold the audio files if it doesnt already exist'''
        try: 
            os.makedirs(self.audio_path)
            print(f'directory: {self.audio_path} created')
        except FileExistsError:
            pass




    def create_tts(self, posts):
        '''Takes the list of posts and creates text to speech audio for each one
        places them in the audio_path directory...
        the 0th index of posts is the title so we explicitly name it title.mp3'''

        def export_audio(text, fp):
            text_grp = []
            word_list = text.split(" ")
            par = ""
            for i, wd in enumerate(word_list):
                par_len = len(par)
                wd_len = len(wd)
                if par_len + wd_len + 1 < 100:
                    par += " {}".format(wd)


                else:
                    text_grp.append(par)
                    par = wd
                if i+1 == len(word_list):
                    text_grp.append(par)
            for sub_text in text_grp:
                # print("length = ", len(sub_text))
                # print(sub_text)
                try:
                    gTTS(text=sub_text, lang='en').write_to_fp(fp)
                except:
                    pass
        
        title_file = f'{self.audio_path}title.mp3'
        print("writing title audio file...")
        if os.path.exists(title_file):
            os.remove(title_file)
        # Creating the title tts first
        with open(title_file, 'ab') as f:
            export_audio(posts[0], f)
            # gTTS(text=posts[0], lang='en').write_to_fp(f)

        # Creating tts for the replies next
        print("writing reply audio files...")

        for i, reply in enumerate(posts[1:]):
            # Saving tts of replies as: reply0.mp3, reply1.mp3, ... , replyn.mp3
            reply_file = f'{self.audio_path}reply{str(i)}.mp3'
            if os.path.exists(reply_file):
                os.remove(reply_file)
            with open(reply_file, 'ab') as f:
                export_audio(reply, f)
                # gTTS(text=reply, lang='en').write_to_fp(f)

