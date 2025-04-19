from yta_general_utils.programming.env import Environment
from yta_general_utils.downloader import Downloader
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileExtension
from yta_general_utils.dataclasses import FileReturn
from PIL import Image
from abc import ABC, abstractmethod
from typing import Union
from random import choice

import requests


class GifDownloader(ABC):
    """
    Abstract class to be inherited from other classes
    to download gifs.
    """

    @abstractmethod
    def download(
        self,
        keywords: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Download a gif found with the given 'keywords'.
        """
        pass

class GiphyGifDownloader(GifDownloader):
    """
    Gif downloader that uses the Giphy platform.
    """

    _GIPHY_API_KEY = Environment.get_current_project_env('GIPHY_API_KEY')

    def download(
        self,
        keywords: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        """
        Download a random gif from Giphy platform using 
        an API key.

        This method returns None if no gif found or the
        final 'output_filename' with it's been locally
        stored.

        For more information, check this:
        - https://developers.giphy.com/dashboard/
        """
        if not output_filename:
            return None
        
        limit = 5

        url = "http://api.giphy.com/v1/gifs/search"
        url += f'?q={keywords}&api_key={self._GIPHY_API_KEY}&limit={str(limit)}'

        response = requests.get(url)
        response = response.json()

        if not response or len(response['data']) == 0:
            # TODO: Raise exception of no gif found
            print(f'No gif found with the keywords "{keywords}".')
            return None
        
        output_filename = Output.get_filename(output_filename, FileExtension.WEBP)

        element = choice(response['data'])
        gif_url = 'https://i.giphy.com/' + element['id'] + '.webp'

        output_filename = Output.get_filename(output_filename, FileExtension.WEBP)
        Downloader.download_image(gif_url, output_filename)

        return FileReturn(
            Image.open(output_filename),
            output_filename
        )