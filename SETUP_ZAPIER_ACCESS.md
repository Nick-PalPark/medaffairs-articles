# Setting Up GitHub Access to Zapier Table

This guide explains how to configure GitHub to access your Zapier table at `https://tables.zapier.com/app/tables/t/01K4QYZXV51PJBZ3P9FWQB5MRA` and automatically pull tagged articles into the medaffairs-articles repository.

## Prerequisites

1. Access to the Zapier table: `https://tables.zapier.com/app/tables/t/01K4QYZXV51PJBZ3P9FWQB5MRA`
2. Admin access to the GitHub repository `Nick-PalPark/medaffairs-articles`
3. Admin access to the GitHub repository `Nick-PalPark/medaffairs.tech` (for website updates)

## Step 1: Get Zapier API Credentials

### Option A: Using Zapier Tables API (Recommended)
1. Go to your Zapier account dashboard
2. Navigate to "Tables" or visit `https://tables.zapier.com/`
3. Find your table: `01K4QYZXV51PJBZ3P9FWQB5MRA`
4. Look for API settings or integration options
5. Generate an API key for programmatic access

### Option B: Using Zapier Webhooks/API (Alternative)
If direct table API isn't available:
1. Set up a Zapier webhook that exports table data
2. Use webhook URL as the API endpoint
3. Configure authentication token/key

## Step 2: Configure GitHub Repository Secrets

You need to set up the following secrets in your GitHub repository:

### Required Secrets:

1. **ZAPIER_TABLE_ID**
   - Value: `01K4QYZXV51PJBZ3P9FWQB5MRA`
   - Description: The ID of your Zapier table

2. **ZAPIER_API_KEY**
   - Value: `[Your API key from Step 1]`
   - Description: Authentication key for Zapier Tables API

3. **MEDAFFAIRS_TECH_PAT** (Optional but recommended)
   - Value: `[Personal Access Token]`
   - Description: GitHub PAT with repository dispatch permissions for medaffairs.tech
   - Required scopes: `repo`, `workflow`

### How to Add Secrets:

1. Go to your GitHub repository: `https://github.com/Nick-PalPark/medaffairs-articles`
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with the name and value specified above

## Step 3: Configure Tag Filtering (Optional)

If you want to filter articles by specific tags:

1. Edit `config_template.py` and update the `REQUIRED_TAGS` setting:
   ```python
   REQUIRED_TAGS = ["medaffairs", "healthcare", "medical"]  # Your desired tags
   ```

2. The workflow will automatically use this configuration through the GitHub Actions environment

## Step 4: Test the Integration

### Manual Test:
1. Go to **Actions** tab in your GitHub repository
2. Find the "Capture articles and update website" workflow
3. Click **Run workflow** to trigger it manually
4. Monitor the execution logs

### Expected Results:
- New markdown files appear in `articles/` directory
- `articles.json` gets updated with raw article data
- `data/articles.json` gets updated with website-formatted data
- Changes are automatically committed to the repository
- medaffairs.tech website gets notified to refresh content

## Step 5: Verify Automatic Scheduling

The workflow is configured to run daily at 08:00 UTC. You can:
- Check the **Actions** tab for scheduled runs
- Modify the schedule in `.github/workflows/update_data.yml` if needed
- Disable automatic runs by removing the `schedule` trigger

## Troubleshooting

### Common Issues:

1. **"Config file not found" error**
   - Ensure `ZAPIER_TABLE_ID` and `ZAPIER_API_KEY` secrets are set correctly
   - Check that the workflow creates `config.py` properly

2. **"All API endpoints failed" error**
   - Verify your API key is valid and has the correct permissions
   - Check if the Zapier table URL/ID is correct
   - Try accessing the API endpoint manually with curl/Postman

3. **No articles fetched**
   - Check if there are actually tagged articles in your Zapier table
   - Verify tag filtering configuration matches your table structure
   - Review the API response format and adjust extraction logic if needed

4. **Authentication errors**
   - Confirm API key format (Bearer token vs basic auth)
   - Check if additional headers are required
   - Verify API endpoint URL structure

### Debug Steps:

1. **Test API Access Manually:**
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        -H "Content-Type: application/json" \
        "https://tables.zapier.com/api/v1/tables/01K4QYZXV51PJBZ3P9FWQB5MRA/records?limit=5"
   ```

2. **Check Workflow Logs:**
   - Go to Actions tab and review failed workflow runs
   - Look for specific error messages in the "Run capture script" step

3. **Test Locally:**
   - Clone the repository
   - Create `config.py` with your credentials
   - Run `python capture_articles.py` to test the script

## API Endpoint Documentation

The script tries multiple endpoint patterns:
- `https://tables.zapier.com/api/v1/tables/{table_id}/records`
- `https://tables.zapier.com/api/v1/tables/{table_id}/rows`
- `https://api.zapier.com/v1/tables/{table_id}/records`

If none work, you may need to:
1. Check Zapier documentation for correct endpoint format
2. Update the endpoints in `capture_articles.py`
3. Adjust authentication method if needed

## Next Steps

Once configured:
1. Articles will be automatically fetched daily
2. Website will be updated with new content
3. You can manually trigger updates anytime via GitHub Actions
4. Monitor the workflow logs to ensure smooth operation

## Support

If you encounter issues:
1. Check the GitHub Actions logs for detailed error messages
2. Verify all secrets are correctly configured
3. Test API access manually using curl or Postman
4. Refer to Zapier Tables API documentation for authentication details