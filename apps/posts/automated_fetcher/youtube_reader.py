import yt_dlp

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
                
                return {
                    'title': info.get('title', ''),
                    'description': info.get('description', ''),
                    'duration': info.get('duration', 0)
                }
        except Exception as e:
            raise Exception(f"Error reading YouTube video: {str(e)}")
