from dotenv import dotenv_values
import logging

config = dotenv_values(".env")

ASF_HOSTS = config.get("ASF_HOSTS").split(",")
ASF_PASSWORD = config.get("ASF_PASSWORD")

STEAM_ID = config["STEAM_ID"]
STEAM_SESSION_ID = config.get("STEAM_SESSION_ID")
STEAM_LOGIN_SECURE = config["STEAM_LOGIN_SECURE"]

MAX_ATTEMPTS = int(config.get("MAX_ATTEMPTS"))
FARM_AT_UTC_TIME = config.get("FARM_AT_UTC_TIME")

LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = "%(levelname)s | %(asctime)s | %(name)s (%(filename)s).%(funcName)s(%(lineno)d) -> %(message)s"
LOGGING_DATEFORMAT = "%Y-%m-%d %H:%M:%S"
