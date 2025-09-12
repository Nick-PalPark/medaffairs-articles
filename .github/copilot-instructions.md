# medaffairs-articles

A private content repository storing articles and metadata for use with [medaffairs.tech](https://github.com/Nick-PalPark/medaffairs.tech).

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

This is a content-only repository with no build system, dependencies, or automated processes. The primary tasks involve managing Markdown articles and their corresponding JSON metadata files.

### Repository Structure
- `articles/` — Contains Markdown articles, one per file
- `metadata/` — Contains JSON metadata files, one per article
- `README.md` — Project documentation
- `.github/` — GitHub configuration and this instructions file

### Essential Commands
- Validate JSON metadata files: `jq . metadata/filename.json`
- Validate all JSON files: `for file in metadata/*.json; do echo "Validating $file:"; jq . "$file" > /dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON"; done`
- List all articles: `ls -la articles/`
- List all metadata: `ls -la metadata/`

## Content Management Workflow

### Adding a New Article

1. **Create the Markdown article:**
   - Create a new file in `articles/` with a descriptive filename using kebab-case
   - Example: `articles/machine-learning-trends-2025.md`
   - Use standard Markdown formatting

2. **Create the corresponding JSON metadata:**
   - Create a matching JSON file in `metadata/` with the same base filename
   - Example: `metadata/machine-learning-trends-2025.json`
   - Use the exact metadata format specified below

3. **Required JSON Metadata Format:**
   ```json
   {
     "title": "Your Article Title",
     "author": "Author Name",
     "date": "YYYY-MM-DD",
     "tags": ["tag1", "tag2", "tag3"],
     "summary": "A brief summary of the article content."
   }
   ```

4. **Validate the metadata:**
   - Always run: `jq . metadata/your-filename.json` to validate JSON format
   - Ensure the JSON is properly formatted and contains all required fields

### File Naming Conventions
- Use kebab-case (lowercase with hyphens) for filenames
- Article and metadata files must have matching base names
- Examples:
  - `articles/covid-vaccine-efficacy.md` + `metadata/covid-vaccine-efficacy.json`
  - `articles/pharmaceutical-regulations.md` + `metadata/pharmaceutical-regulations.json`

### Validation Steps
Always perform these validation steps when working with content:

1. **Verify file structure:**
   ```bash
   ls articles/ && ls metadata/
   ```

2. **Validate all JSON metadata:**
   ```bash
   for file in metadata/*.json; do 
     echo "Validating $file:"
     jq . "$file" > /dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON"
   done
   ```

3. **Check file naming consistency:**
   - Ensure every `.md` file in `articles/` has a corresponding `.json` file in `metadata/`
   - Verify filenames match exactly (excluding extensions)

## Integration Notes

- This repository serves as a content source for the medaffairs.tech website
- Changes made here should be synced with the main website repository
- The metadata format is standardized for automated processing by the website

## Common Tasks

### Listing Content
```bash
# View all articles
ls -la articles/

# View all metadata
ls -la metadata/

# Count articles
ls articles/*.md | wc -l
```

### Content Validation
```bash
# Validate specific JSON file
jq . metadata/example-article.json

# Pretty-print JSON
jq . metadata/example-article.json

# Extract specific fields from metadata
jq '.title, .author, .date' metadata/example-article.json
```

### Repository Status
```bash
# Check git status
git status

# View recent changes
git log --oneline -5

# Check for uncommitted changes
git diff --name-only
```

## Important Notes

- **No Build System:** This repository has no package.json, build scripts, or CI/CD pipelines
- **Content Focus:** All work involves managing Markdown and JSON files
- **Validation Required:** Always validate JSON format using `jq` before committing
- **Naming Critical:** Maintain consistent kebab-case naming and ensure article/metadata file pairs match
- **Simple Workflow:** Create content → Validate format → Commit changes

## Troubleshooting

### JSON Validation Errors
If `jq` reports JSON errors:
1. Check for missing commas, quotes, or brackets
2. Ensure all strings are properly quoted
3. Verify array syntax for tags: `["tag1", "tag2"]`
4. Confirm date format: `"YYYY-MM-DD"`

### Missing File Pairs
If articles and metadata don't match:
1. List both directories: `ls articles/ && ls metadata/`
2. Ensure filenames match exactly (excluding extensions)
3. Create missing counterpart files as needed

### Git Issues
For any git-related problems:
1. Check status: `git status`
2. View recent history: `git log --oneline -5`
3. Use standard git workflows for this content repository