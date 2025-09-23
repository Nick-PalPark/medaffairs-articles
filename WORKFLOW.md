# Article Workflow Documentation

## New Workflow: sync-articles.yml

This repository includes a GitHub Actions workflow that automates the article capture and JSON generation process with enhanced scheduling and manual trigger capabilities.

### What it does:
1. **Runs capture_articles.py** - Fetches new articles from Inoreader and saves them as markdown files in `articles/`
2. **Generates articles.json** - Uses `scripts/generate_articles_json.py` to create a normalized JSON file from all markdown files
3. **Preserves manual titles** - Any `manual_title` values in the existing articles.json are preserved when rebuilding
4. **Commits changes** - Automatically commits updated articles.json and any new article files
5. **Triggers medaffairs.tech** - Sends a repository_dispatch event to update the public website
6. **Rate limiting** - Prevents excessive manual runs (1 per 30 minutes unless forced)
7. **Enhanced logging** - Detailed logging with grouped output for better visibility

### Schedule:
- Runs twice daily at 08:00 UTC and 20:00 UTC
- Can be triggered manually via workflow_dispatch with options:
  - Sync type selection (full, articles_only, json_only)
  - Rate limit override option

### Requirements:
- `MEDAFFAIRS_TECH_PAT` secret must be configured with a Personal Access Token that has repository dispatch permissions for the medaffairs.tech repo
- Inoreader API credentials must be configured as repository secrets:
  - `INOREADER_APP_ID`
  - `INOREADER_APP_KEY` 
  - `INOREADER_USERNAME`
  - `INOREADER_PASSWORD`

### Features:
- **Rate Limiting**: Manual triggers are limited to once per 30 minutes (configurable)
- **Selective Sync**: Choose between full sync, articles only, or JSON generation only
- **Force Override**: Bypass rate limiting when necessary
- **Comprehensive Logging**: Grouped output with clear success/failure indicators
- **Error Recovery**: Automatic backup and restore of articles.json
- **Validation**: JSON validation and article count verification
- **Security**: Automatic cleanup of sensitive configuration files

### Scripts:
- `scripts/generate_articles_json.py` - Standalone script that builds articles.json from markdown files
  - Extracts titles from `# Title` headings
  - Parses metadata like `**URL:**`, `**Published:**`, `**Source:**`
  - Preserves existing `manual_title` values by matching on URL or filename
  - Outputs normalized JSON array format

### Manual Usage:
```bash
# Generate articles.json from markdown files (preserving manual titles)
python scripts/generate_articles_json.py --articles-dir articles --output articles.json

# Generate with custom paths
python scripts/generate_articles_json.py --articles-dir /path/to/articles --output /path/to/output.json --existing /path/to/existing.json
```