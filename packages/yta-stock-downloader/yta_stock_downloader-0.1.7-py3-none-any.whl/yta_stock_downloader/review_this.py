"""
TODO: Delete this class. I should not handle repeated
images or videos in memory here, this must be done in
the specific class that implements it.
"""
from yta_stock_downloader.pexels.dataclasses import PexelsImagePageResult
from yta_stock_downloader.pexels.image import search_pexels_images
from yta_general_utils.downloader.image import download_image
from yta_general_utils.programming.output import Output
from yta_general_utils.file.filename import get_file_extension


# TODO: I'm using pagination here, so I keep this code
# until the next commit to check if I reuse the code
# to implement pagination in all these stock downloader
# classes

class StockPexelsDownloader:
    """
    This object is useful to get and download stock images.
    """
    __instance = None

    def __new__(cls, ignore_repeated = True):
        if not StockPexelsDownloader.__instance:
            StockPexelsDownloader.__instance = object.__new__(cls)
        
        return StockPexelsDownloader.__instance

    def __init__(self, ignore_repeated = True):
        if not hasattr(self, 'ignore_repeated'):
            self.ignore_repeated = ignore_repeated
            self.__ignore_image_ids = []
            self.__ignore_video_ids = []

    # TODO: Set those 'locale' as Enums
    # TODO: Maybe 'results_per_page' is not needed as parameter
    def search_images(
        self,
        query: str,
        locale: str = 'es-ES',
        results_per_page: int = 25,
        page: int = 1
    ) -> PexelsImagePageResult:
        """
        Looks for the available images according to the provided 'query'.
        """
        if not query:
            return None
        
        if not locale:
            # TODO: As we will apply enums this will be avoided
            return None
        
        if results_per_page < 1:
            results_per_page = 1

        if results_per_page > 25:
            results_per_page = 25

        if page < 1:
            page = 1

        return search_pexels_images(query, locale, results_per_page, page)
    
    def download_first_image(self, query: str, locale: str = 'es-ES', output_filename: str = ''):
        """
        Downloads the first valid and available image according to the
        provided 'query' and stores it (if found) as 'output_filename'.

        If no 'output_filename' provided, it will use a temporary file
        (that could be deleted by internal functions).
        """
        # TODO: Should I raise exception instead (?)
        if not query:
            return None
        
        photos_page_result = self.search_images(query, locale)

        if not photos_page_result:
            return None
        
        photo_to_download = None
        
        if self.ignore_repeated:
            current_page = 1

            while current_page <= photos_page_result.total_pages:
                # We need fire a new request for the next page
                if current_page > 1:
                    photos_page_result = search_pexels_images(query, locale, page = current_page)

                for photo in photos_page_result.photos:
                    if photo.id not in self.__ignore_image_ids:
                        # Photo available and not repeated, so we can use it
                        photo_to_download = photo
                        self.__ignore_image_ids.append(photo_to_download.id)
                        # To stop the while loop
                        current_page = photos_page_result.total_pages
                        break

                current_page += 1
        else:
            photo_to_download = photos_page_result.photos[0]

        if not photo_to_download:
            # Results found but all repeated
            return None

        # TODO: I'm hardcoding the 'landscape' format url here, but... you know...
        download_url = photo_to_download.src['landscape'].split('?')[0]
        
        # We make sure it fits the image extension
        downloaded = download_image(
            download_url,
            Output.get_filename(output_filename, get_file_extension(download_url))
        )

        if not downloaded:
            return None
        
        return output_filename