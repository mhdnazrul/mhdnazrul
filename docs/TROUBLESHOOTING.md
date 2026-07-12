# Troubleshooting Guide

This guide outlines common failures in the automated pipelines and how to quickly resolve them without needing to dive deep into the source code.

## 🩺 How to Debug a Failing Workflow
1. Navigate to the **Actions** tab on your GitHub repository.
2. Click on the workflow run marked with a red ❌.
3. Expand the specific step that failed to view the console logs.

---

## ❌ Common Failures & Solutions

### 1. WakaTime Step Fails
**Symptom:** The `Update WakaTime Stats` step fails, or the WakaTime section in the README says "No data".
**Cause:** The `WAKATIME_API_KEY` secret is either missing, expired, or invalid.
**Fix:**
1. Log into wakatime.com and navigate to Settings > Secret API Key.
2. Copy the key.
3. Go to GitHub Repo Settings > Secrets and variables > Actions.
4. Update the `WAKATIME_API_KEY` secret.
5. Manually trigger the `Update README` workflow.

### 2. Codeforces Stats Are Not Updating
**Symptom:** The GitHub Action completes successfully, but the Competitive Programming stats in the README haven't changed.
**Cause:** Cloudflare Protection. The Codeforces API occasionally blocks IPs originating from GitHub Actions data centers (returning a 403 Forbidden).
**Fix:** 
- *No action required.* The Python script (`update_cp_stats.py`) is designed with a `try/except` block and custom `User-Agent` headers. If it hits a Cloudflare block, it gracefully skips the README injection rather than crashing the workflow. It will automatically try again on the next cron schedule.

### 3. GitHub Activity Shows "No Activity"
**Symptom:** The Recent Activity section is blank.
**Cause:** You haven't made any public commits, issues, or PRs recently. The action only fetches recent public events.
**Fix:** Push a commit to a public repository.

### 4. Dependabot PRs are Failing the Health Check
**Symptom:** Dependabot opens a PR to update an Action, but the `health-check.yml` workflow fails on that PR.
**Cause:** The new version of the action might have introduced a syntax change, or your workflow YAML needs updating to support it.
**Fix:** Read the release notes linked in the Dependabot PR, update the workflow syntax accordingly, or simply close the PR if you prefer to stay on the pinned SHA.

### 5. Accidentally Deleted HTML Tags in README
**Symptom:** The layout is completely broken after manually editing the README.
**Cause:** You accidentally deleted the `<!-- START_SECTION:name -->` or `</td>` tags.
**Fix:** Look at your Git commit history and revert the change, or manually restore the hidden HTML comment tags. The Python scripts rely on exactly matching `<!-- START_SECTION:cp_stats -->` to know where to inject data.
