# stack_video_maker
This project will find popular stack threads and convert them into a text-to-speech videos. 

1. Find popular stack threads worthy of being converted to threads using reddit api and some type of web scraping.

2. Convert top threads into static images, convert top thread title's to TTS using text-to-speech api. 

3. Convert answer of threads into static image, read outloud with text-to-speech
  - repeat with all relevant & interesting answers to the question 

4. String Question image with text-to-speech & string Answers image with text-to-speech into a video using video editing api. 



# Usage

## For Stackoverflow
After installation of env, run the below command

```
cd src
python run_stack.py keyword number
```
    usage: run_stack.py [-h] keyword entries

    positional arguments:
      keyword     keyword to search
      entries     ents number to search

    optional arguments:
      -h, --help  show this help message and exit

The title of generated videos are `keyword_0.mp4`, `keyword_1.mp4` ...

The intro and outro videos are located in `videos` and you can change them in line 15, 16 of `src/VideoEdit.py`