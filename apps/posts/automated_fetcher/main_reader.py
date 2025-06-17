class MainReader:
    def __init__(self, url):
        self.url = url

    def read(self):
        fetcher = self.analyze_fetcher(self.url)
        data = fetcher.get_info()
        return data

    def analyze_fetcher(self, url):
        if 'youtube.com' in url or 'youtu.be' in url:
            from apps.posts.automated_fetcher.youtube_reader import YoutubeReader
            return YoutubeReader(url)
        else:
            raise ValueError("Unsupported URL format")