import os
import aiohttp
import asyncio
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from parser.parser_webdriver import ParseWebDriver
from config import Kinopoisk

class ParseKinopoisk:
    """
    class which is dedicated to produce 
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    async def check_number(number:int) -> str:
        """
        Static method which is dedicated to check numbers
        Input:  number = number of values which was previously created
        Output: we returned number as a string
        """
        return str(number) if isinstance(number, int) or isinstance(number, float) \
                or not isinstance(number, str) else number

    async def produce_html_values(self, session:object, link:str) -> str:
        """
        Method which is dedicated to work with html values
        Input:  session = session which was previously developed
                link = link value which is required to work with
        Output: html value which is dedic
        """
        async with session.get(link) as r:
            if r.status == 200:
                return await r.text()
            return link

    async def produce_html_response(self, link:str) -> str:
        r = requests.get(link)
        if r.status_code == 200:
            return r.text
        return link

    async def produce_html_webdriver(self, link:str) -> str:
        """
        Method which is dedicated to create values of the link only with the 
        Input:  link = value of the link where required to find values of it
        Output: full html values of it
        """
        pass

    async def produce_html_parsing(self, html:str, value_link:str) -> dict:
        """
        Method which is dedicated to produce values of the actor/actress differentiating from it
        Input:  html = html which was previously parsed from it
                value_link = link value which was previously parsed
        Output: we successfully parsed values from the page as a dictionary
        """
        value_dict = {'link': value_link}
        if len(html) < 1000:
            return value_dict
        try:
            print(value_link)
            print('1<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            soup = BeautifulSoup(html, 'html.parser')
            # soup = soup.find_all("script")#[4]
            print(soup)

        except Exception as e:
            print(e)
        return value_dict

    @staticmethod
    async def produce_value_links(number:str) -> str:
        """
        Static method which is dedicated to produce values
        Input:  number = number which is requited to work with
        Output: we created link value for developing new values of it
        """
        return '/'.join([Kinopoisk.link, Kinopoisk.link_name, number])

    async def produce_main(self, numbers:list) -> list:
        """
        Method which is dedicated to produce values of the actors and get all of their information
        Input:  numbers = numbers of IDs of the Kinopoisk which possibly could be used as a parsing
        Output: we created lists of the dictionaries and developed the database for it
        """
        numbers = [asyncio.create_task(self.check_number(number)) for number in numbers]
        numbers = await asyncio.gather(*numbers)

        tasks = [asyncio.create_task(self.produce_value_links(number)) for number in numbers]
        links = await asyncio.gather(*tasks)

        semaphore = asyncio.Semaphore(Kinopoisk.semaphore)
        async with semaphore:
            
            tasks = [asyncio.create_task(self.produce_html_response(link)) for link in links]
            htmls = await asyncio.gather(*tasks)
        tasks = [asyncio.create_task(self.produce_html_parsing(html, link)) for html, link in zip(htmls[:1], links[:1])]
        return await asyncio.gather(*tasks)