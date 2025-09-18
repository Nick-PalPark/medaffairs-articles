# Auto-generated config.py for capture_articles.py - DO NOT COMMIT
# Populated from repository secrets at runtime by Actions

INOREADER_APP_ID = "test_app_id"
INOREADER_APP_KEY = "test_app_key"

# OAuth refresh token (preferred for automation)
# To obtain: authorize medaffairs.tech app and store refresh_token in INOREADER_REFRESH_TOKEN secret
INOREADER_REFRESH_TOKEN = "test_refresh_token" if "test_refresh_token" else None

# Username/password (fallback when refresh token not available)
INOREADER_USERNAME = "test_user"
INOREADER_PASSWORD = "test_password"

INOREADER_API_BASE = "https://www.inoreader.com/reader/api/0/"
INOREADER_AUTH_URL = "https://www.inoreader.com/oauth2/token"

ARTICLES_DIR = "articles"
MAX_ARTICLES = 50
DAYS_BACK = 7
