

# This file will be the main driver function and run the entire progam
# This will import the Reddit Scraping Class and the Video Editing Class

import argparse # Used to handle command line arguments
import pandas as pd

from RedditScrape import RedditScrape # Importing reddit scraping class to acquire posts and authors 

from StackoverScrape import questions_answers

from TextToSpeech import TextToSpeech # Importing tts class to make mp3 of posts

from ImageCreator import ImageCreator # Generates images of posts

from VideoEdit import VideoEditor # Edits all the tts mp3 and Images into a mp4 video 



def main() -> int: 

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='target csv file')
    args = parser.parse_args()

    ''' input_metadata holds the meta data from each entry in the input file
    is a list of dicts that will be used to build each video
    [ {link: <link>, n_entries: <n_entries>, title: <name> }, ...]
    '''
    input_metadata = [] 

    # Open the file from argument and build the list of meta data for each link to build videos 
    try:
        # keyword, num of entry
        csv_file = args.file

        stack_data = pd.read_csv(csv_file)

    except:
        print('Failed to scraping from stackover')
        return 1

    num_data = stack_data.shape[0]

    # Loop through each video meta object and create videos 
    for index in range(num_data): 
        # print(video_meta)

        # reddit_scraper = RedditScrape(video_meta['url'], video_meta['n_entries'])

        # # Returns 2 lists of strings, [all posts] [authors of posts]
        # # index 0 of both are associated with the title, the rest are replies to the thread
        # posts, authors = reddit_scraper.scrape_post()

        url = stack_data.url[index]
        q_title = stack_data.title[index]
        asked_user = stack_data.asked_user[index]
        question = stack_data.question[index]
        answered_user = stack_data.answered_user[index]
        answer = stack_data.answer[index]
        key = stack_data.keyword[index]

        posts = [q_title, question, answer]
        authors = [asked_user, asked_user, answered_user]

        new_split_posts = []
        new_split_authors = []

        for text, name in zip(posts, authors):
            if len(text) < 500:
                new_split_posts.append(text)
                new_split_authors.append(name)
            else:
                text_grp = []
                word_list = text.split(" ")
                par = ""
                for i, wd in enumerate(word_list):
                    par_len = len(par)
                    wd_len = len(wd)
                    if par_len + wd_len + 1 < 500:
                        par += " {}".format(wd)
                        if i+1 == len(word_list):
                            text_grp.append(par)
                    else:
                        text_grp.append(par)
                        par = ""
                num_split = len(text_grp)
                new_split_posts += text_grp
                new_split_authors += [name for _ in range(num_split)]

        # Text to speech 
        tts = TextToSpeech()   # Creating tts class
        tts.create_tts(new_split_posts)  # Creating all tts mp3 files for video 

        # Image Creation
        # Creating image for title 
        ImageCreator.create_image_for(new_split_posts[0], new_split_authors[0], 'title')

        # Creating image post for the replies: reply0.jpg, reply1.jpg, ...
        for i in range(1, len(new_split_posts)):
            ImageCreator.create_image_for(new_split_posts[i],new_split_authors[i], f'reply{str(i-1)}')


        # Creating a Video Editing object
        # Passing n_entries + 1, for # of images, since we have title + n replies

        Editor = VideoEditor(int(len(new_split_posts))-1, key + "_" + str(index+1))
        Editor.create_movie()
        print('movie created')

    return 0


if __name__ == '__main__':
    exit(main())


