from apiclient.discovery import build
from urllib.parse import urlparse, parse_qs

class YoutubeApiCommons:
    @staticmethod
    def config_service(file_name):
        with open(file_name):
            k = f.readline()

        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        return build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=k)

    @staticmethod
    def get_id_from_url(url):
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query).get('v')
        if query: 
            return query[0]
        path = parsed_url.path.split('/')
        if path:
            return path[:-1]