# Webhook-Based Article Processing

This repository now supports webhook-based article processing that maintains a single JSON file for all articles at `_data/articles.json`.

## Workflow Overview

The `process-article.yml` workflow provides two ways to add new articles:

1. **Webhook Trigger**: Via `repository_dispatch` event with type `new-article`
2. **Manual Trigger**: Via GitHub Actions UI with test data

## Article Data Structure

Each article must contain the following fields:

### Required Fields
- `title` (string): The article title
- `url` (string): The article URL (must be unique)

### Optional Fields
- `snappy_title` (string): A catchy/shortened version of the title (defaults to empty string)
- `author` (string): Article author (defaults to "Unknown")
- `date` (string): Publication date in ISO format (defaults to current timestamp)
- `category` (string): Article category (defaults to "general")
- `cover_image` (string): URL to cover image (defaults to empty string)

### Auto-Generated Fields
- `processed_at` (string): ISO timestamp when the article was processed by the workflow

## Usage Examples

### 1. Repository Dispatch (Webhook)

Send a POST request to trigger the workflow:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/Nick-PalPark/medaffairs-articles/dispatches \
  -d '{
    "event_type": "new-article",
    "client_payload": {
      "title": "Revolutionary AI Medical Diagnosis Tool",
      "snappy_title": "AI Diagnoses Disease in Seconds!",
      "url": "https://example.com/ai-medical-tool",
      "author": "Dr. Jane Smith",
      "date": "2024-01-15T10:30:00Z",
      "category": "technology",
      "cover_image": "https://example.com/images/ai-tool.jpg"
    }
  }'
```

### 2. Manual Workflow Dispatch

1. Go to the **Actions** tab in GitHub
2. Select **Process Article via Webhook**
3. Click **Run workflow**
4. Paste your article JSON in the **test_article** field:

```json
{
  "title": "New Cancer Treatment Shows Promise",
  "url": "https://example.com/cancer-treatment",
  "author": "Medical Research Team",
  "category": "research"
}
```

## Workflow Behavior

### Article Processing Logic

1. **Validation**: Checks for required fields (`title` and `url`)
2. **Duplicate Prevention**: Rejects articles with existing URLs
3. **Data Normalization**: Fills in default values for missing optional fields
4. **File Management**: 
   - Reads existing `_data/articles.json` if it exists
   - Adds new article to the beginning of the array (most recent first)
   - Writes updated array back to the file
5. **Git Operations**: Commits and pushes changes automatically

### Error Handling

The workflow will fail gracefully in these cases:
- Missing required fields (`title` or `url`)
- Duplicate URLs (article already exists)
- Invalid JSON format
- File system errors

### Success Conditions

The workflow succeeds when:
- All required fields are present
- The article URL is unique
- The article is successfully added to `_data/articles.json`
- Changes are committed and pushed to the repository

## Example Output Structure

After processing, `_data/articles.json` will contain an array of articles:

```json
[
  {
    "title": "Revolutionary AI Medical Diagnosis Tool",
    "snappy_title": "AI Diagnoses Disease in Seconds!",
    "url": "https://example.com/ai-medical-tool",
    "author": "Dr. Jane Smith",
    "date": "2024-01-15T10:30:00Z",
    "category": "technology",
    "cover_image": "https://example.com/images/ai-tool.jpg",
    "processed_at": "2025-09-24T14:42:10.272183+00:00"
  },
  {
    "title": "New Cancer Treatment Shows Promise",
    "snappy_title": "",
    "url": "https://example.com/cancer-treatment",
    "author": "Medical Research Team",
    "date": "2025-09-24T14:42:32.140460+00:00",
    "category": "research",
    "cover_image": "",
    "processed_at": "2025-09-24T14:42:32.140471+00:00"
  }
]
```

## Integration with Other Systems

This workflow is designed to work with:

1. **Content Management Systems**: That can trigger webhooks when new articles are published
2. **RSS/Feed Processors**: That can parse feeds and send article data via webhook
3. **Editorial Workflows**: That can approve articles and trigger publication via webhook
4. **Third-party APIs**: That can integrate with the GitHub repository dispatch API

## Monitoring and Debugging

### Workflow Logs

Check the **Actions** tab to monitor workflow runs:
- Green checkmark: Article processed successfully
- Red X: Processing failed (check logs for details)

### Common Issues

1. **"Missing required field"**: Ensure both `title` and `url` are provided
2. **"Article already exists"**: The URL is already in the articles.json file
3. **"Error parsing JSON"**: The JSON payload is malformed
4. **Permission errors**: Check that the workflow has `contents: write` permissions

### Testing

You can test the workflow manually using the GitHub Actions UI with sample data:

```json
{
  "title": "Test Article",
  "snappy_title": "Amazing Test!",
  "url": "https://example.com/test-unique-url",
  "author": "Test Author",
  "category": "test"
}
```

## Security Considerations

- The workflow requires `contents: write` permissions to update the repository
- Repository dispatch events require a GitHub token with appropriate permissions
- Consider restricting who can trigger manual workflow runs via repository settings
- Validate article URLs to prevent injection of malicious links

## Rate Limiting

The workflow processes one article at a time. For bulk operations, consider:
- Sending multiple webhook events with delays between them
- Creating a separate bulk processing workflow if needed
- Using GitHub's rate limiting guidelines for API calls