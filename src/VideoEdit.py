# This clas will hold the class that edits the images into video
#TODO: Once complete, remove global import and only import required

from moviepy.editor import * # movie editor 
import os  # used for some file grabbing
from PIL import Image # Image library

class VideoEditor:
    def __init__(self,num_replies, video_name):
        self.num_replies = num_replies
        self.video_name = video_name
        self.image_path = '../images/'
        self.audio_path = '../audio/'
        self.save_path = '../edited_videos/'
        self.intro_clip = '../videos/intro.mp4'
        self.outro_clip = '../videos/outro.mp4'

        self.create_dir() # Creates the edited videos dir if it doesnt exist

        print(self.num_replies)


    def create_dir(self):
        '''Creates the dir to hold the edited video if it doesnt already exist'''
        try: 
            os.makedirs(self.save_path)
            print(f'directory: {self.save_path} created')
        except FileExistsError:
            pass

    def create_movie(self):
        '''
        Creates a .mp4 file for every text to speech and post
        will then combine every mp4 file for entire video
        can add transitions this way
        '''
        clips = [] # clips are mp4 clips to be combined to make entire movie
        clip_count = 0
        

        # Create audio file and image file, then combine and add to list of clips
        title_audio = AudioFileClip(self.audio_path + 'title.mp3')
        title_clip = ImageClip(self.image_path + 'title.jpeg').set_duration(title_audio.duration+0.5)
        title_mp4 = concatenate([title_clip], method="compose")
        new_audioclip = CompositeAudioClip([title_audio])

        title_mp4.audio = new_audioclip
        clips.append(title_mp4)

        # Loop through the rest of posts doing same thing above
        for i in range(0, self.num_replies):
            tmp_audio = AudioFileClip(f'{self.audio_path}reply{i}.mp3')
            tmp_dur = tmp_audio.duration
            tmp_clip = ImageClip(f'{self.image_path}reply{i}.jpeg').set_duration(tmp_dur + 0.5)
            tmp_mp4 = concatenate([tmp_clip], method='compose')
            tmp_mp3 = CompositeAudioClip([tmp_audio])
            tmp_mp4.audio = tmp_mp3

            clips.append(tmp_mp4)
            
        # clips.append(self.outro_clip)
        # Combina all clips, and combine into master video
        merged_clip_name = f'{self.save_path}merged_clips.mp4'
        final_vid_name = f'{self.save_path}{self.video_name}.mp4'

        merged_vid = concatenate(clips, method='compose')

        merged_vid.write_videofile(merged_clip_name,
          fps=10,
          codec='libx264',
          audio_codec='aac',
          temp_audiofile='temp-audio.m4a',
          remove_temp=True
        )
        video_list_file = "{}video_list.txt".format(self.save_path)

        with open(video_list_file, "w") as f:
            f.write("file {}\n".format(self.intro_clip))
            f.write("file {}\n".format(merged_clip_name))
            f.write("file {}\n".format(self.outro_clip))

        ffmpeg_cmd = 'ffmpeg -f concat -safe 0 -i "{}" -i "{}" -i "{}" -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=unsafe=1:n=3:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" -c copy {}'.format(self.intro_clip, merged_clip_name, self.outro_clip, final_vid_name)
        # cmd = 'ffmpeg -i \'{}\' -i \'{}\' -i \'{}\' -codec aac -filter_complex \"[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n=3:v=1:a=1:safe=0 [v] [a]\" -map "[v]" -map "[a]" -y {}'.format(self.intro_clip, merged_clip_name, self.outro_clip, merged_clip_name)
        os.system(ffmpeg_cmd)
        os.remove(merged_clip_name)

# ffmpeg -f concat -safe 0 -i video_list.txt -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=unsafe=1:n=3:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" -c copy demo_1.mp4
# ffmpeg -f concat -safe 0 -i "../videos/intro.mp4" -i "../edited_videos/new.mp4" -i "../videos/outro.mp4" -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=unsafe=1:n=3:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" -c copy demo_1.mp4