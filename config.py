from dotenv import dotenv_values
import logging

config = dotenv_values(".env")

ASF_HOSTS = config["ASF_HOSTS"].split(",")
ASF_PASSWORD = config["ASF_PASSWORD"]

ASF_MAIN_HOST = config["ASF_MAIN_HOST"]
ASF_MAIN_BOT_NAME = config["ASF_MAIN_BOT_NAME"]

STEAM_ID = config["STEAM_ID"]
STEAM_SESSION_ID = config["STEAM_SESSION_ID"]
STEAM_LOGIN_SECURE = config["STEAM_LOGIN_SECURE"]

MAX_ATTEMPTS = int(config["MAX_ATTEMPTS"])
PRICE_OFFSET = float(config["PRICE_OFFSET"])
FARM_AT_UTC_TIME = config["FARM_AT_UTC_TIME"]

LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = "%(levelname)s | %(asctime)s | %(name)s (%(filename)s).%(funcName)s(%(lineno)d) -> %(message)s"
LOGGING_DATEFORMAT = "%Y-%m-%d %H:%M:%S"
