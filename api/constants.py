import re

VIDEO_PAGE_URLS = [
    "https://www.youtube.com/c/{channel_id}/videos",
    "https://www.youtube.com/user/{channel_id}/videos"
]
YOUTUBE_REQUEST_HEADERS = {"Accept-Language": "en-US,en;q=0.5"}

RE_VIDEO_DATA = re.compile(r"var ytInitialData = (\{.+?\});")
