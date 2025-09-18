# Inoreader API Configuration
# Copy this file to config.py and fill in your actual credentials

# Inoreader API credentials
# Get these from https://www.inoreader.com/developers/
INOREADER_APP_ID = "your_app_id_here"
INOREADER_APP_KEY = "your_app_key_here"

# OAuth2 credentials - Two options available:

# Option 1 (PREFERRED for automation): OAuth refresh token
# Obtain by authorizing medaffairs.tech app through Inoreader OAuth flow
# More secure and stable for automated workflows
# INOREADER_REFRESH_TOKEN = "your_refresh_token_here"

# Option 2 (fallback): Username and password
# Used when refresh token is not available
INOREADER_USERNAME = "your_username"
INOREADER_PASSWORD = "your_password"

# API endpoints
INOREADER_API_BASE = "https://www.inoreader.com/reader/api/0/"
INOREADER_AUTH_URL = "https://www.inoreader.com/oauth2/token"

# Output settings
ARTICLES_DIR = "articles"
MAX_ARTICLES = 50  # Maximum number of articles to fetch per run
DAYS_BACK = 7      # How many days back to look for articles