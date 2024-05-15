import random
import time

import requests
from loguru import logger
from openpyxl import Workbook
from tqdm import tqdm

from config import USE_MOBILE_PROXY, IP_CHANGE_LINK


def read_from_txt(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
    except Exception as e:
        raise Exception(f"Encountered an error while reading a txt file '{file_path}': {str(e)}")


def export_json(data, destination):
    try:
        workbook = Workbook()
        sheet = workbook.active

        headers = ["Address", "Scroll Marks"]
        sheet.append(headers)

        for key, value in data.items():
            sheet.append([key, value])

        workbook.save(destination)

    except Exception as e:
        logger.error(f"Encountered an error while exporting db to Excel: {str(e)}")
        exit()


def change_mobile_ip() -> None:
    try:
        if USE_MOBILE_PROXY:
            res = requests.get(IP_CHANGE_LINK)

            if res.status_code == 200:
                logger.info("IP address changed successfully", send_to_tg=False)
            else:
                raise Exception("Failed to change IP address")

    except Exception as e:
        raise Exception(f"Encountered an error when changing ip address, check your proxy provider: {e}")


def sleep(delay_range):
    random_delay = random.randint(*delay_range)
    with tqdm(total=random_delay, desc="Waiting", unit="s", dynamic_ncols=True, colour="blue") as pbar:
        for _ in range(random_delay):
            time.sleep(1)
            pbar.update(1)


def print_greeting_msg():
    start_message = r"""
                   __    _ __                        __                  
       _______  __/ /_  (_) /  _   __   ____  ____ _/ /______  ____  ___ 
      / ___/ / / / __ \/ / /  | | / /  /_  / / __ `/ //_/ __ \/ __ \/ _ \
     (__  ) /_/ / /_/ / / /   | |/ /    / /_/ /_/ / ,< / /_/ / / / /  __/   
    /____/\__, /_.___/_/_/    |___/    /___/\__,_/_/|_|\____/_/ /_/\___/ 
         /____/      """

    logger.success(start_message)