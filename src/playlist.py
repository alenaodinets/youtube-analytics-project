import os
import datetime
from googleapiclient.discovery import build
from isodate import parse_duration

API_KEY = os.getenv('API_KEY')


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.youtube = self.build_youtube_service()
        self.playlist_title = self.get_playlist_title()
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def build_youtube_service(self):
        return build('youtube', 'v3', developerKey=API_KEY)

    def get_playlist_title(self):
        request = self.youtube.playlists().list(part="snippet", id=self.playlist_id)
        response = request.execute()
        return response['items'][0]['snippet']

    @property
    def title(self):
        return self.playlist_title['title']

    @property
    def total_duration(self):
        """возвращает объект класса datetime.timedelta с суммарной длительностью плейлиста"""
        videos = self.youtube.playlistItems().list(part="contentDetails",
                                                   playlistId=self.playlist_id).execute()['items']
        total_duration = datetime.timedelta()
        for video in videos:
            video_id = video["contentDetails"]["videoId"]
            video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=video_id).execute()
            content_details = video_response['items'][0]['contentDetails']
            duration = content_details.get('duration', '')
            if duration:
                parsed_duration = parse_duration(duration)
                total_duration += parsed_duration
        return total_duration

    def get_video_ids(self):
        videos = self.youtube.playlistItems().list(part="contentDetails",
                                                   playlistId=self.playlist_id).execute()['items']
        return [video["contentDetails"]["videoId"] for video in videos]


    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                            maxResults=50).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()

        likes = 0
        video_url = str()
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > likes:
                video_url = video['id']
                likes = int(video['statistics']['likeCount'])
        return f'https://youtu.be/{video_url}'
