import sys 
from utils.commons import YoutubeApiCommons

args = sys.argv

video_url = args[1]

call_obj = YoutubeApiCommons(video_url)
fetch_response = call_obj.get_comments()

print(fetch_response)