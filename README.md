# medaffairs-articles

This private repository stores articles and metadata for use with [medaffairs.tech](https://github.com/Nick-PalPark/medaffairs.tech).

## Structure

- `articles/` — Contains Markdown articles, one per file.
- `metadata/` — Contains JSON metadata files per article.
- `README.md` — This file.

## Example

- `articles/example-article.md` — Example Markdown article.
- `metadata/example-article.json` — Example metadata for the article.

## Usage

1. **Add a new article:**  
   - Create a new Markdown file in `articles/`, e.g. `your-article-title.md`.
   - Create a corresponding JSON metadata file in `metadata/`, e.g. `your-article-title.json`.

2. **Metadata format:**
   ```json
   {
     "title": "Your Article Title",
     "author": "Your Name",
     "date": "YYYY-MM-DD",
     "tags": ["tag1", "tag2"],
     "summary": "Short summary of the article."
   }
   ```

3. **Syncing with medaffairs.tech:**  
   You can use this repository to track and update articles and metadata before publishing or syncing with medaffairs.tech.

---

If you need automation, scripts, or integration help, ask Copilot for assistance!
