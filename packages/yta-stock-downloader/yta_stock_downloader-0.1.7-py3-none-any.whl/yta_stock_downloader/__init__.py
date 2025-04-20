from yta_stock_downloader.pexels.image import get_first_pexels_image, get_random_pexels_image
from yta_stock_downloader.pexels.video import get_first_pexels_video, get_random_pexels_video
from yta_stock_downloader.pixabay.image import get_first_pixabay_image, get_random_pixabay_image
from yta_stock_downloader.pixabay.video import get_first_pixabay_video, get_random_pixabay_video
from yta_stock_downloader.pixabay.dataclasses import PixabayImage, PixabayVideo
from yta_stock_downloader.pexels.dataclasses import PexelsImage, PexelsVideo
from yta_stock_downloader.pexels.enums import PexelsLocale
from yta_stock_downloader.validation import validate_query, validate_ids_to_ignore
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.dataclasses import FileReturn
from typing import Union
from abc import ABC, abstractmethod
from typing import Union


__all__ = [
    'StockVideoDownloader',
    'StockImageDownloader',
    'PexelsImageDownloader',
    'PexelsVideoDownloader',
    'PixabayImageDownloader',
    'PixabayVideoDownloader'
]

class _StockDownloader(ABC):
    """
    Class to wrap the functionality related to
    downloading stock images and videos.

    This class must be inherited from the 
    specific classes that implement the 
    platform-specific functionality.
    """

    _ids_to_ignore: list[int]
    """
    The internal list of ids that must be ignored
    when trying to download a new one.
    """
    _do_ignore_ids: bool
    """
    The internal flag to indicate if the previously
    downloaded resources have to be ignored or not.
    """

    def __init__(
        self,
        do_ignore_ids: bool = False
    ):
        self._do_ignore_ids = do_ignore_ids

    def activate_ignore_ids(
        self
    ) -> None:
        """
        Set as True the internal flag that indicates 
        that the ids of the videos that are downloaded
        after being activated have to be ignored in 
        the next downloads, so each video is downloaded
        only once.
        """
        self._do_ignore_ids = True

    def deactivate_ignore_ids(
        self
    ) -> None:
        """
        Set as False the internal flag that indicates 
        that the ids of the videos that are downloaded
        after being activated have to be ignored in 
        the next downloads, so each video can be 
        downloaded an unlimited amount of times.
        """
        self._do_ignore_ids = True

    def reset(
        self
    ):
        """
        This method will empty the array that handles 
        the duplicated ids (if activated) to enable 
        downloading any image found again.
        """
        self._ids_to_ignore = []

    def _get_ids_to_ignore(
        self,
        ids_to_ignore: list[int]
    ):
        """
        Get the list of ids to ignore based on the 
        'ids_to_ignore' passed as parameter and also
        the ones holded in the instance, without
        duplicities.

        If the option of the instance is set to not
        ignore ids, the only ids to ignore will be 
        the ones passed as the 'ids_to_ignore'
        parameter.

        For internal use only.
        """
        return (
            list(set(ids_to_ignore + self._ids_to_ignore))
            if self._do_ignore_ids else
            ids_to_ignore
        )
    
    def _append_id(
        self,
        id: int
    ):
        """
        Append the provided 'id' to the internal list
        of ids to ignore, but only if the internal flag
        to do it is activated.

        For internal use only.
        """
        if (
            self._do_ignore_ids and
            id not in self._ids_to_ignore
        ):
            self._ids_to_ignore.append(id)

    @abstractmethod
    def download(
        self,
        query: str,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ):
        """
        Download the first available image from the
        platform and stores it locally with the
        'output_filename' name provided.
        """
        pass

    @abstractmethod
    def download_random(
        self,
        query: str,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ):
        """
        Download a random available image from the
        platform and stores it locally with the
        'output_filename' name provided.
        """
        pass

class StockImageDownloader(_StockDownloader):
    """
    Class to download stock images from the
    different platforms available.
    
    This is a general image downloader which
    will choose by itself the platform from
    which obtain the images. If you need a
    platform-specific stock image downloader,
    use one of the specific classes.
    """

    def __init__(
        self,
        do_ignore_ids: bool = False
    ):
        self._do_ignore_ids = do_ignore_ids
        self._pexels_downloader = PexelsImageDownloader(do_ignore_ids)
        self._pixabay_downloader = PixabayImageDownloader(do_ignore_ids)

    def reset(
        self
    ):
        """
        This method will empty the array that handles 
        the duplicated ids (if activated) to enable 
        downloading any image found again. This method
        will also reset its platform-specific 
        downloader instances.
        """
        self._pexels_downloader.reset()
        self._pixabay_downloader.reset()

    def download(
        self,
        query: str,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Download an image from the first platform that
        has results according to the provided 'query'
        and stores it locally.
        """
        output_filename = Output.get_filename(output_filename, FileTypeX.IMAGE)

        image = self._pexels_downloader.download(
            query = query,
            ids_to_ignore = ids_to_ignore,
            output_filename = output_filename
        )

        if image is not None:
            return image
        
        image = self._pixabay_downloader.download(
            query = query,
            ids_to_ignore = ids_to_ignore,
            output_filename = output_filename
        )

        if image is not None:
            return image
        
        # TODO: Use another provider when available
        raise Exception('No results found with any of our providers.')
    
    def download_random(
        self,
        query: str,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Download a random image from the first platform
        that has results according to the provided 'query'
        and stores it locally.
        """
        output_filename = Output.get_filename(output_filename, FileTypeX.IMAGE)

        image = self._pexels_downloader.download_random(
            query = query,
            ids_to_ignore = ids_to_ignore,
            output_filename = output_filename
        )

        if image is not None:
            return image
        
        image = self._pixabay_downloader.download_random(
            query = query,
            ids_to_ignore = ids_to_ignore,
            output_filename = output_filename
        )

        if image is not None:
            return image
        
        # TODO: Use another provider when available
        raise Exception('No results found with any of our providers.')

class StockVideoDownloader(_StockDownloader):
    """
    Class to download stock videos from the
    different platforms available.
    
    This is a general video downloader which
    will choose by itself the platform from
    which obtain the videos. If you need a
    platform-specific stock video downloader,
    use one of the specific classes.
    """

    def __init__(
        self,
        do_ignore_ids: bool = False
    ):
        self._do_ignore_ids = do_ignore_ids
        self._pexels_downloader = PexelsVideoDownloader(do_ignore_ids)
        self._pixabay_downloader = PixabayVideoDownloader(do_ignore_ids)

    def reset(
        self
    ):
        """
        This method will empty the array that handles 
        the duplicated ids (if activated) to enable 
        downloading any image found again. This method
        will also reset its platform-specific 
        downloader instances.
        """
        self._pexels_downloader.reset()
        self._pixabay_downloader.reset()

    def download(
        self,
        query: str,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Download a video from the first platform that
        has results according to the provided 'query'
        and stores it locally.
        """
        output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)

        video = self._pexels_downloader.download(
            query = query,
            ids_to_ignore = ids_to_ignore,
            output_filename = output_filename
        )

        if video is not None:
            return video
        
        video = self._pixabay_downloader.download(
            query = query,
            ids_to_ignore = ids_to_ignore,
            output_filename = output_filename
        )

        if video is not None:
            return video
        
        # TODO: Use another provider when available
        raise Exception('No results found with any of our providers.')
    
    def download_random(
        self,
        query: str,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Download a random video from the first platform
        that has results according to the provided 'query'
        and stores it locally.
        """
        output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)

        video = self._pexels_downloader.download_random(
            query = query,
            ids_to_ignore = ids_to_ignore,
            output_filename = output_filename
        )

        if video is not None:
            return video
        
        video = self._pixabay_downloader.download_random(
            query = query,
            ids_to_ignore = ids_to_ignore,
            output_filename = output_filename
        )

        if video is not None:
            return video
        
        # TODO: Use another provider when available
        raise Exception('No results found with any of our providers.')

class PexelsImageDownloader(_StockDownloader):
    """
    Class to provide images from the Pexels platform.

    This class uses the Pexels API and our registered
    API key to obtain the results.

    See: https://www.pexels.com/
    """

    def get_first(
        self,
        query: str,
        locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES,
        ids_to_ignore: list[int] = []
    ) -> Union[PexelsImage, None]:
        """
        Obtain the first available image from the Pexels
        provider for the given 'query' and 'locale' (if
        available).
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)
        locale = PexelsLocale.to_enum(locale)

        ids_to_ignore = self._get_ids_to_ignore(ids_to_ignore)

        return get_first_pexels_image(
            query,
            locale,
            ids_to_ignore
        )
    
    def get_random(
        self,
        query: str,
        locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES,
        ids_to_ignore: list[int] = []
    ) -> Union[PexelsImage, None]:
        """
        Obtain a random image from the Pexels provider
        for the given 'query' and 'locale' (if available).
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)
        locale = PexelsLocale.to_enum(locale)

        ids_to_ignore = self._get_ids_to_ignore(ids_to_ignore)

        return get_random_pexels_image(
            query,
            locale,
            ids_to_ignore
        )
    
    def download(
        self,
        query: str,
        locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> Union[FileReturn, None]:
        """
        Download the first image that is available in the
        Pexels provider for the given 'query' and 'locale'
        (if available).
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)
        locale = PexelsLocale.to_enum(locale)

        image = self.get_first(query, locale, ids_to_ignore)

        return (
            _download_image(self, image, output_filename)
            if image is None else
            None
        )
    
    def download_random(
        self,
        query: str,
        locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> Union[FileReturn, None]:
        """
        Download a random image that is available in the
        Pexels provider for the given 'query' and 'locale'
        (if available).
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)
        locale = PexelsLocale.to_enum(locale)

        image = self.get_random(query, locale, ids_to_ignore)

        return (
            _download_image(self, image, output_filename)
            if image is None else
            None
        )
    
class PexelsVideoDownloader(_StockDownloader):
    """
    Class to provide videos from the Pexels platform.

    This class uses the Pexels API and our registered
    API key to obtain the results.

    See: https://www.pexels.com/
    """

    def get_first(
        self,
        query: str,
        locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES,
        ids_to_ignore: list[int] = []
    ) -> Union[PexelsVideo, None]:
        """
        Obtain the first available video from the Pexels
        provider for the given 'query' and 'locale' (if
        available).
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)
        locale = PexelsLocale.to_enum(locale)

        ids_to_ignore = self._get_ids_to_ignore(ids_to_ignore)

        return get_first_pexels_video(
            query,
            locale,
            ids_to_ignore
        )
    
    def get_random(
        self,
        query: str,
        locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES,
        ids_to_ignore: list[int] = []
    ) -> Union[PexelsVideo, None]:
        """
        Obtain a random video that is available in the
        Pexels provider for the given 'query' and
        'locale' (if available).
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)
        locale = PexelsLocale.to_enum(locale)

        ids_to_ignore = self._get_ids_to_ignore(ids_to_ignore)

        return get_random_pexels_video(
            query,
            locale,
            ids_to_ignore
        )

    def download(
        self,
        query: str,
        locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> Union[FileReturn, None]:
        """
        Download the first video available in the Pexels
        platform with the given 'query' and 'locale' (if
        existing), avoiding the ones in the 'ids_to_ignore' 
        list.
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)
        locale = PexelsLocale.to_enum(locale)

        video = self.get_first(
            query,
            locale,
            ids_to_ignore,
        )

        return (
            _download_video(self, video, output_filename)
            if video is None else
            None
        )
    
    def download_random(
        self,
        query: str,
        locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> Union[FileReturn, None]:
        """
        Download a random video available in the Pexels
        platform with the given 'query' and 'locale' (if
        existing), avoiding the ones in the 'ids_to_ignore' 
        list.
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)
        locale = PexelsLocale.to_enum(locale)

        video = self.get_random(
            query,
            locale,
            ids_to_ignore,
        )

        return (
            _download_video(self, video, output_filename)
            if video is None else
            None
        )
    
class PixabayImageDownloader(_StockDownloader):
    """
    Class to provide images and videos from the Pixabay
    platform.

    This class uses the Pixabay API and our registered
    API key to obtain the results.

    See: https://pixabay.com/
    """

    def get_first(
        self,
        query: str,
        ids_to_ignore: list[int] = []
    ) -> Union[PixabayImage, None]:
        """
        Obtain the first image that is available in the
        Pexels provider for the given 'query'.
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)

        ids_to_ignore = self._get_ids_to_ignore(ids_to_ignore)

        return get_first_pixabay_image(
            query,
            ids_to_ignore
        )
    
    def get_random(
        self,
        query: str,
        ids_to_ignore: list[int] = []
    ) -> Union[PixabayImage, None]:
        """
        Obtain a random image that is available in the
        Pexels provider for the given 'query'.
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)

        ids_to_ignore = self._get_ids_to_ignore(ids_to_ignore)

        return get_random_pixabay_image(
            query,
            ids_to_ignore
        )
    
    def download(
        self,
        query: str,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> Union[FileReturn, None]:
        """
        Download the first image that is available in the
        Pexels platform for the given 'query'.
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)

        image = self.get_first(query, ids_to_ignore)

        return (
            _download_image(self, image, output_filename)
            if image is None else
            None
        )
    
    def download_random(
        self,
        query: str,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> Union[FileReturn, None]:
        """
        Download a random image that is available in the
        Pexels platform for the given 'query'.
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)

        image = self.get_random(query, ids_to_ignore)

        return (
            _download_image(self, image, output_filename)
            if image is None else
            None
        )
    
class PixabayVideoDownloader(_StockDownloader):
    """
    Class to provide videos from the Pixabay platform.

    This class uses the Pixabay API and our registered
    API key to obtain the results.

    See: https://pixabay.com/
    """

    def get_first(
        self,
        query: str,
        ids_to_ignore: list[int] = []
    ) -> Union[PixabayVideo, None]:
        """
        Obtain the first video that is available in the
        Pixabay platform for the given 'query'.
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)

        ids_to_ignore = self._get_ids_to_ignore(ids_to_ignore)

        return get_first_pixabay_video(
            query,
            ids_to_ignore
        )
    
    def get_random(
        self,
        query: str,
        ids_to_ignore: list[int] = []
    ) -> Union[PixabayVideo, None]:
        """
        Obtain a random video that is available in the
        Pixabay platform for the given 'query'.
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)

        ids_to_ignore = self._get_ids_to_ignore(ids_to_ignore)

        return get_random_pixabay_video(
            query,
            ids_to_ignore
        )

    def download(
        self,
        query: str,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> Union[FileReturn, None]:
        """
        Download the first video that is available in the
        Pexels platform for the given 'query' avoiding
        the ones in the 'ids_to_ignore' list.
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)

        video = self.get_first(query, ids_to_ignore)

        return (
            _download_video(self, video, output_filename)
            if video is None else
            None
        )
    
    def download_random(
        self,
        query: str,
        ids_to_ignore: list[int] = [],
        output_filename: Union[str, None] = None
    ) -> Union[FileReturn, None]:
        """
        Download a random video that is available in the
        Pexels platform for the given 'query' avoiding
        the ones in the 'ids_to_ignore' list.
        """
        validate_query(query)
        validate_ids_to_ignore(ids_to_ignore)

        video = self.get_random(query, ids_to_ignore)

        return (
            _download_video(self, video, output_filename)
            if video is None else
            None
        )
    
def _download_image(
    self: Union[PixabayImageDownloader, PexelsImageDownloader],
    image: Union[PixabayImage],
    output_filename: Union[str, None] = None
):
    """
    This method has been created to avoid the code
    duplicated when trying to download an image, so
    pay attention to pass the 'self' instance.

    For internal use only.
    """
    try:
        download = image.download(Output.get_filename(output_filename, FileTypeX.IMAGE))
        self._append_id(image.id)
    except:
        # TODO: Handle the exception
        download = None

    return download

def _download_video(
    self: Union[PixabayVideoDownloader, PexelsVideoDownloader],
    video: Union[PixabayVideo, PexelsVideo],
    output_filename: Union[str, None] = None
):
    """
    This method has been created to avoid the code
    duplicated when trying to download a video, so
    pay attention to pass the 'self' instance.

    For internal use only.
    """
    try:
        download = video.download(Output.get_filename(output_filename, FileTypeX.VIDEO))
        self._append_id(video.id)
    except:
        # TODO: Handle the exception
        download = None

    return download
    
# TODO: I should implement a way of using pagination
# and look for next page results if not found in the
# current page and a behaviour like that