from dotenv import dotenv_values

config = dotenv_values(".env")

ASF_HOSTS = config.get("ASF_HOSTS").split(",")
ASF_PASSWORD = config.get("ASF_PASSWORD")

FARM_AT_UTC_TIME = config.get("FARM_AT_UTC_TIME")
