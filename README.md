# medaffairs.tech — Article Capture and Processing

This repository captures medical and healthcare articles from Zapier tables and processes them for the medaffairs.tech website. It features a streamlined workflow that automatically fetches, processes, and publishes articles.

## Automated Workflow

The repository includes a single, streamlined GitHub Actions workflow (`update_data.yml`) that handles the complete pipeline:

### What it does:
1. **Captures articles** - Fetches new articles from Zapier table and saves them as markdown files in `articles/`
2. **Generates raw JSON** - Creates `articles.json` from all markdown files with metadata
3. **Transforms for website** - Converts to structured format with heroes and categorized columns in `data/articles.json`
4. **Commits changes** - Automatically commits all updated files
5. **Triggers website update** - Sends repository_dispatch to medaffairs.tech for immediate publishing

### Schedule:
- Runs daily at 08:00 UTC
- Can be triggered manually via workflow_dispatch

### Requirements:
- `ZAPIER_TABLE_ID`, `ZAPIER_API_KEY` secrets for table access
- `MEDAFFAIRS_TECH_PAT` secret with repository dispatch permissions for the medaffairs.tech repo

**📖 For detailed setup instructions, see [SETUP_ZAPIER_ACCESS.md](SETUP_ZAPIER_ACCESS.md)**

## Article Processing

### Raw Data Format (articles.json)
The workflow generates a raw JSON array with article metadata:
```json
[
  {
    "id": "2025-01-15_Article-Title.md",
    "title": "Article Title", 
    "url": "https://example.com/article",
    "published": "2025-01-15 12:00:00",
    "source": "Medical Journal",
    "filepath": "articles/2025-01-15_Article-Title.md",
    "manual_title": "Custom Title (if set)"
  }
]
```

### Website Format (data/articles.json)
The raw data is transformed to the structured format expected by medaffairs.tech:
```json
{
  "last_updated": 1736956800000,
  "heroes": [
    {"title": "Featured Article", "url": "...", "image": "..."}
  ],
  "columns": {
    "news": [...],
    "tech": [...], 
    "opinion": [...]
  }
}
```

## Manual Title Editing
- Edit `articles.json` directly to add `manual_title` values
- Manual titles take precedence over auto-generated titles
- Changes are preserved when the workflow regenerates the JSON

## Scripts
- `capture_articles.py` - Main article capture script
- `scripts/generate_articles_json.py` - Converts markdown files to raw JSON
- `scripts/transform_to_site_format.py` - Transforms raw JSON to website format
- `test_zapier_connection.py` - Test script to validate Zapier API setup
