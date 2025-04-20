"""
Here is an example of the information we obtain from
the API when asking for an image:

"id": 195893,
"pageURL": "https://pixabay.com/en/blossom-bloom-flower-195893/",
"type": "photo",
"tags": "blossom, bloom, flower",
"previewURL": "https://cdn.pixabay.com/photo/2013/10/15/09/12/flower-195893_150.jpg"
"previewWidth": 150,
"previewHeight": 84,
"webformatURL": "https://pixabay.com/get/35bbf209e13e39d2_640.jpg",
"webformatWidth": 640,
"webformatHeight": 360,
"largeImageURL": "https://pixabay.com/get/ed6a99fd0a76647_1280.jpg",
"fullHDURL": "https://pixabay.com/get/ed6a9369fd0a76647_1920.jpg",
"imageURL": "https://pixabay.com/get/ed6a9364a9fd0a76647.jpg",
"imageWidth": 4000,
"imageHeight": 2250,
"imageSize": 4731420,
"views": 7671,
"downloads": 6439,
"likes": 5,
"comments": 2,
"user_id": 48777,
"user": "Josch13",
"userImageURL": "https://cdn.pixabay.com/user/2013/11/05/02-10-23-764_250x250.jpg",

And here it is what we receive about a video:

"id": 125,
"pageURL": "https://pixabay.com/videos/id-125/",
"type": "film",
"tags": "flowers, yellow, blossom",
"duration": 12,
"videos": {
    "large": {
        "url": "https://cdn.pixabay.com/video/2015/08/08/125-135736646_large.mp4",
        "width": 1920,
        "height": 1080,
        "size": 6615235,
        "thumbnail": "https://cdn.pixabay.com/video/2015/08/08/125-135736646_large.jpg"
    },
},
"views": 4462,
"downloads": 1464,
"likes": 18,
"comments": 0,
"user_id": 1281706,
"user": "Coverr-Free-Footage",
"userImageURL": "https://cdn.pixabay.com/user/2015/10/16/09-28-45-303_250x250.png"

"""
from yta_general_utils.downloader import Downloader
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.dataclasses import FileReturn
from dataclasses import dataclass
from typing import Union


# TODO: Maybe move this to another part (?)
IMAGE_QUALITY_FORMATS_ORDERED = ['imageURL', 'fullHDURL', 'largeImageURL', 'webformatURL', 'previewURL']
"""
This fields are available in the response and
contain all the image formats available for
download.
"""

@dataclass
class PixabayImage:
    """
    Class to represent a Pixabay image and to
    simplify the way we work with its data.
    """

    id: str = None
    """
    Unique identifier of this image in Pixabay
    platform. Useful to avoid using it again
    in the same project.
    """
    width: int = None
    height: int = None
    size: int = None
    """
    Size (in bytes?) of the image.
    """
    display_url: str = None
    """
    Url in which the image is displayed in the
    Pixabay platform. This url is not for 
    downloading the image.
    """
    _download_url: str = None
    """
    The download url of the option with the highest
    quality available. This download url is found in
    the 'src' attribute by searching in desc. order.
    """
    tags: str = None
    """
    Tags used when uploading the image to Pixabay
    platform.
    """
    author: dict = None
    """
    Author information.
    """
    raw_json: dict = None
    """
    The whole raw json data provided by Pexels. This
    is for debugging purposes only.
    """

    @property
    def download_url(self):
        """
        The download url of the option with the highest
        quality available. This download url is found in
        different attributes of the whole response, by
        searching in desc. order.
        """
        if not hasattr(self, '_download_url'):
            for field in IMAGE_QUALITY_FORMATS_ORDERED:
                # TODO: The field is actually in the response, not nested
                if self.raw_json[field]:
                    self._download_url = self.raw_json[field]
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
            'size': self.size,
            'tags': self.tags,
            'display_url': self.display_url,
            'download_url': self.download_url,
            'author': self.author,
        }

    def __init__(
        self,
        data: any
    ):
        self.id = data['id']
        self.width = data['imageWidth']
        self.height = data['imageHeight']
        self.size = data['imageSize']
        self.display_url = data['pageURL']
        self.tags = data['tags']
        self.author = {
            'id': data['user_id'],
            'name': data['user'],
            'avatar_url': data['userImageURL']
        }
        self.raw_json = data

    def download(
        self,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Download the current Pixabay image to the provided
        'output_filename' (or, if not provided, to a 
        temporary file).

        This method returns the final 'output_filename' 
        of the downloaded image.
        """
        return Downloader.download_image(
            self.download_url,
            Output.get_filename(output_filename, FileTypeX.IMAGE)
        )




# TODO: Maybe move this to another part (?)
VIDEO_QUALITY_FORMATS_ORDERED = ['large', 'medium', 'small', 'tiny']
"""
This fields are available in the response and
contain all the image formats available for
download.
"""

@dataclass
class PixabayVideo:
    """
    Class to represent a video of the Pixabay platform and
    to handle it easier than as raw data. A video has the
    main information but also different video formats and
    qualities that can be used for different purposes.
    Maybe we want a landscape video or maybe a portrait, so
    both of them could be available as 'video_files' for
    the same video content.
    """

    id: str = None
    """
    Unique identifier for this video in the Pixabay
    platform.
    """
    display_url: str = None
    type: str = None
    """
    TODO: I don't know if this type is useful for us
    """
    duration: float = None
    """
    The video duration provided by the platform.
    """
    views: int = None
    downloads: int = None
    likes: int = None
    author: dict = None

    _best_video: any = None
    _download_url: str = None

    raw_json: dict = None

    def __init__(
        self,
        data: any
    ):
        self.id = data['id']
        self.display_url = data['pageURL']
        self.type = data['type']
        self.duration = data['duration']
        self.views = data['views']
        self.downloads = data['downloads']
        self.likes = data['likes']
        self.author = {
            'id': data['user_id'],
            'name': data['user'],
            'avatar_url': data['userImageURL']
        }
        self.raw_json = data

    # TODO: Maybe add 'extension' property to handle
    # it from the end of the 'download_url' property
    
    @property
    def quality(self):
        """
        The quality of the best video.
        """
        return self.best_video['quality']
    
    @property
    def thumbnail_url(self):
        """
        The url of the thumbnail of the best video.
        """
        return self.best_video['thumbnail']
    
    @property
    def width(self):
        """
        The width in pixels of the best video.
        """
        return self.best_video['width']
    
    @property
    def height(self):
        """
        The height in pixels of the best video.
        """
        return self.best_video['height']
    
    @property
    def size(self):
        """
        The size of the best video.
        """
        return self.best_video['size']

    @property
    def best_video(self):
        """
        Best video file for our specific purpose that must
        be loaded on demand to avoid unnecessary processing.
        """
        if not hasattr(self, '_best_video'):
            for size in VIDEO_QUALITY_FORMATS_ORDERED:
                if size in self.raw_json['videos']:
                    self._best_video = self.raw_json['videos'][size]
                    break

        return self._best_video
    
    @property
    def download_url(self):
        """
        The url to download the best video file found.
        """
        if not hasattr(self, '_download_url'):
            self._download_url = self.best_video['url']

        return self._download_url
    
    @property
    def as_json(self):
        """
        Return the object instance as a json to be
        displayed and debugged.
        """
        return {
            'id': self.id,
            'display_url': self.display_url,
            'type': self.type,
            'duration': self.duration,
            'views': self.views,
            'downloads': self.downloads,
            'likes': self.likes,
            'author': self.author,
            'width': self.width,
            'height': self.height,
            'size': self.size,
            'quality': self.quality
        }
    
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

