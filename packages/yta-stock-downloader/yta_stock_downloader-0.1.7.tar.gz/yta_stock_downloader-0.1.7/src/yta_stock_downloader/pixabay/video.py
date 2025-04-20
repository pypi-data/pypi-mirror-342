"""
Pixabay video download API.

See more: https://pixabay.com/api/docs/
"""
from yta_stock_downloader.pixabay.constants import PIXABAY_VIDEOS_API_ENDPOINT_URL
from yta_stock_downloader.pixabay.dataclasses import PixabayVideo
from yta_general_utils.programming.env import Environment
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.dataclasses import FileReturn
from random import choice
from typing import Union

import requests


PIXABAY_API_KEY = Environment.get_current_project_env('PIXABAY_API_KEY')

def _search_pixabay_videos(
    query: str
):
    response = requests.get(
        url = PIXABAY_VIDEOS_API_ENDPOINT_URL,
        params = {
            'key': PIXABAY_API_KEY,
            'q': query,
            'video_type': 'film',
            'pretty': 'true'
        },
        timeout = 10
    )

    return response.json()

def search_pixabay_videos(
    query: str,
    ids_to_ignore: list[str] = []
) -> list[PixabayVideo]:
    response = _search_pixabay_videos(query)

    if response['total'] == 0:
        return []
    
    return [
        PixabayVideo(video)
        for video in response['hits']
        if video['id'] not in ids_to_ignore
    ]

def get_random_pixabay_video(
    query: str,
    ids_to_ignore: list[str] = []
) -> Union[PixabayVideo, None]:
    videos = search_pixabay_videos(query, ids_to_ignore)

    return choice(videos) if len(videos) > 0 else None

def get_first_pixabay_video(
    query: str,
    ids_to_ignore: list[str] = []
) -> Union[PixabayVideo, None]:
    videos = search_pixabay_videos(query, ids_to_ignore)

    return videos[0] if len(videos) > 0 else None

def download_random_pixabay_video(
    query: str,
    ids_to_ignore: list[str] = [],
    output_filename: Union[str, None] = None
) -> Union[FileReturn, None]:
    video = get_random_pixabay_video(query, ids_to_ignore)

    return (
        video.download(Output.get_filename(output_filename, FileTypeX.VIDEO))
        if video is not None else
        None
    )

def download_first_pixabay_video(
    query: str,
    ids_to_ignore: list[str] = [],
    output_filename: Union[str, None] = None
) -> Union[FileReturn, None]:
    video = get_first_pixabay_video(query, ids_to_ignore)

    return (
        video.download(Output.get_filename(output_filename, FileTypeX.VIDEO))
        if video is not None else
        None
    )