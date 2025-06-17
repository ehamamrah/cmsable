import yt_dlp
from datetime import datetime, timedelta, timezone
from django.utils import timezone as django_timezone

class YoutubeReader:
    def __init__(self, url):
        self.url = url
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }

    def get_info(self):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)

                timestamp = info.get('timestamp', None)
                if timestamp:
                    publish_date = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                else:
                    publish_date = django_timezone.now()

                duration_seconds = info.get('duration', 0)
                duration = timedelta(seconds=duration_seconds)
                
                return {
                    'title': info.get('title', ''),
                    'description': info.get('description', ''),
                    'duration': duration,
                    'publish_date': publish_date
                }
        except Exception as e:
            raise Exception(f"Error reading YouTube video: {str(e)}")