# Article Workflow Documentation

## New Workflow: update_data.yml

This repository now includes a GitHub Actions workflow that automates the article capture and JSON generation process.

### What it does:
1. **Runs capture_articles.py** - Fetches new articles from Inoreader and saves them as markdown files in `articles/`
2. **Generates articles.json** - Uses `scripts/generate_articles_json.py` to create a normalized JSON file from all markdown files
3. **Preserves manual titles** - Any `manual_title` values in the existing articles.json are preserved when rebuilding
4. **Commits changes** - Automatically commits updated articles.json and any new article files
5. **Triggers medaffairs.tech** - Sends a repository_dispatch event to update the public website

### Schedule:
- Runs daily at 08:00 UTC
- Can also be triggered manually via workflow_dispatch

### Requirements:
- `MEDAFFAIRS_TECH_PAT` secret must be configured with a Personal Access Token that has repository dispatch permissions for the medaffairs.tech repo

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