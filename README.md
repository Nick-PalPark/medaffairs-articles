# Medical Affairs Articles Capture

An automated workflow to capture and store articles from Inoreader RSS feeds as markdown files.

## Features

- Connects to Inoreader API to fetch unread articles
- Converts articles to clean markdown format
- Automatically organizes articles by date and title
- Configurable article count and date range
- HTML content cleaning and basic markdown conversion
- Prevents duplicate article downloads

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Inoreader API Access

1. Register your application at [Inoreader Developers](https://www.inoreader.com/developers/)
2. Get your App ID and App Key
3. Copy the configuration template:
   ```bash
   cp config_template.py config.py
   ```
4. Edit `config.py` with your credentials:
   ```python
   INOREADER_APP_ID = "your_app_id_here"
   INOREADER_APP_KEY = "your_app_key_here"
   INOREADER_USERNAME = "your_username"
   INOREADER_PASSWORD = "your_password"
   ```

### 3. Configure Settings (Optional)

In `config.py`, you can adjust:
- `MAX_ARTICLES`: Maximum articles to fetch per run (default: 50)
- `DAYS_BACK`: How many days back to look for articles (default: 7)
- `ARTICLES_DIR`: Directory to save articles (default: "articles")

## Usage

### Run the Articles Capture Workflow

```bash
python capture_articles.py
```

This will:
1. Authenticate with Inoreader API
2. Fetch your unread articles from the last 7 days
3. Convert them to markdown format
4. Save them in the `articles/` directory

### Article Format

Each article is saved as a markdown file with:
- Sanitized filename based on date and title
- Metadata header (source, author, published date, URLs)
- Clean content converted from HTML
- Timestamp of when it was captured

Example filename: `2024-01-15_New-Medical-Research-Breakthrough.md`

### Automation

To run automatically, you can set up a cron job:

```bash
# Run every 6 hours
0 */6 * * * cd /path/to/medaffairs-articles && python capture_articles.py
```

## File Structure

```
medaffairs-articles/
├── articles/                    # Captured articles (markdown files)
│   └── example-article.md
├── capture_articles.py          # Main workflow script
├── config_template.py           # Configuration template
├── config.py                    # Your configuration (ignored by git)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Troubleshooting

### Authentication Issues
- Verify your App ID and App Key are correct
- Ensure your Inoreader username/password are valid
- Check that your app has the 'read' scope enabled

### No Articles Found
- Check if you have unread articles in Inoreader
- Adjust `DAYS_BACK` setting to look further back
- Verify your feeds are still active

### Import Errors
- Install all requirements: `pip install -r requirements.txt`
- Ensure `config.py` exists and is properly configured

## API Rate Limits

Inoreader has API rate limits. The script includes basic error handling, but for heavy usage consider:
- Reducing `MAX_ARTICLES` setting
- Running less frequently
- Implementing exponential backoff for retries
