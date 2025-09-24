# Articles Data Directory

This directory contains the articles database file that is updated by the webhook processing workflow.

## Structure

- `articles.json` - Main articles database file containing all processed articles

## Data Format

The `articles.json` file follows this structure:

```json
{
  "articles": [
    {
      "id": "unique_record_id",
      "article_title": "Original article title",
      "snappy_title": "AI-generated snappy title",
      "feed_title": "Source feed title",
      "article_url": "https://example.com/article",
      "cover_image": "https://example.com/image.jpg",
      "article_content": "Article content/summary",
      "ai_category": "tech|industry|opinion",
      "article_date": "2024-01-15T10:30:00Z",
      "published_timestamp": 1705314600000,
      "tags": ["tag1", "tag2"],
      "table_record_id": "original_database_record_id",
      "created_at": "2024-01-15T10:30:00.000Z",
      "updated_at": "2024-01-15T10:30:00.000Z"
    }
  ],
  "last_updated": "2024-01-15T10:30:00.000Z"
}
```

## Webhook Processing

Articles are added/updated via the `process-article.yml` GitHub Actions workflow which accepts these fields from Zapier webhooks:

- `ai_category` - Article category (tech, industry, opinion)
- `article_content` - Article content/summary
- `article_date` - Publication date (ISO format)
- `article_title` - Original article title
- `article_url` - Article URL
- `cover_image` - Cover image URL
- `feed_title` - Source feed title
- `snappy_title` - AI-generated catchy title
- `table_record_id` - Database record ID
- `tags` - Comma-separated tags

The workflow will:
1. Create new articles or update existing ones based on `table_record_id` or `article_url`
2. Preserve `created_at` timestamps for existing articles
3. Update `last_updated` timestamp for the entire dataset
4. Commit changes back to the repository