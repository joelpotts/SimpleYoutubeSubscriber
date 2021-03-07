import concurrent.futures
import json
import logging

import dateparser
import requests

from api import constants
from api.models import Subscription


def get_subscription_videos(user):
    """
        1) Get all channels from the DB
        2) Download all channel pages from youtube
        3) Extract all data from resulting pages
        4) Generate JSON: Need title, link, timestamp, image
    """

    channels = get_subs(user)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_and_process_channel, channel) for channel in channels]
    video_data = [video for f in futures for video in f.result()]
    video_data = [
        {**item, "timestamp": dateparser.parse(item["timestamp"]).isoformat()}
        for item in video_data
    ]

    return video_data

def get_subs(user):
    """Get the list channel IDs for the associated user.

    param user: The authenticated user who made the request.
    """

    subscription_query = Subscription.objects.filter(user=user)
    if subscription_query:
        return [sub.channel for sub in subscription_query]
    return None


def fetch_and_process_channel(channel_id):
    """Download the channel video page and process the results"""
    page_data = fetch_channel_page_data(channel_id)
    processed_data = process_page_data(page_data)
    return processed_data


def request_channel_page(channel_id):
    """Download the video channel page"""
    for url in constants.VIDEO_PAGE_URLS:
        try:
            response = requests.get(
                url.format(channel_id=channel_id), headers=constants.YOUTUBE_REQUEST_HEADERS
            )
            response.raise_for_status()
            return response.text
        except requests.HTTPError:
            logging.error("An error occurred fetching the youtube page.")
        except Exception:
            logging.error(
                f"An unexpected error occurred fetching the youtube channel page: {channel_id}"
            )
    return {}


def fetch_channel_page_data(channel_id):
    """Get channel page and extract the video data"""
    try:
        page_text = request_channel_page(channel_id)
        video_data = constants.RE_VIDEO_DATA.search(page_text).group(1)
        return json.loads(video_data)
    except json.JSONDecodeError:
        logging.error("An error occurred trying to extract JSON data from the page")
    except AttributeError:
        logging.error(f"No data found on page {channel_id}")
    except Exception:
        logging.error(f"An unexpected error occurred processing the response from {channel_id}")


def process_page_data(page_data):
    """Extract each video item and extract the info for each."""
    video_items = []
    try:
        tab_renderers = page_data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
        video_items = tab_renderers[1]["tabRenderer"]["content"]["sectionListRenderer"]["contents"
            ][0]["itemSectionRenderer"]["contents"][0]["gridRenderer"]["items"]
    except KeyError:
        logging.error("The JSON did not have the expected keys to process the page data correctly")

    video_data = []
    for item in video_items:
        if data := get_video_data(item):
            video_data.append(data)
    return video_data


def get_video_data(video_item):
    """Extract the required data for the video item"""
    try:
        return {
            "url": video_item["gridVideoRenderer"]["videoId"],
            "title": video_item["gridVideoRenderer"]["title"]["runs"][0]["text"],
            "image_url": video_item["gridVideoRenderer"]["thumbnail"]["thumbnails"][0]["url"],
            "timestamp": video_item["gridVideoRenderer"]["publishedTimeText"]["simpleText"
                ].replace("Streamed ", ""),
        }
    except TypeError:
        logging.error("dateparser was unable to parse a date due to thread safety")
    except Exception as error:
        logging.error(
            f"An error occurred converting a video item into processed video data. {error}"
        )
