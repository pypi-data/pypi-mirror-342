from yta_stock_downloader.pexels.enums import PexelsLocale
from yta_general_utils.downloader import Downloader
from yta_general_utils.programming.output import Output
from yta_general_utils.dataclasses import FileReturn
from yta_general_utils.file.enums import FileTypeX
from typing import Union
from dataclasses import dataclass


# TODO: Maybe move this to another part (?)
FIELDS_ON_SRC = ['original', 'large2x', 'large', 'medium', 'small', 'portrait', 'landscape', 'tiny']
"""
This fields are available in the 'src' attribute
which contains all the image formats available
for download.
"""

@dataclass
class PexelsImage:
    """
    Class to represent a Pexels image and to
    simplify the way we work with its data.
    """

    id: int = None
    """
    Unique identifier of this image in Pexels
    platform. Useful to avoid using it again
    in the same project.
    """
    width: int = None
    height: int = None
    display_url: str = None
    """
    Url in which the image is displayed in the
    Pexels platform. This url is not for 
    downloading the image.
    """
    _download_url: str = None
    """
    The download url of the option with the highest
    quality available. This download url is found in
    the 'src' attribute by searching in desc. order.
    """
    src: dict = None
    """
    The different image formats (within a dict)
    available for download. See FIELDS_ON_SRC to
    see available formats.
    """
    author: dict = None
    """
    The author of the image as a dict containing
    its name, profile url and id.
    """
    agerage_color: str = None
    """
    The average color of the image, provided by
    the Pexels platform.
    """
    is_liked: bool = None
    """
    A boolean that indicates if I have liked the
    image or not.
    """    
    alt: str = None
    """
    The alternative text of the image, which is a
    useful description for web browsers.
    """
    raw_json: dict = None
    """
    The whole raw json data provided by Pexels. This
    is for debugging purposes only.
    """

    @property
    def download_url(self):
        """
        The download url of the option highest quality
        option available. This download url is found in
        the 'src' attribute by searching in desc. order.
        """
        if not hasattr(self, '_download_url'):
            for field in FIELDS_ON_SRC:
                if self.src[field]:
                    self._download_url = self.src[field]
                    break

        return self._download_url

    @property
    def as_json(self):
        """
        Return the object instance as a json to be
        displayed and debugged.
        """
        return {
            'id': self.id,
            'width': self.width,
            'height': self.height,
            'display_url': self.display_url,
            'download_url': self.download_url,
            'author': self.author,
            'average_color': self.average_color,
            'src': self.src,
            'is_liked': self.is_liked, 
            'alt': self.alt,
        }

    def __init__(
        self,
        data
    ):
        # TODO: Could be some of those fields unavailable?
        self.id = data['id']
        self.width = data['width']
        self.height = data['height']
        self.display_url = data['url']
        self.src = data['src']
        self.author = {
            'id': data['photographer_id'],
            'url': data['photographer_url'],
            'name': data['photographer'],
        }
        self.average_color = data['avg_color']
        """
        These are the different formats available: 'original', 
        'large2x', 'large', 'medium', 'small', 'portrait',
        'landscape' and 'tiny'
        """
        self.is_liked = data['liked']
        self.alt = data['alt']
        self.raw_json = data

    def download(
        self,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Download this image to the provided local
        'output_filename'. If no 'output_filename'
        is provided, it will be stored locally with
        a temporary name.

        This method returns the final downloaded
        image filename.
        """
        return Downloader.download_image(
            self.download_url,
            Output.get_filename(output_filename, FileTypeX.IMAGE)
        )

@dataclass
class PexelsImagePageResult:
    """
    A class to represent the results obtained from the
    Pexels Image API requests we send, including all 
    the information needed to be able to work with the
    obtained images and to look for more images.

    This class has to be instantiated when we send a
    request and we receive a response, so the response
    is parsed with this class.
    """
    
    query: str = None
    """
    The query used in the request.
    """
    locale: PexelsLocale = None
    """
    The locale used in the request.
    """
    page: int = None
    """
    The current page of Pexels image results.
    """
    per_page: int = None
    """
    The amount of images that are being obtained
    per page for the request.
    """
    total_results: int = None
    """
    The amount of results obtained with the request,
    that is the sum of all existing results 
    considering not pagination nor current page.

    TODO: Is this actually that value (?)
    """
    next_page_api_url: str = None
    """
    The API url to make a request to obtain the next
    results page.

    TODO: How do you actually use this url (?)
    """
    images: list[PexelsImage] = None
    """
    The array containing all the images found in the
    current page according to the query.
    """
    raw_json: dict = None
    """
    The whole raw json data provided by Pexels. This
    is for debugging purposes only.
    """

    @property
    def total_pages(self):
        """
        The total amount of pages according to the search,
        items per page and pages found.

        TODO: Is this actually useful for anything (?)
        """
        total = (int) (self.total_results / self.per_page)
        if self.total_results % self.per_page > 0:
            total += 1

        return total

    @property
    def as_json(self):
        """
        Return the object instance as a json to be
        displayed and debugged.
        """
        # TODO: Review this due to new changes
        return {
            'query': self.query,
            'locale': self.locale,
            'page': self.page,
            'per_page': self.per_page,
            'total_results': self.total_results,
            'total_pages': self.total_pages,
            'next_page_api_url': self.next_page_api_url,
            'images': self.images
        }

    def __init__(
        self,
        query,
        locale,
        data
    ):
        self.query = query
        self.locale = locale
        self.page = data['page']
        self.per_page = data['per_page']
        self.total_results = data['total_results']
        self.next_page_api_url = data['next_page'],
        self.images = [PexelsImage(image) for image in data['photos']]
        self.raw_json = data

@dataclass
class PexelsVideo:
    """
    Class to represent a video of the Pexels platform and
    to handle it easier than as raw data. A video has the
    main information but also different video files, or
    video formats, that can be used for different purposes.
    Maybe we want a landscape video or maybe a portrait,
    so both of them could be available as 'video_files'
    for the same video content.
    """

    id: str = None
    """
    The video unique identifier in the Pexels platform.
    """
    display_url: str = None
    width: int = None
    height: int = None
    duration: float = None
    thumbnail_url: str = None
    author: dict = None
    """
    The author of the image as a dict containing
    its name, profile url and id.
    """
    video_files: list[any] = None
    """
    A list containing all the video source files for
    this specific video.
    """
    _best_video: dict = None
    """
    The video source with the best quality which is
    actually stored on the platform.

    TODO: Rethink this because it is a complex dict
    with 'file_type' and more properties we should
    map to be handled easier
    """
    _download_url: str = None
    """
    The url to download the best video file found.
    """
    raw_json: dict = None
    """
    The whole raw json data provided by Pexels. This
    is for debugging purposes only.
    """

    @property
    def best_video(self):
        """
        The video source with the best quality which is
        actually stored on the platform.
        """
        if not hasattr(self, '_best_video'):
            # TODO: What if lower quality but higher fps value (?)
            self._best_video = max(self.video_files, key = lambda video_file: video_file['width'])

        return self._best_video
    
    @property
    def download_url(self):
        """
        The url to download the best video file found.
        """
        if not hasattr(self, '_download_url'):
            self._download_url = self.best_video['link']

        return self._download_url
    
    @property
    def fps(self):
        """
        The fps of the best video.
        """
        return self.best_video['fps']
    
    @property
    def as_json(self):
        """
        Return the object instance as a json to be
        displayed and debugged.
        """
        return {
            'id': self.id,
            'display_url': self.display_url,
            'width': self.width,
            'height': self.height,
            'duration': self.duration,
            'thumbnail_url': self.thumbnail_url,
            'author': self.author,
            'download_url': self.download_url,
        }

    def __init__(self, data: any):
        self.id = data['id']
        self.display_url = data['url']
        self.width = data['width']
        self.height = data['height']
        self.duration = data['duration']
        self.thumbnail_url = data['image']
        self.author = {
            'id': data['user']['id'],
            'url': data['user']['url'],
            'name': data['user']['name'],
        }
        # TODO: Add author
        self.video_files = data['video_files']
        self.raw_json = data

    def download(
        self,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Download this video to the provided local
        'output_filename'. If no 'output_filename'
        is provided, it will be stored locally with
        a temporary name.

        This method returns the final downloaded
        video filename.
        """
        return Downloader.download_video(
            self.download_url,
            Output.get_filename(output_filename, FileTypeX.VIDEO)
        )