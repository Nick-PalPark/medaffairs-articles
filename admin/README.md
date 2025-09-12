# MedAffairs Articles Admin Tools

This directory contains browser-based admin tools for managing articles fetched from Inoreader.

## Files

### editor.html
A web-based interface for viewing and editing articles. Features include:

- **Article Overview**: View all fetched articles with metadata
- **Manual Title Editing**: Override article titles with custom headlines
- **Category Management**: Designate articles as heroes or columns
- **Search & Filtering**: Find articles by content, source, or category
- **Limit Enforcement**: Respects hero/column limits set in configuration

### editor.js
JavaScript functionality for the web editor, providing:

- **Real-time Editing**: Live updates as you modify titles and categories
- **Data Validation**: Enforces limits and prevents conflicts
- **Export Functionality**: Download updated articles.json for commit
- **Keyboard Shortcuts**: Ctrl+S to save, Ctrl+F to search

### Usage

1. **Open the Editor**: Open `editor.html` in a modern web browser
2. **Load Data**: The editor automatically loads `../articles.json`
3. **Edit Articles**: 
   - Add manual titles to override generated headlines
   - Mark articles as heroes (featured content, max 3)
   - Mark articles as columns (regular content, max 6)
4. **Save Changes**: Click "Save Changes" or press Ctrl+S
5. **Commit Changes**: Download the updated `articles.json` and commit it to the repository

### Features

#### Search & Filtering
- **Search**: Type in the search box to find articles by title, content, or source
- **Filters**: Use filter buttons to show specific categories:
  - All Articles
  - Heroes Only
  - Columns Only
  - Articles with Manual Titles
  - Recent (last 7 days)

#### Manual Title Override
- Add custom headlines that will be used instead of the original title
- Original titles are preserved and shown as placeholders
- Manual titles are highlighted with a green border

#### Hero/Column Management
- **Heroes**: Featured articles displayed prominently (limit: 3)
- **Columns**: Regular featured content (limit: 6)
- Limits are enforced - you cannot exceed the configured maximum
- Articles cannot be both hero and column simultaneously

#### Data Export
Since this is a static web tool, changes are exported as a downloadable JSON file that must be manually committed to the repository. Future versions could integrate with Git APIs for automatic commits.

### Technical Notes

- **Browser Compatibility**: Requires a modern browser with ES6+ support
- **Local Development**: Must be served from the repository root for proper file access
- **Data Format**: Works with the articles.json structure created by `fetch_inoreader.py`
- **No Server Required**: Pure client-side JavaScript application

### Security Considerations

- This tool operates entirely in the browser
- No sensitive data is transmitted to external servers
- Manual commits ensure review of all changes before they go live