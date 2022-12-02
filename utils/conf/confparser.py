from dotenv import load_dotenv, find_dotenv
from utils.path.pathparser import getDir

load_dotenv(find_dotenv(getDir(".env")))