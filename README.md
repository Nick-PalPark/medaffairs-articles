# medaffairs.tech — Drudge-inspired front-end + private-data sync

This repo contains the static front-end for medaffairs.tech and a GitHub Actions workflow that syncs the private medaffairs-data/articles.json into this repo at publish-time.

Quick start / setup checklist
1. medaffairs-data repo:
   - Keep medaffairs-data private if you prefer (recommended by you).
   - Ensure medaffairs-data has the fetch workflow that updates articles.json and triggers medaffairs.tech by calling repository_dispatch with event_type `medaffairs-data-updated`. Example:
     - POST to https://api.github.com/repos/Nick-PalPark/medaffairs.tech/dispatches with body {"event_type":"medaffairs-data-updated"} using a token with repo:dispatch permissions.

2. Create a PAT for this repo to read medaffairs-data:
   - Create a Personal Access Token (classic) with `repo` scope (or finer-grained token with repo:contents access).
   - In medaffairs.tech repository settings -> Secrets -> Actions, create the secret `MEDAFFAIRS_DATA_TOKEN` with that PAT.

3. GitHub Actions:
   - The workflow `.github/workflows/sync_data.yml` will:
     - Run on `repository_dispatch` event named `medaffairs-data-updated` (or manually).
     - Check out medaffairs-data using the PAT and copy `articles.json` into `data/articles.json`.
     - Commit and push the updated file if it changed.
   - After the commit, GitHub Pages (if configured) will publish the updated site.

4. GitHub Pages:
   - Configure GitHub Pages to serve from the branch/folder you want (e.g., main branch / root or `docs/`).
   - If you serve from main root, the site is ready. If you serve from `docs/`, move the static files into `docs/` or adjust the workflow to place files there.
   - Add a `CNAME` file with `medaffairs.tech` if you haven't already and configure DNS as described in your repo settings (A records or CNAME depending on setup).

Notes about titles and editing
- The site will display:
  1) manual_title (if present)
  2) generated_title (AI snappy headline)
  3) original_title (feed title)
- Keep using the admin/editor approach we discussed earlier (or edit articles.json in medaffairs-data via the GitHub UI) to set `manual_title`. The medaffairs-data fetch workflow will preserve manual_title when it updates articles.json.

If you want, I can:
- Update the medaffairs.tech repo directly with these files (I can open a PR) so you can review and merge.
- Or I can walk you step-by-step through adding secrets and enabling the repository_dispatch trigger from medaffairs-data.

## Article Sync Workflow

### Automated Sync
The repository includes a GitHub Actions workflow (`sync-articles.yml`) that automatically syncs articles:
- **Schedule**: Runs twice daily at 08:00 UTC and 20:00 UTC
- **Process**: Fetches new articles from Inoreader → Generates articles.json → Triggers medaffairs.tech update

### Manual Sync
You can manually trigger article synchronization from the GitHub Actions tab:

1. Go to **Actions** → **Sync Articles with Rate Limiting**
2. Click **Run workflow**
3. Configure options:
   - **Sync Type**:
     - `full` (default): Complete sync - fetch articles AND generate JSON
     - `articles_only`: Only fetch new articles, skip JSON generation
     - `json_only`: Only regenerate JSON from existing articles
   - **Force Sync**: Override rate limiting (normally 1 manual run per 30 minutes)

### Rate Limiting
- Manual triggers are rate-limited to prevent excessive API usage
- Maximum 1 manual run per 30 minutes (unless force sync is enabled)
- Scheduled runs are never rate-limited
- Rate limiting only applies to manual `workflow_dispatch` events

### Usage Examples

#### Quick JSON Regeneration
If you've manually edited article markdown files and want to update the JSON:
1. Go to Actions → Sync Articles with Rate Limiting
2. Select "json_only" sync type
3. Run workflow

#### Emergency Sync Override
If you need to sync immediately despite rate limiting:
1. Go to Actions → Sync Articles with Rate Limiting
2. Check "Force Sync" option
3. Select desired sync type and run

#### Testing New Articles
To capture only new articles without regenerating JSON:
1. Go to Actions → Sync Articles with Rate Limiting
2. Select "articles_only" sync type
3. Run workflow

### Troubleshooting

#### Rate Limiting Issues
- **Error**: "Manual sync blocked by rate limiting"
- **Solution**: Wait 30 minutes between manual runs, or use "Force Sync" option
- **Note**: Scheduled runs are never rate-limited

#### Missing Articles
- **Check**: Inoreader API credentials in repository secrets
- **Verify**: INOREADER_APP_ID, INOREADER_APP_KEY, INOREADER_USERNAME, INOREADER_PASSWORD
- **Test**: Run with "articles_only" sync type to isolate capture issues

#### JSON Generation Failed
- **Check**: Articles directory contains valid markdown files
- **Verify**: Markdown files have proper title format (`# Title`)
- **Test**: Run with "json_only" sync type to isolate generation issues

#### Repository Dispatch Failed
- **Check**: MEDAFFAIRS_TECH_PAT secret is configured
- **Verify**: PAT has repository dispatch permissions for medaffairs.tech repo
- **Note**: This only affects triggering the public site update, not local sync

#### Workflow Logs
View detailed logs in the Actions tab:
1. Go to **Actions** → **Sync Articles with Rate Limiting**
2. Click on the specific run
3. Expand log groups for detailed information

DNS / Pages help
- If you'd like, tell me your DNS host and I'll give exact DNS records to point medaffairs.tech to GitHub Pages.

## Setup complete
