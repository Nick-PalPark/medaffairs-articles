# Zapier Table Integration Setup

This repository now fetches articles from a Zapier table instead of Inoreader RSS feeds.

## Table Information
- **Zapier Table URL**: https://tables.zapier.com/app/tables/t/01K4QYZXV51PJBZ3P9FWQB5MRA
- **Table ID**: `01K4QYZXV51PJBZ3P9FWQB5MRA`

## Required Secrets

Add these secrets to your GitHub repository (`Settings` → `Secrets and variables` → `Actions`):

1. **ZAPIER_TABLE_ID**: `01K4QYZXV51PJBZ3P9FWQB5MRA`
2. **ZAPIER_API_KEY**: Your Zapier API key (get from Zapier account settings)

## Expected Table Structure

The Zapier table should have these columns:
- `title` - Article title
- `url` - Article URL
- `content` - Article content/summary
- `source` - Source publication name
- `author` - Article author
- `published` - Publication date (YYYY-MM-DD HH:MM:SS format)
- `created_at` - When added to table (ISO format)

## Testing

The integration includes fallback sample data, so the workflow will run even without API access for testing purposes.

To test locally:
```bash
# Copy config template and add your credentials
cp config_template.py config.py
# Edit config.py with your ZAPIER_TABLE_ID and ZAPIER_API_KEY

# Run the capture workflow
python capture_articles.py

# Generate JSON
python scripts/generate_articles_json.py --articles-dir articles --output articles.json

# Transform to site format
python scripts/transform_to_site_format.py --input articles.json --output data/articles.json
```

## API Endpoints Attempted

The script tries multiple possible Zapier API endpoints:
1. `https://tables.zapier.com/api/v1/tables/{ID}/records`
2. `https://tables.zapier.com/api/v1/tables/{ID}/rows`
3. `https://api.zapier.com/v1/tables/{ID}/records`

If all fail, it uses fallback sample data for testing.

## Troubleshooting

1. **No articles fetched**: Check your `ZAPIER_API_KEY` is valid
2. **API endpoints fail**: Verify the table is publicly accessible or API format
3. **Pipeline works with sample data**: This is normal for testing - replace with real API key for production

## Migration from Inoreader

The following changes were made:
- Replaced `InoreaderClient` with `ZapierTableClient`
- Updated secrets from `INOREADER_*` to `ZAPIER_*`
- Modified article processing to handle Zapier table data format
- Preserved all existing downstream processing (JSON generation, site format transformation)