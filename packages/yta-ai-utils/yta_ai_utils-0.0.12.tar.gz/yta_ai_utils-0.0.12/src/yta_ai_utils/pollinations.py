from yta_general_utils.downloader import Downloader
from yta_general_utils.dataclasses import FileReturn
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.url import encode_url_parameter
from typing import Union


class Pollinations:
    """
    Class to wrap prodia functionality. Prodia is an
    image generator engine.
    """

    @staticmethod
    def generate_image(
        prompt: str,
        output_filename: Union[str, None] = None
    ) -> FileReturn:
        if not PythonValidator.is_string(prompt):
            raise Exception('The provided "prompt" is not a valid string.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.IMAGE)
        
        prompt = encode_url_parameter(prompt)

        # TODO: Make some of these customizable
        WIDTH = 1920
        HEIGHT = 1080
        # TODO: This seed should be a random value or
        # I will receive the same image with the same
        # prompt
        SEED = 43
        MODEL = 'flux'

        url = f'https://pollinations.ai/p/{prompt}?width={WIDTH}&height={HEIGHT}&seed={SEED}&model={MODEL}'

        return Downloader.download_image(url, output_filename)

"""
    Check because there is also a model available for
    download and to work with it (as they say here
    https://pollinations.ai/):

    # Using the pollinations pypi package
    ## pip install pollinations

    import pollinations as ai

    model_obj = ai.Model()

    image = model_obj.generate(
        prompt=f'Awesome and hyperrealistic photography of a vietnamese woman... {ai.realistic}',
        model=ai.flux,
        width=1038,
        height=845,
        seed=43
    )
    image.save('image-output.jpg')

    print(image.url)
    """