# stack_video_maker

## how to install 
After activate venv(if needed), install dependencies.
`pip install -r requirements.txt`

After then, please install `ffmpeg`.

# Usage

## For Stackoverflow

First, make the list csv file.

`python StackoverScrape.py keyword 3`

After then, run the below command

```
cd src
python run_stack.py list.csv
```
    usage: run_stack.py [-h] keyword entries

    positional arguments:
      keyword     keyword to search
      entries     ents number to search

    optional arguments:
      -h, --help  show this help message and exit

The title of generated videos are `keyword_0.mp4`, `keyword_1.mp4` ...

The intro and outro videos are located in `videos` and you can change them in line 15, 16 of `src/VideoEdit.py`