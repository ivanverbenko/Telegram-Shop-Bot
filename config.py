import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ['TOKEN']

ADMINS = []
DATABASE_URL = os.environ['DATABASE_URL']