from yta_ai_utils.blip import Blip
from yta_ai_utils.llava import Llava
from yta_general_utils.programming.validator import PythonValidator
from PIL import Image
from typing import Union
from abc import ABC, abstractmethod

import numpy as np


class ImageDescriptor(ABC):
    """
    Class to describe images.
    """

    @abstractmethod
    def describe(
        self,
        image: Union[str, Image.Image, np.ndarray]
    ) -> str:
        """
        Describe the provided 'image' using an engine
        capable of it.
        """
        pass

class DefaultImageDescriptor(ImageDescriptor):
    """
    Default class to describe an image. It will choose the
    engine we think is a good choice in general.

    The process could take from seconds to a couple of minutes
    according to the system specifications.
    """
    def describe(
        self,
        image: Union[str, Image.Image, np.ndarray]
    ) -> str:
        return BlipImageDescriptor().describe(image)

class BlipImageDescriptor(ImageDescriptor):
    """
    Class to describe an image using the Blip engine, which
    is from Salesforce and will use pretrained models that are
    stored locally in 'C:/Users/USER/.cache/huggingface/hub',
    loaded in memory and used to describe it.

    The process could take from seconds to a couple of minutes
    according to the system specifications.
    """

    def describe(
        self,
        image: Union[str, Image.Image, np.ndarray]
    ) -> str:
        return Blip.describe(image)
    
class LlavaImageDescriptor(ImageDescriptor):
    """
    Class to describe an image using the Llava engine
    through the 'ollama' python package.
    """

    def describe(
        self,
        image_filename: str
    ):
        """
        THIS METHOD IS NOT WORKING YET.

        TODO: This is not working because of my pc limitations.
        It cannot load the resources due to memory capacity.
        """
        if not PythonValidator.is_string(image_filename):
            raise Exception('The provided "image_filename" is not a valid string.')

        return Llava.describe(image_filename)