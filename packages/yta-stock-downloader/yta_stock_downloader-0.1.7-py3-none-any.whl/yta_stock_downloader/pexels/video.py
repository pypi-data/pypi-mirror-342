"""
Pexels video download API.

See more: https://www.pexels.com/api/documentation/
"""
from yta_stock_downloader.pexels.enums import PexelsLocale
from yta_stock_downloader.pexels.constants import PEXELS_SEARCH_VIDEOS_URL, PEXELS_GET_VIDEO_BY_ID_URL
from yta_stock_downloader.pexels.dataclasses import PexelsVideo
from yta_general_utils.dataclasses import FileReturn
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.programming.env import Environment
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.validator.number import NumberValidator
from random import choice
from typing import Union

import requests


PEXELS_API_KEY = Environment.get_current_project_env('PEXELS_API_KEY')
RESULTS_PER_PAGE = 25
HEADERS = {
    'content-type': 'application/json',
    'Accept-Charset': 'UTF-8',
    'Authorization': PEXELS_API_KEY
}

def _search_pexels_videos(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    per_page: int = RESULTS_PER_PAGE
):
    response = requests.get(
        url = PEXELS_SEARCH_VIDEOS_URL,
        params = {
            'query': query,
            'locale': locale.value,
            'per_page': per_page
        },
        headers = HEADERS
    )

    # TODO: Should I create a PexelsVideoPageResult (?)
    return [
        PexelsVideo(video)
        for video in response.json()['videos']
    ]

    return response.json()['videos']
    page_results = PexelsImagePageResult(query, locale.value, response.json())

    return page_results

def search_pexels_videos(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    ignore_ids: list[str] = [],
    per_page: int = 25
):
    """
    Obtain videos from Pexels platform according to the 
    provided 'query' and 'locale', including only 
    'per_page' elements per page.
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')
    
    locale = PexelsLocale.to_enum(locale)

    if not NumberValidator.is_positive_number(per_page):
        raise Exception('The provided "duration" parameter is not a positive number.')

    # TODO: Check if this .json()['videos'] is working
    # TODO: Do we need something from the .json() response (?)
    videos = _search_pexels_videos(query, locale, per_page)

    return [
        video
        for video in videos
        if video.id not in ignore_ids
    ]

def get_random_pexels_video(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    ignore_ids = []
) -> Union[PexelsVideo, None]:
    """
    Obtain a random video from the Pexels platform
    according to the provided 'query' and 'locale'
    parameters and avoiding the ones which id is
    contained in the provided 'ignore_ids' parameter
    list.

    This method returns an empty list if no videos
    found with the provided 'query' and 'locale'
    parameters, also according to the provided
    'ignore_ids' ids list.
    """
    videos = search_pexels_videos(query, locale, ignore_ids)

    return choice(videos) if len(videos) > 0 else None

def get_first_pexels_video(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    ignore_ids = []
) -> Union[PexelsVideo, None]:
    """
    Obtain the first video from the Pexels platform
    according to the provided 'query' and 'locale'
    parameters and avoiding the ones which id is
    contained in the provided 'ignore_ids' parameter
    list.

    This method returns an empty list if no videos
    found with the provided 'query' and 'locale'
    parameters, also according to the provided
    'ignore_ids' ids list.
    """
    videos = search_pexels_videos(query, locale, ignore_ids)

    return videos[0] if len(videos) > 0 else None

def get_pexels_video_by_id(
    id: int
) -> Union[PexelsVideo, None]:
    """
    Obtain the pexels video with the provided 'id'
    (if existing).
    """
    response = requests.get(
        url = f'{PEXELS_GET_VIDEO_BY_ID_URL}{str(id)}',
        headers = HEADERS
    )
    
    # TODO: How to know if no video found (?)
    video = PexelsVideo(response.json())
    
    return video if video is not None else None

def download_random_pexels_video(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    ignore_ids = [],
    output_filename: Union[str, None] = None
) -> Union[FileReturn, None]:
    """
    Download a random video from the Pexels
    platform.
    """
    video = get_random_pexels_video(query, locale, ignore_ids)

    return (
        video.download(Output.get_filename(output_filename, FileTypeX.VIDEO))
        if video else
        None
    )

def download_first_pexels_video(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    ignore_ids = [],
    output_filename: Union[str, None] = None
) -> Union[FileReturn, None]:
    """
    Download the first video available from the
    Pexels platform.
    """
    video = get_first_pexels_video(query, locale, ignore_ids)

    return (
        video.download(Output.get_filename(output_filename, FileTypeX.VIDEO))
        if video is not None else
        None
    )

def download_pexels_video_by_id(
    id: int,
    output_filename: Union[str, None] = None
) -> Union[FileReturn, None]:
    """
    Download the video with the given 'id' from the
    Pexels platform if available.
    """
    video = get_pexels_video_by_id(id)

    return (
        video.download(Output.get_filename(output_filename, FileTypeX.VIDEO))
        if video is not None else
        None
    )