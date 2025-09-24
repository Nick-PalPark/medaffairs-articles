# Process Article Webhook Usage

This document describes how to use the `process-article.yml` GitHub Actions workflow to process articles from Zapier webhooks.

## Overview

The workflow processes individual articles sent via `repository_dispatch` events from Zapier and creates JSON files in the `_data/articles/` directory.

## Triggering the Workflow

### Repository Dispatch Event

Send a POST request to trigger the workflow:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/Nick-PalPark/medaffairs-articles/dispatches \
  -d '{
    "event_type": "new_article",
    "client_payload": {
      "title": "Your Article Title",
      "url": "https://example.com/article",
      "source": "Source Name",
      "published": "2024-01-15T10:30:00Z",
      "content": "Article content or summary...",
      "category": "tech"
    }
  }'
```

## Payload Format

### Required Fields

- `title` (string): The article title
- `url` (string): The article URL

### Optional Fields

- `source` (string): The source publication name (default: "Unknown")
- `published` (string): Publication date in ISO 8601 format (default: current timestamp)
- `content` (string): Article content or summary (default: empty string)
- `category` (string): Article category (default: "general")

### Example Payload

```json
{
  "event_type": "new_article",
  "client_payload": {
    "title": "Revolutionary AI Treatment Shows Promise in Clinical Trials",
    "url": "https://example.com/ai-treatment-breakthrough",
    "source": "Medical News Today",
    "published": "2024-01-15T10:30:00Z",
    "content": "A groundbreaking AI-powered treatment has shown remarkable results...",
    "category": "tech"
  }
}
```

## Generated Files

### File Location

Articles are stored as individual JSON files in `_data/articles/`

### File Naming

Files are named using the pattern: `YYYYMMDD_HHMMSS_Safe_Article_Title.json`

Example: `20240115_103000_Revolutionary_AI_Treatment_Shows_Promise.json`

### File Structure

```json
{
  "id": "20240115_103000_Revolutionary_AI_Treatment_Shows_Promise.json",
  "title": "Revolutionary AI Treatment Shows Promise in Clinical Trials",
  "url": "https://example.com/ai-treatment-breakthrough",
  "source": "Medical News Today",
  "published": "2024-01-15T10:30:00Z",
  "category": "tech",
  "content": "A groundbreaking AI-powered treatment has shown remarkable results...",
  "created_at": "2024-01-15T10:35:42Z",
  "processed_by": "zapier-webhook"
}
```

## Integration with Zapier

### Setup Steps

1. **Create a GitHub Personal Access Token**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate a token with `repo` scope
   - Copy the token for use in Zapier

2. **Configure Zapier Webhook**
   - In your Zapier workflow, add a "Webhooks by Zapier" action
   - Set the URL to: `https://api.github.com/repos/Nick-PalPark/medaffairs-articles/dispatches`
   - Set the method to `POST`
   - Add headers:
     - `Accept`: `application/vnd.github+json`
     - `Authorization`: `token YOUR_GITHUB_TOKEN`
   - Set the payload to map your article data to the expected format

3. **Test the Integration**
   - Run a test from Zapier
   - Check the GitHub Actions tab for workflow execution
   - Verify that a JSON file was created in `_data/articles/`

## Error Handling

### Common Issues

1. **Missing Required Fields**
   - Ensure `title` and `url` are always provided
   - The workflow will fail with a clear error message if these are missing

2. **Invalid JSON in Payload**
   - Verify that the JSON payload is properly formatted
   - Check for escaped quotes in content fields

3. **Authentication Issues**
   - Verify that the GitHub token has the correct permissions
   - Check that the token hasn't expired

### Monitoring

- Check the Actions tab in GitHub for workflow status
- Failed workflows will show detailed error messages
- Successful workflows will show a summary of the processed article

## Security Considerations

- Never commit GitHub tokens to the repository
- Use GitHub repository secrets for sensitive configuration
- The workflow validates input data to prevent malicious content
- File names are sanitized to prevent directory traversal attacks

## Workflow Permissions

The workflow requires:
- `contents: write` - To commit new JSON files to the repository
- Repository dispatch events must be enabled for the repository