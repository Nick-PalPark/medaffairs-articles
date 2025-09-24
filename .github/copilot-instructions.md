# MedAffairs Articles Repository

This repository manages medical and healthcare news articles for the MedAffairs.tech website. It contains tools to capture articles from Inoreader, process them into markdown files, generate JSON feeds, and sync data with the public website.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Development Environment
- Navigate to repository root: `cd /home/runner/work/medaffairs-articles/medaffairs-articles`
- Install dependencies: `pip3 install -r requirements.txt` (takes ~30 seconds)
- Create config: `cp config_template.py config.py` and fill in Inoreader credentials
- Test setup: `python3 test_capture.py` (should show 3/3 tests passing)

### Alternative Setup
- Use virtual environment: `python3 -m venv venv && source venv/bin/activate`
- Or use the wrapper script: `./run_capture.sh` (handles venv setup automatically)

## Validation

### ALWAYS Test Complete Workflows
After making any changes, ALWAYS validate by:
1. Run tests: `python3 test_capture.py` -- Should pass 3/3 tests
2. Test JSON generation: `python3 scripts/generate_articles_json.py --output test.json`
3. Verify JSON format: `python3 -c "import json; print(json.load(open('test.json')))"`
4. Test article capture if config available: `python3 capture_articles.py --dry-run`
5. Check markdown parsing works correctly on sample files

### Manual Validation Requirements
- ALWAYS run tests after code changes to capture workflow
- Verify JSON generation preserves manual_title values
- Test markdown file parsing for title and metadata extraction
- Validate output JSON structure matches expected format

## Data Format Requirements

### Critical: articles.json Structure
The JSON generation script outputs this structure:
```json
[
  {
    "id": "filename.md",
    "title": "Article Title from # Heading",
    "url": "https://example.com/article",
    "published": "2024-01-01T12:00:00Z",
    "source": "Source Name",
    "filepath": "articles/filename.md",
    "manual_title": "Custom Title (preserved)"
  }
]
```

### Markdown File Format
Articles are stored as markdown files with this structure:
```markdown
# Article Title

**URL:** https://example.com/article
**Published:** 2024-01-01
**Source:** Source Name

Article content goes here...
```

### Common Data Issues
- Missing `# Title` heading causes title extraction to fail
- Invalid **URL:** format won't be parsed correctly
- manual_title values are preserved when regenerating JSON
- File ID is derived from filename, used for matching existing entries

## File Structure and Navigation

### Repository Root Contents
```
.
├── capture_articles.py     # Main article capture script
├── scripts/
│   └── generate_articles_json.py  # Convert markdown to JSON
├── articles/               # Markdown files storage
├── config_template.py      # Configuration template
├── test_capture.py         # Test suite
├── requirements.txt        # Python dependencies
├── .github/workflows/      # GitHub Actions workflows
└── data/articles.json      # Generated JSON for website
```

### Key Code Locations
- **Article capture logic**: `capture_articles.py`, class `InoreaderClient`
- **JSON generation**: `scripts/generate_articles_json.py`, function `parse_mdfile`
- **HTML cleaning**: `capture_articles.py`, method `clean_html_content`
- **File processing**: `capture_articles.py`, class `ArticleProcessor`
- **Tests**: `test_capture.py`, functions `test_*`

## Common Tasks

### Adding New Articles
1. Create markdown file in `articles/` directory
2. Follow the standard format with `# Title` and metadata
3. Generate JSON: `python3 scripts/generate_articles_json.py`
4. Validate: `python3 -c "import json; json.load(open('articles.json'))"`

### Updating Article Processing
1. Edit `capture_articles.py` for capture logic changes
2. Edit `scripts/generate_articles_json.py` for JSON generation changes
3. ALWAYS run tests: `python3 test_capture.py`
4. Test with sample data before production use

### Managing Manual Titles
1. Edit `articles.json` directly to add `manual_title` field
2. Regenerate JSON: `python3 scripts/generate_articles_json.py --existing articles.json`
3. Manual titles are preserved when regenerating from markdown files
4. Match by URL or filename to preserve custom titles

### Troubleshooting Common Issues
- **Import errors**: Run `pip3 install -r requirements.txt`
- **Config not found**: Copy `config_template.py` to `config.py` and configure
- **Test failures**: Check dependencies and file permissions
- **JSON generation fails**: Verify markdown files have proper `# Title` format
- **Manual titles lost**: Use `--existing` parameter when regenerating

## Build and Deployment

### No Build Process Required
- This is a Python-based data processing repository
- No compilation or bundling needed
- Dependencies managed via pip/requirements.txt
- GitHub Actions handle automated workflows

### GitHub Actions Workflows
The repository includes several automated workflows:
1. **sync-articles.yml**: Captures articles and syncs with website (runs every 30 minutes)
2. **sync_data.yml**: Syncs articles.json from private data repository
3. **update_data.yml**: Updates data on external triggers

### Manual Workflow Triggers
You can manually trigger workflows from GitHub Actions tab:
- **Sync Articles**: Full capture and JSON generation
- **Force Sync**: Override rate limiting
- **Data Sync**: Sync from private repository

## Performance Notes

### Timing Expectations
- Test suite: ~5 seconds for 3 tests
- JSON generation: ~2 seconds for typical article count
- Article capture: ~30-60 seconds (depends on API responses)
- Full workflow: ~2-5 minutes total

### Rate Limiting
- Inoreader API has rate limits - respect them
- Manual workflow runs limited to once per 30 minutes
- Scheduled runs bypass rate limiting
- Use `force_sync` option to override if needed

## Development Workflow

### Making Changes
1. Install dependencies: `pip3 install -r requirements.txt`
2. Run existing tests: `python3 test_capture.py`
3. Make focused changes to specific components
4. Re-run tests to validate changes
5. Test with sample data before committing

### Testing New Features
1. Add test cases to `test_capture.py` following existing patterns
2. Test with minimal data first, then full dataset
3. Verify JSON structure matches expected format
4. Test manual_title preservation across regenerations
5. Validate markdown parsing edge cases

### Configuration Management
- Never commit `config.py` with real credentials
- Use `config_template.py` for documentation
- Set up GitHub secrets for automated workflows
- Test configuration changes with dry-run mode

Remember: This is a data processing pipeline. Most operations complete quickly, but API calls may take longer. Always test locally before pushing changes that affect article capture or processing.