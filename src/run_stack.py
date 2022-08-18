

# This file will be the main driver function and run the entire progam
# This will import the Reddit Scraping Class and the Video Editing Class

import argparse # Used to handle command line arguments

from RedditScrape import RedditScrape # Importing reddit scraping class to acquire posts and authors 

from StackoverScrape import questions_answers

from TextToSpeech import TextToSpeech # Importing tts class to make mp3 of posts

from ImageCreator import ImageCreator # Generates images of posts

from VideoEdit import VideoEditor # Edits all the tts mp3 and Images into a mp4 video 



def main() -> int: 

    parser = argparse.ArgumentParser()
    parser.add_argument('keyword', type=str, help='keyword to search')
    parser.add_argument('entries', type=int, help='ents number to search')
    args = parser.parse_args()

    ''' input_metadata holds the meta data from each entry in the input file
    is a list of dicts that will be used to build each video
    [ {link: <link>, n_entries: <n_entries>, title: <name> }, ...]
    '''
    input_metadata = [] 

    # Open the file from argument and build the list of meta data for each link to build videos 
    try:
        # keyword, num of entry
        keyword = args.keyword
        ent_num = args.entries

        stack_data = questions_answers(keyword, ent_num)

    except:
        print('Failed to scraping from stackover')
        return 1

    

    # Loop through each video meta object and create videos 
    for index, video_meta in enumerate(stack_data): 
        # print(video_meta)

        # reddit_scraper = RedditScrape(video_meta['url'], video_meta['n_entries'])

        # # Returns 2 lists of strings, [all posts] [authors of posts]
        # # index 0 of both are associated with the title, the rest are replies to the thread
        # posts, authors = reddit_scraper.scrape_post()

        url = video_meta["url"]
        asked_user = video_meta["asked_user"]
        question = video_meta["question"]
        answered_user = [video_meta["answered_user"]]
        answer = [video_meta["answer"]]
        posts = [question] + answer
        authors = [asked_user] + answered_user



        # for i, post in enumerate(posts):
        print('question: ', question)
        print('answer: ', answer)


        # Text to speech 
        tts = TextToSpeech()   # Creating tts class
        tts.create_tts(posts)  # Creating all tts mp3 files for video 

        # Image Creation
        # Creating image for title 
        ImageCreator.create_image_for(question, asked_user, 'title')

        # Creating image post for the replies: reply0.jpg, reply1.jpg, ...
        for i in range(1, len(posts)):
            ImageCreator.create_image_for(posts[i],authors[i], f'reply{str(i-1)}')


        # Creating a Video Editing object
        # Passing n_entries + 1, for # of images, since we have title + n replies

        Editor = VideoEditor(int(len(posts))-1, keyword+"_"+str(index+1))
        Editor.create_movie()
        print('movie created')

        
    return 0



if __name__ == '__main__':
    exit(main())


