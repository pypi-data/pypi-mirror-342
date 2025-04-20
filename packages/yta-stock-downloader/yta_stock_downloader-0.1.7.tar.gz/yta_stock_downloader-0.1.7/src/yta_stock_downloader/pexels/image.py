"""
Pexels image download API.

See more: https://www.pexels.com/api/documentation/
"""
from yta_stock_downloader.pexels.dataclasses import PexelsImage, PexelsImagePageResult
from yta_stock_downloader.pexels.constants import PEXELS_SEARCH_IMAGE_API_ENDPOINT_URL
from yta_stock_downloader.pexels.enums import PexelsLocale
from yta_general_utils.dataclasses import FileReturn
from yta_general_utils.programming.env import Environment
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.output import Output
from yta_general_utils.random import Random
from yta_general_utils.file.enums import FileTypeX
from typing import Union

import requests


PEXELS_API_KEY = Environment.get_current_project_env('PEXELS_API_KEY')
RESULTS_PER_PAGE = 25
HEADERS = {
    'content-type': 'application/json',
    'Accept-Charset': 'UTF-8',
    'Authorization': PEXELS_API_KEY
}

def _search_pexels_images(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    per_page: int = RESULTS_PER_PAGE,
    page: int = 1
) -> PexelsImagePageResult:
    """
    Send a search images request agains the
    Pxeles platform.

    For internal use only.
    """
    response = requests.get(
        PEXELS_SEARCH_IMAGE_API_ENDPOINT_URL,
        {
            'query': query,
            'orientation': 'landscape',   # landscape | portrait | square
            'size': 'large',   # large | medium | small
            'locale': locale.value, # 'es-ES' | 'en-EN' ...
            'per_page': per_page,
            'page': page
        },
        headers = HEADERS
    )

    return PexelsImagePageResult(query, locale.value, response.json())

def search_pexels_images(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    ignore_ids: list[str] = [],
    per_page: int = RESULTS_PER_PAGE
) -> list[PexelsImage]:
    """
    Makes a search of Pexels images and returns the results.
    This method will return an empty list (at least by now)
    if no results found.
    """
    page_results = _search_pexels_images(query, locale, per_page, 1)

    if page_results.total_results == 0:
        return []

    # Ignore images with ids to ignore
    images = [
        image
        for image in page_results.images
        if image.id not in ignore_ids
    ]

    # TODO: Think about an strategy to apply when 'images'
    # are not enough and we should make another request.
    # But by now we are just returning nothing, we don't 
    # want infinite requests loop or similar
    if len(images) == 0:
        # TODO: Make another request if possible (?)
        if page_results.page < page_results.total_pages:
            # TODO: Can we request a new one (?)
            pass
        pass

    return images

def get_first_pexels_image(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    ignore_ids: list[str] = [],
) -> Union[PexelsImage, None]:
    """
    Find and return the first image from Pexels provider
    with the given 'query' and 'locale' parameters (if
    existing).

    The result will be None if no results, or an object that 
    contains the 'id', 'width', 'height', 'url'. Please, see
    the PexelsImage class to know about the return.
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')

    locale = PexelsLocale.to_enum(locale)
    
    results = search_pexels_images(query, locale, ignore_ids)

    return (
        results[0]
        if len(results) > 0 else 
        None
    )

def get_random_pexels_image(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    ignore_ids: list[str] = [],
) -> Union[PexelsImage, None]:
    """
    Find and return a random image from Pexels provider
    with the given 'query' and 'locale' parameters (if
    existing).

    The result will be None if no results, or an object that 
    contains the 'id', 'width', 'height', 'url'. Please, see
    the PexelsImage class to know about the return.
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')

    locale = PexelsLocale.to_enum(locale)
    
    results = search_pexels_images(query, locale, ignore_ids)

    return (
        results[Random.int_between(0, len(results) - 1)]
        if len(results) > 0 else
        None
    )

def download_first_pexels_image(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    ignore_ids: list[str] = [],
    output_filename: Union[str, None] = None
) -> Union[FileReturn, None]:
    """
    Download the first pexels image found with the provided
    'query' and the also given 'locale'. The image will be
    stored locally as 'output_filename' or as a temporary
    filename if that parameter is not provided. The stored
    image filename is returned.

    This method will raise an Exception if no images are
    found or if the download is not possible.
    """
    image_to_download = get_first_pexels_image(query, locale, ignore_ids)

    return (
        image_to_download.download(Output.get_filename(output_filename, FileTypeX.IMAGE))
        if image_to_download is not None else
        None
    )

def download_random_pexels_image(
    query: str,
    locale: PexelsLocale = PexelsLocale.ES_ES,
    ignore_ids: list[str] = [],
    output_filename: Union[str, None] = None
) -> Union[FileReturn, None]:
    """
    Download a random pexels image found with the provided
    'query' and the also given 'locale'. The image will be
    stored locally as 'output_filename' or as a temporary
    filename if that parameter is not provided. The stored
    image filename is returned.

    This method will raise an Exception if no images are
    found or if the download is not possible.
    """
    image_to_download = get_random_pexels_image(query, locale, ignore_ids)

    return (
        image_to_download.download(Output.get_filename(output_filename, FileTypeX.IMAGE))
        if image_to_download is not None else
        None
    )