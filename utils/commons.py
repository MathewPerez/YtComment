import json
from csv import writer
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

class YoutubeApiCommons:
    def __init__(self, video_url):
        self.video_url = video_url

    def config_service(self, file_name):
        with open(file_name) as f:
            k = f.readline()

        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        return build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=k)

    def get_id_from_url(self, url):
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query).get('v')
        if query: 
            return query[0]
        path = parsed_url.path.split('/')
        if path:
            return path[:-1]

    def get_comments(self,
                 part='snippet', 
                 maxResults=100, 
                 textFormat='plainText',
                 order='time',
                 videoId='',
                 csv_filename="bts"):

        videoId = self.video_url
        
        comments, commentsId, repliesCount, likesCount, viewerRating = [], [], [], [], []
        
        service = self.config_service('utils/dev_key.txt')
        
        response = service.commentThreads().list(
            part=part,
            maxResults=maxResults,
            textFormat=textFormat,
            order=order,
            videoId=self.get_id_from_url(videoId)
        ).execute()
                    

        while response:
                    
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comment_id = item['snippet']['topLevelComment']['id']
                reply_count = item['snippet']['totalReplyCount']
                like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
                
                comments.append(comment)
                commentsId.append(comment_id)
                repliesCount.append(reply_count)
                likesCount.append(like_count)

                with open(f'{csv_filename}.csv', 'a+') as f:
                    csv_writer = writer(f)
                    csv_writer.writerow([comment, comment_id, reply_count, like_count])
            
            if 'nextPageToken' in response:
                response = service.commentThreads().list(
                    part=part,
                    maxResults=maxResults,
                    textFormat=textFormat,
                    order=order,
                    videoId=self.get_id_from_url(videoId),
                    pageToken=response['nextPageToken']
                ).execute()
            else:
                break

        return {
            'Comments': comments,
            'Comment ID': commentsId,
            'Reply Count' : repliesCount,
            'Like Count' : likesCount
        }