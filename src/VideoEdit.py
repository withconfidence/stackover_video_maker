# This clas will hold the class that edits the images into video
#TODO: Once complete, remove global import and only import required

import os  # used for some file grabbing


class VideoEditor:
    def __init__(self,num_replies, video_name):
        self.num_replies = num_replies
        self.video_name = video_name
        self.image_path = '../images/'
        self.save_path = '../edited_videos/'
        self.intro_clip = '../videos/intro.mp4'
        self.outro_clip = '../videos/outro.mp4'
        self.dummy_audio = "../videos/dummy.opus"

        self.create_dir() # Creates the edited videos dir if it doesnt exist

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

        merged_clip_name = f'{self.save_path}merged_clips.mp4'

        image_temp = "images.txt"
        with open(image_temp, "w") as f:
            point = 5
            title_image = self.image_path + 'title.jpeg'
            f.write("file {}\noutpoint {}\n".format(title_image, point))

            for i in range(0, self.num_replies):
                target_image = "{}reply{}.jpeg".format(self.image_path, i)
                f.write("file {}\noutpoint {}\n".format(target_image, point))
        img_cmd = "ffmpeg -f concat -safe 0 -i {} -i {} -framerate 10 -c:v libx264 -r 30 -loglevel quiet -y {}".format(image_temp, self.dummy_audio,  merged_clip_name)
        os.system(img_cmd)

        final_vid_name = f'{self.save_path}{self.video_name}.mp4'
        ffmpeg_cmd = 'ffmpeg -i {} -i {} -i {} -s 1920*1080 -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=unsafe=1:n=3:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" -loglevel quiet -y {}'.format(self.intro_clip, merged_clip_name, self.outro_clip, final_vid_name)

        os.system(ffmpeg_cmd)
        try:
            os.remove(merged_clip_name)
            os.remove(image_temp)
        except:
            pass

