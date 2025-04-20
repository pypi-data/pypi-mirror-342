"""
Pixabay image download API.

See more: https://pixabay.com/api/docs/
"""
from yta_stock_downloader.pixabay.constants import PIXABAY_API_ENDPOINT_URL
from yta_stock_downloader.pixabay.dataclasses import PixabayImage
from yta_general_utils.programming.env import Environment
from yta_general_utils.dataclasses import FileReturn
from yta_general_utils.programming.output import Output
from yta_general_utils.random import Random
from yta_general_utils.file.enums import FileTypeX
from typing import Union

import requests


PIXABAY_API_KEY = Environment.get_current_project_env('PIXABAY_API_KEY')

def _search_pixabay_images(query: str):
    """
    Send a search images request agains the
    Pixabay platform.

    For internal use only.
    """
    return requests.get(
        PIXABAY_API_ENDPOINT_URL,
        {
            'key': PIXABAY_API_KEY,
            'q': query,
            'orientation': 'horizontal',
            'image_type': 'photo'
        },
        timeout = 10
    )

def search_pixabay_images(
    query: str,
    ids_to_ignore: list[str] = []
) -> list[PixabayImage]:
    """
    Search the images with the provided 'query' in
    the Pixabay platform.

    This method returns an empty array if no images
    found, or the array containing the images if
    found.
    """
    response = _search_pixabay_images(query).json()

    if response['total'] == 0:
        return []
    
    return [
        PixabayImage(image)
        for image in response['hits']
        if image['id'] not in ids_to_ignore
    ]

def get_first_pixabay_image(
    query: str,
    ids_to_ignore: list[str]
) -> Union[PixabayImage, None]:
    """
    Find and return the first image from Pixabay provider
    with the given 'query' (if existing).

    The result will be None if no results, or a result
    containing the first one found.
    """
    images = search_pixabay_images(query, ids_to_ignore)

    return (
        images[0]
        if len(images) > 0 else
        None
    )

def get_random_pixabay_image(
    query: str,
    ids_to_ignore: list[str]
) -> Union[PixabayImage, None]:
    """
    Find and return a random image from Pixabay provider
    with the given 'query' (if existing).

    The result will be None if no results, or a result
    containing the first one found.
    """
    images = search_pixabay_images(query, ids_to_ignore)

    return (
        images[Random.int_between(0, len(images) - 1)]
        if len(images) > 0 else
        None
    )

def download_first_pixabay_image(
    query: str,
    ids_to_ignore: list[str],
    output_filename: Union[str, None] = None
) -> Union[FileReturn, None]:
    """
    Download the first found pexels image with the provided
    'query'. The image will be stored locally as
    'output_filename' or as a temporary filename if that
    parameter is not provided. The stored image filename is
    returned.

    This method will raise an Exception if no images are
    found or if the download is not possible.
    """
    image_to_download = get_first_pixabay_image(query, ids_to_ignore)

    return (
        image_to_download.download(Output.get_filename(output_filename, FileTypeX.IMAGE))
        if image_to_download is not None else
        None
    )

def download_random_pixabay_image(
    query: str,
    ids_to_ignore: list[str],
    output_filename: Union[str, None] = None
) -> Union[FileReturn, None]:
    """
    Download a random pexels image found with the provided
    'query'. The image will be stored locally as
    'output_filename' or as a temporary filename if that
    parameter is not provided. The stored image filename is
    returned.

    This method will raise an Exception if no images are
    found or if the download is not possible.
    """
    image_to_download = get_random_pixabay_image(query, ids_to_ignore)

    return (
        image_to_download.download(Output.get_filename(output_filename, FileTypeX.IMAGE))
        if image_to_download is not None else
        None
    )