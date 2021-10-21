import os
from PIL import Image
import requests
from io import BytesIO
from multiprocessing import Pool


class ModelGender:
    """
    class which is dedicated to produce values of the gender to selected values
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_image_content(value_link:str) -> list:
        """
        Method which is dedicated to develop values of the 
        Input:  value_link = link value of the image location
        Output: list of the image bytes
        """
        response = requests.get(value_link, stream=True)
        return BytesIO(response.content)

    def get_image_value(self, value_image:str) -> str:
        """
        Method which is dedicated to develop values of the image from the
        Input:  value_image = string value of the image
        Output: we develop values of the image to detect it from it
        """
        pass

    def produce_gender_search_manually(self, value_text:str) -> int:
        """
        Method which is dedicated to produce values from the 
        Input:  value_text = text about the user
        Output: we developed value of the id to which gender of it
        """
        pass

    def produce_gender_search_modelling(self, value_image:str) -> int:
        """
        Method which is dedicated to develop values of the image
        Input:  value_image = image string for the development
        Output: 
        """
        pass

    def produce_values_main(self) -> None:
        """
        Method which is dedicated to produce values into the datbase with produce values
        of the gender to the database
        Input:  None
        Output: we created values of the 
        """
        pass