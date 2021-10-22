import os
import cv2
from pprint import pprint
from PIL import Image
import requests
from io import BytesIO
from multiprocessing import Pool
from db.db_main import DataBaseMain
from db.db_creator import User, association_table_user_gender
from models.model_downloader import ModelDownloader


class ModelGender:
    """
    class which is dedicated to produce values of the gender to selected values
    """
    def __init__(self) -> None:
        self.gender_net, self.gender_deploy, self.face_detector_pb, \
            self.face_detector_pbtxt = ModelDownloader().download_gender_detection_models()
        self.session = DataBaseMain().return_session()
        self.net_face = cv2.dnn.readNet(self.face_detector_pb, self.face_detector_pbtxt)
        self.net_gender = cv2.dnn.readNet(self.gender_net, self.gender_deploy)
        self.model_mean = (78.426784342837218, 87.483941943331134, 114.8954327372182929)

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
        value_male = ['he', 'him', 'his']
        value_female = ['she', 'her', 'hers']
        value_text = [''.join(e for e in f if e.isalnum()).lower() for f in value_text.split()]
        count_male = sum([value_text.count(f) for f in value_male])
        count_female = sum([value_text.count(f) for f in value_female])
        if count_male > count_female:
            return 'Male'
        elif count_male < count_female:
            return 'Female'
        return 'Unknown'

    def produce_gender_search_modelling(self, value_image:str) -> int:
        """
        Method which is dedicated to develop values of the image
        Input:  value_image = image string for the development
        Output: value of the model which was previously checked
        """
        pass

    def produce_values_main(self) -> None:
        """
        Method which is dedicated to produce values into the datbase with produce values
        of the gender to the database
        Input:  None
        Output: we created values of the 
        """
        user_gender_specified = self.session.query(User.id).filter(association_table_user_gender.c.id_user== User.id).all()
        user_gender_specified = [f[0] for f in user_gender_specified]
        user_gender_specified = []
        user_desc_images_gender_without = self.session.query(
            User.id, User.description, User.link_image).filter(~User.id.in_(user_gender_specified)).all()
        value_gender_manual = [[i, self.produce_gender_search_manually(text)] 
            if text else 'Unknown' for i, text, _ in user_desc_images_gender_without]
        value_image = [self.get_image_content(link) for i, _, link in user_desc_images_gender_without[:2]]
        