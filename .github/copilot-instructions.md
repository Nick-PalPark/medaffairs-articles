# MedAffairs Articles Repository

This repository manages articles for the MedAffairs.tech website. It contains a static HTML website that displays medical and healthcare news articles organized into three categories: Industry News, Tech Insights, and Opinion & Analysis. The site features hero articles at the top and categorized article lists below.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Serve the Website
- Navigate to repository root: `cd /home/runner/work/medaffairs-articles/medaffairs-articles`
- Start local server: `python3 -m http.server 8000` -- Takes <5 seconds to start. NEVER CANCEL.
- Access site at: `http://localhost:8000`
- Stop server: `Ctrl+C` or `killall python3`

### Alternative Serving Methods
- Any HTTP server works: `npx serve .`, `php -S localhost:8000`, Node.js `http-server`
- File:// URLs do NOT work due to CORS restrictions with JSON loading

## Validation

### ALWAYS Test Complete User Scenarios
After making any changes, ALWAYS validate by:
1. `python3 -m http.server 8000` -- Set timeout to 30+ seconds
2. Navigate to `http://localhost:8000` in browser or Playwright
3. Verify all three sections load articles (not "Error loading..." messages)
4. Check hero articles display with images and titles
5. Verify "Last updated" timestamp appears
6. Test clicking article links (they should open)
7. Stop the server when done

### Manual Validation Requirements
- ALWAYS serve the site and visually inspect it after changes
- Check browser console for JavaScript errors
- Verify JSON loads correctly: `curl http://localhost:8000/data/articles.json`
- Test responsive design on mobile viewport if CSS changes made

## Data Format Requirements

### Critical: data/articles.json Structure
The JavaScript expects this EXACT structure:
```json
{
  "last_updated": 1758756847676,
  "heroes": [
    {
      "manual_title": null,
      "generated_title": null,
      "original_title": "Article Title",
      "url": "https://example.com/article",
      "image": "https://example.com/image.jpg",
      "source": "Source Name",
      "published_at": 1758754545000
    }
  ],
  "columns": {
    "news": [
      {
        "manual_title": null,
        "generated_title": null,
        "original_title": "Industry News Article",
        "url": "https://example.com/news-article",
        "source": "Source Name",
        "published_at": 1758754545000
      }
    ],
    "tech": [
      {
        "manual_title": null,
        "generated_title": null,
        "original_title": "Tech Article Title",
        "url": "https://example.com/tech-article",
        "source": "Source Name",
        "published_at": 1758754545000
      }
    ],
    "opinion": [
      {
        "manual_title": null,
        "generated_title": null,
        "original_title": "Opinion Article Title",
        "url": "https://example.com/opinion-article",
        "source": "Source Name",
        "published_at": 1758754545000
      }
    ]
  }
}
```

### Common Data Issues
- If you see "Error loading..." messages, the JSON structure is wrong
- Missing `heroes`, `columns.news`, `columns.tech`, or `columns.opinion` arrays causes errors
- `last_updated` field is optional but recommended
- `image` is optional for heroes but recommended for visual appeal
- Title priority: `manual_title` > `generated_title` > `original_title`

## File Structure and Navigation

### Repository Root Contents
```
.
├── index.html          # Main HTML file with embedded JavaScript
├── static/
│   ├── css/style.css   # All styling (responsive design included)
│   └── js/site.js      # JavaScript that loads data/articles.json
├── articles/           # Raw markdown files (*.md)
├── articles.json       # Raw articles data (array format)
├── data/
│   └── articles.json   # Website format data (structured for site)
├── scripts/
│   ├── generate_articles_json.py      # Converts markdown to raw JSON
│   └── transform_to_site_format.py    # Converts raw JSON to website format
└── .github/
    └── copilot-instructions.md # This file
```

### Key Code Locations
- **Article loading logic**: Lines 78-88 in `static/js/site.js`
- **Hero section**: Lines 58-66 in `static/js/site.js` 
- **Category sections**: Lines 68-76 in `static/js/site.js`
- **Responsive CSS**: `static/css/style.css`
- **Error handling**: Lines 85-87 in `static/js/site.js`

### Data Processing Pipeline
1. **Markdown files** in `articles/` directory
2. **Raw JSON generation**: `scripts/generate_articles_json.py` → `articles.json`
3. **Website format**: `scripts/transform_to_site_format.py` → `data/articles.json`
4. **Website display**: `static/js/site.js` loads `data/articles.json`

## Common Tasks

### Updating Article Data
1. Add new markdown files to `articles/` directory, or edit existing ones
2. Regenerate raw JSON: `python3 scripts/generate_articles_json.py --articles-dir articles --output articles.json`
3. Transform to website format: `python3 scripts/transform_to_site_format.py --input articles.json --output data/articles.json`
4. ALWAYS test by serving site: `python3 -m http.server 8000`
5. Verify articles display correctly at `http://localhost:8000`

### Manual Title Editing
- Edit `articles.json` directly to add `manual_title` values
- Manual titles take precedence over auto-generated titles
- Run transformation script to update website format: `python3 scripts/transform_to_site_format.py --input articles.json --output data/articles.json`

### Styling Changes  
1. Edit `static/css/style.css`
2. ALWAYS test responsive design: resize browser or use mobile viewport
3. Test hero section, column layout, and footer
4. Verify changes work on both desktop and mobile

### HTML Structure Changes
1. Edit `index.html`  
2. Be careful with JavaScript section in `static/js/site.js`
3. Maintain existing element classes and IDs for CSS compatibility
4. ALWAYS validate by serving the site

### Troubleshooting Common Issues
- **"Error loading..." messages**: Check JSON structure matches expected format
- **Images not loading**: Verify `image` URLs are accessible in heroes data
- **Links not working**: Check `url` fields in JSON are valid
- **Site not accessible**: Ensure HTTP server is running, not using file:// URLs
- **JavaScript errors**: Check browser console, validate JSON syntax
- **Empty columns**: Run transformation script to categorize articles properly

## Build and Deployment

### No Build Process Required
- This is a static website with no build steps
- No dependencies, package managers, or compilation needed
- Deploy by copying files to any HTTP server
- No CI/CD pipeline currently exists

### Adding CI/CD (Optional)
If you want to add automated deployment:
1. Create `.github/workflows/deploy.yml`
2. Add JSON validation step: `python3 -c "import json; json.load(open('data/articles.json'))"`
3. Add HTML validation if needed
4. Deploy to GitHub Pages or any static hosting

## Performance Notes

### Timing Expectations
- HTTP server startup: <5 seconds
- Initial page load: <2 seconds  
- JSON fetch and render: <1 second
- Full validation cycle: <30 seconds total

### No Long-Running Operations
- No build processes that take minutes
- No test suites to run
- No database setup required
- All validation is near-instant

## Development Workflow

### Making Changes
1. Edit files directly (no build required)
2. Start HTTP server to test: `python3 -m http.server 8000`
3. Refresh browser to see changes
4. Validate complete user scenario
5. Stop server and commit changes

### Testing New Features
1. Always backup `articles.json` before major changes
2. Test with minimal data first, then full dataset
3. Verify error handling works (empty arrays, missing fields)
4. Test edge cases like very long article titles
5. Validate responsive design changes on mobile
6. Run the complete data pipeline: markdown → raw JSON → website format

Remember: This is a simple static website. Most operations complete in seconds, not minutes. Always validate changes by actually serving and viewing the site.