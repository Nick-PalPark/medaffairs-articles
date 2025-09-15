# MedAffairs.tech Website

MedAffairs.tech is a static HTML website that displays medical and healthcare news articles organized into three categories: Industry News, Tech Insights, and Products & Opinion. The site features hero articles at the top and categorized article lists below.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Serve the Website
- Navigate to repository root: `cd /home/runner/work/medaffairs.tech/medaffairs.tech`
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
- Verify JSON loads correctly: `curl http://localhost:8000/articles-updated.json`
- Test responsive design on mobile viewport if CSS changes made

## Data Format Requirements

### Critical: articles-updated.json Structure
The JavaScript expects this EXACT structure:
```json
{
  "last_updated": "2025-09-11T00:24:37.335021",
  "heroes": [
    {
      "title": "Article Title",
      "url": "https://example.com/article",
      "cover_image": "https://example.com/image.jpg"
    }
  ],
  "industry": [
    {
      "title": "Industry Article Title", 
      "url": "https://example.com/industry-article"
    }
  ],
  "tech": [
    {
      "title": "Tech Article Title",
      "url": "https://example.com/tech-article"  
    }
  ],
  "opinion": [
    {
      "title": "Opinion Article Title",
      "url": "https://example.com/opinion-article"
    }
  ]
}
```

### Common Data Issues
- If you see "Error loading..." messages, the JSON structure is wrong
- Missing `heroes`, `industry`, `tech`, or `opinion` arrays causes errors
- `last_updated` field is optional but recommended
- `cover_image` is optional for heroes but recommended for visual appeal

## File Structure and Navigation

### Repository Root Contents
```
.
├── index.html          # Main HTML file with embedded JavaScript
├── style.css          # All styling (responsive design included)
├── articles-updated.json # Article data (must match expected structure)
└── .github/
    └── copilot-instructions.md # This file
```

### Key Code Locations
- **Article loading logic**: Lines 52-97 in `index.html`
- **Hero section**: Lines 64-72 in `index.html` 
- **Category sections**: Lines 74-90 in `index.html`
- **Responsive CSS**: Lines 34-35 in `style.css`
- **Error handling**: Lines 92-97 in `index.html`

## Common Tasks

### Updating Article Data
1. Edit `articles-updated.json` with correct structure
2. Validate JSON syntax: `python3 -c "import json; json.load(open('articles-updated.json'))"`
3. ALWAYS test by serving site: `python3 -m http.server 8000`
4. Verify articles display correctly at `http://localhost:8000`

### Styling Changes  
1. Edit `style.css`
2. ALWAYS test responsive design: resize browser or use mobile viewport
3. Test hero section, column layout, and footer
4. Verify changes work on both desktop and mobile

### HTML Structure Changes
1. Edit `index.html`  
2. Be careful with JavaScript section (lines 50-99)
3. Maintain existing element classes and IDs for CSS compatibility
4. ALWAYS validate by serving the site

### Troubleshooting Common Issues
- **"Error loading..." messages**: Check JSON structure matches expected format
- **Images not loading**: Verify `cover_image` URLs are accessible
- **Links not working**: Check `url` fields in JSON are valid
- **Site not accessible**: Ensure HTTP server is running, not using file:// URLs
- **JavaScript errors**: Check browser console, validate JSON syntax

## Build and Deployment

### No Build Process Required
- This is a static website with no build steps
- No dependencies, package managers, or compilation needed
- Deploy by copying files to any HTTP server
- No CI/CD pipeline currently exists

### Adding CI/CD (Optional)
If you want to add automated deployment:
1. Create `.github/workflows/deploy.yml`
2. Add JSON validation step: `python3 -c "import json; json.load(open('articles-updated.json'))"`
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
1. Always backup `articles-updated.json` before major changes
2. Test with minimal data first, then full dataset
3. Verify error handling works (empty arrays, missing fields)
4. Test edge cases like very long article titles
5. Validate responsive design changes on mobile

Remember: This is a simple static website. Most operations complete in seconds, not minutes. Always validate changes by actually serving and viewing the site.