from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.downloader import Downloader
from typing import Union

from openai import OpenAI


# TODO: Is this actually useful? I think it could be removed...
class OpenAI:
    """
    Class to wrap the OpenAI functionality.
    """
    
    def generate_image(
        prompt: str,
        output_filename: Union[str, None] = None
    ):
        if not PythonValidator.is_string(prompt):
            raise Exception('The provided "prompt" is not a valid string.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.IMAGE)

        client = OpenAI()

        response = client.images.generate(
            model = "dall-e-3",
            prompt = prompt,
            size = "1792x1024",
            quality = "standard",
            n = 1,
        )

        image_url = response.data[0].url

        return Downloader.download_image(image_url, output_filename)