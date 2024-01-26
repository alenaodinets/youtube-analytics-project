import requests
import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

import isodate

load_dotenv()



class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        api_key: str = os.getenv("API_KEY")
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))
