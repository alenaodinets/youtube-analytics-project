import datetime
import os

from googleapiclient.discovery import build

API_KEY = os.getenv('API_KEY')


class Video:
    def __init__(self, video_id: str):
        self.video_id = video_id
        self.title = self._get_title()
        self.link = f"https://www.youtube.com/watch?v={video_id}"
        self.views_count = self._get_video_info('viewCount')
        self.like_count = self._get_video_info('likeCount')

    def __str__(self):
        return self.title

    def _get_title(self):
        try:
            youtube = build('youtube', 'v3', developerKey=API_KEY)
            request = youtube.videos().list(
                part='snippet',
                id=self.video_id
            )
            response = request.execute()
            return response['items'][0]['snippet']['title']
        except IndexError:
            return None

    def _get_video_info(self, data_type: str):
        try:
            youtube = build('youtube', 'v3', developerKey=API_KEY)
            request = youtube.videos().list(
                part='statistics',
                id=self.video_id
            )
            response = request.execute()
            return int(response['items'][0]['statistics'][data_type])
        except IndexError:
            return None


class PLVideo(Video):
    def __init__(self, video_id, id_playlist):
        super().__init__(video_id)
        self.id_playlist = id_playlist

    def __str__(self):
        return f'{self.title}'
