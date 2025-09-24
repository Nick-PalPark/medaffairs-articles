# Article Workflow Documentation

# Article Workflow Documentation

## Streamlined Workflow: update_data.yml

This repository features a single, comprehensive GitHub Actions workflow that handles the complete article processing pipeline from RSS capture to website publication.

### What it does:
1. **Captures articles** - Runs `capture_articles.py` to fetch new articles from Inoreader and save as markdown files in `articles/`
2. **Generates raw JSON** - Uses `scripts/generate_articles_json.py` to create `articles.json` from all markdown files
3. **Transforms for website** - Uses `scripts/transform_to_site_format.py` to convert raw data to structured format in `data/articles.json`
4. **Preserves manual titles** - Any `manual_title` values in existing articles.json are preserved when rebuilding
5. **Commits changes** - Automatically commits updated markdown files and both JSON formats
6. **Triggers medaffairs.tech** - Sends repository_dispatch event to update the public website

### Schedule:
- Runs daily at 08:00 UTC
- Can be triggered manually via workflow_dispatch

### Requirements:
- `INOREADER_APP_ID`, `INOREADER_APP_KEY`, `INOREADER_USERNAME`, `INOREADER_PASSWORD` secrets for RSS access
- `MEDAFFAIRS_TECH_PAT` secret with repository dispatch permissions for medaffairs.tech repo

### Scripts:
- `capture_articles.py` - Main capture script that fetches articles from Inoreader RSS feeds
- `scripts/generate_articles_json.py` - Converts markdown files to raw JSON array format
  - Extracts titles from `# Title` headings
  - Parses metadata like `**URL:**`, `**Published:**`, `**Source:**`
  - Preserves existing `manual_title` values by matching on URL or filename
  - Outputs normalized JSON array format
- `scripts/transform_to_site_format.py` - Transforms raw JSON to website format
  - Creates structured format with `heroes` and categorized `columns`
  - Selects top articles as featured heroes
  - Categorizes articles into news/tech/opinion based on keywords
  - Adds timestamp and proper formatting for the website

### Manual Usage:
```bash
# Complete pipeline (same as workflow)
python capture_articles.py
python scripts/generate_articles_json.py --articles-dir articles --output articles.json
python scripts/transform_to_site_format.py --input articles.json --output data/articles.json

# Individual steps with custom paths
python scripts/generate_articles_json.py --articles-dir /path/to/articles --output /path/to/output.json --existing /path/to/existing.json
python scripts/transform_to_site_format.py --input raw-articles.json --output site-data.json
```

### Data Flow:
1. **RSS Feeds** → `capture_articles.py` → **Markdown files** in `articles/`
2. **Markdown files** → `generate_articles_json.py` → **Raw JSON** (`articles.json`)  
3. **Raw JSON** → `transform_to_site_format.py` → **Website JSON** (`data/articles.json`)
4. **Website JSON** → repository_dispatch → **medaffairs.tech website update**