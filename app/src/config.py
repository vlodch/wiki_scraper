import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
WIKI_BASE_URL = os.getenv('WIKI_BASE_URL', 'https://en.wikipedia.org')
MAX_LINKS_PER_PAGE = int(os.getenv('MAX_LINKS_PER_PAGE', 9))
