from yta_general_utils.programming.env import Environment
from yta_general_utils.programming.validator import PythonValidator

import google.generativeai as genai


GEMINI_API_KEY =  Environment.get_current_project_env('GEMINI_API_KEY')

class Gemini:
    """
    Class to wrap the Gemini AI chatbot.
    """

    @staticmethod
    def ask(
        prompt: str
    ):
        """
        Ask Gemini AI (gemini-1.5-flash) model by using the
        provided 'prompt' and return its response.
        """
        if not PythonValidator.is_string(prompt):
            raise Exception('The provided "prompt" is not a valid string.')

        genai.configure(api_key = GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        chat = model.start_chat()
        response = chat.send_message(
            prompt,
        )

        return response.text