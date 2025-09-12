# medaffairs-articles

This private repository provides automated article ingestion and management for [medaffairs.tech](https://github.com/Nick-PalPark/medaffairs.tech). It fetches articles from Inoreader, generates headlines using OpenAI, and provides a web-based editor for content management.

## Features

- **Automated Article Fetching**: Retrieves tagged articles from Inoreader API
- **AI-Powered Headlines**: Generates engaging headlines using OpenAI (optional)
- **Manual Override System**: Edit titles and manage featured content
- **Hero/Column Management**: Designate featured articles with enforced limits
- **Web-Based Editor**: Browser interface for content management
- **GitHub Actions Integration**: Automated updates every 4 hours

## Repository Structure

```
├── articles.json          # Main articles database (auto-generated)
├── scripts/
│   └── fetch_inoreader.py # Article fetching and processing script
├── admin/
│   ├── editor.html        # Web-based article editor
│   ├── editor.js          # Editor JavaScript functionality
│   └── README.md          # Admin tools documentation
├── .github/workflows/
│   └── update_data.yml    # Automated update workflow
├── articles/              # Legacy: Manual Markdown articles
├── metadata/              # Legacy: Manual JSON metadata files
└── README.md              # This file
```

## Setup

### 1. Required Secrets

Configure these secrets in your repository settings:

- `INOREADER_APP_ID`: Your Inoreader application ID
- `INOREADER_API_KEY`: Your Inoreader API key  
- `OPENAI_API_KEY`: Your OpenAI API key (optional, for headline generation)

### 2. Repository Variables (Optional)

Configure these variables for customization:

- `INOREADER_TAG`: Tag to fetch from Inoreader (default: "medaffairs")
- `MAX_HEROES`: Maximum number of hero articles (default: 3)
- `MAX_COLUMNS`: Maximum number of column articles (default: 6)

### 3. Inoreader Setup

1. Create an Inoreader account at [inoreader.com](https://www.inoreader.com)
2. Apply for API access through their developer program
3. Tag relevant articles with your chosen tag (e.g., "medaffairs")
4. Add your API credentials to repository secrets

### 4. OpenAI Setup (Optional)

1. Create an OpenAI account and get an API key
2. Add the key to repository secrets as `OPENAI_API_KEY`
3. Headlines will be auto-generated for new articles

## Usage

### Automated Operation

The system runs automatically every 4 hours via GitHub Actions:

1. **Fetches** tagged articles from Inoreader
2. **Generates** snappy headlines using OpenAI (if configured)
3. **Preserves** any manual title overrides
4. **Enforces** hero/column limits
5. **Updates** `articles.json`
6. **Commits** changes if any new articles are found

### Manual Management

#### Using the Web Editor

1. Open `admin/editor.html` in a web browser
2. View all articles with search and filtering options
3. Edit manual titles to override generated headlines
4. Designate articles as heroes or columns
5. Save changes and commit the updated `articles.json`

#### Manual Script Execution

```bash
# Set required environment variables
export INOREADER_APP_ID="your_app_id"
export INOREADER_API_KEY="your_api_key"
export OPENAI_API_KEY="your_openai_key"  # Optional

# Run the fetch script
python scripts/fetch_inoreader.py
```

### Content Categories

- **Heroes** (Max 3): Featured articles displayed prominently
- **Columns** (Max 6): Regular featured content  
- **Regular Articles**: All other fetched content

### Data Format

The `articles.json` file contains:

```json
{
  "articles": [
    {
      "id": "unique_article_id",
      "title": "Original Article Title",
      "manual_title": "Custom Override Title",
      "generated_headline": "AI-Generated Snappy Headline", 
      "url": "https://source.com/article",
      "content": "Article content...",
      "summary": "Brief summary...",
      "published_date": "2024-01-01T12:00:00Z",
      "fetched_date": "2024-01-01T12:30:00Z",
      "tags": ["medical", "research"],
      "source": "Medical Journal",
      "author": "Dr. Smith",
      "is_hero": false,
      "is_column": true
    }
  ],
  "heroes": ["article_id1", "article_id2"],
  "columns": ["article_id3", "article_id4"],
  "last_updated": "2024-01-01T12:30:00Z",
  "limits": {
    "max_heroes": 3,
    "max_columns": 6
  }
}
```

## Integration with medaffairs.tech

The `articles.json` file can be consumed by medaffairs.tech for:

- Display of featured hero articles
- Column content management
- Full article listings with proper titles
- Metadata for sorting and filtering

## Manual Workflow (Legacy)

The original manual workflow is still supported:

1. **Add articles**: Create Markdown files in `articles/`
2. **Add metadata**: Create JSON files in `metadata/`
3. **Manual management**: Edit files directly

## Troubleshooting

### Common Issues

1. **No articles fetched**: Check Inoreader API credentials and tag name
2. **OpenAI errors**: Verify API key and account credits
3. **Workflow failures**: Check Actions logs for detailed error messages
4. **Editor not loading**: Ensure `articles.json` exists in the root directory

### Debugging

- Check GitHub Actions logs for detailed execution information
- Run the fetch script locally with debug environment variables
- Use browser developer tools to debug the web editor

## Security Notes

- API keys are stored as GitHub secrets and not exposed in logs
- The web editor operates entirely client-side
- All commits are attributed to the GitHub Actions bot
- Manual commits require proper authentication

---

For technical support or feature requests, please open an issue or consult the documentation in the `admin/` directory.
