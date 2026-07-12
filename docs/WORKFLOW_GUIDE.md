# Workflow Guide

This document explains the automation pipelines (GitHub Actions) that power the repository.

## ⚙️ The Workflows

### 1. `generate-assets.yml`
- **Schedule:** `00:00 UTC` (Daily)
- **Purpose:** Generates the "Contribution Grid Snake" animation.
- **How it works:** It uses the `Platane/snk@v3` action to read your GitHub contribution graph. It generates two SVGs (light mode and dark mode palette). To keep your `main` branch clean of massive SVG diffs, it uses `crazy-max/ghaction-github-pages@v4` to force-push the generated SVGs to an isolated `output` branch. The README pulls the images directly from that branch.

### 2. `update-readme.yml`
- **Schedule:** `00:30 UTC` (Daily)
- **Purpose:** The primary data pipeline for all text and statistics.
- **How it works:** 
  1. Checks out the code.
  2. Sets up Python 3.11.
  3. Executes `scripts/update_cp_stats.py` to fetch Codeforces data and inject it into the README.
  4. Runs `athul/waka-readme` to fetch WakaTime metrics and inject them.
  5. Runs `jamesgeorge007/github-activity-readme` to fetch your latest 5 commits/PRs and inject them.
  6. Uses `stefanzweifel/git-auto-commit-action` to detect any file changes and push a single `chore:` commit to the `main` branch.

### 3. `health-check.yml`
- **Schedule:** `00:00 UTC` (Every Sunday)
- **Purpose:** Ensures the repository remains production-ready and links don't die over time.
- **How it works:** Runs Markdown linting, CSpell (spell checker), Actionlint (YAML syntax checker), and Lychee (a deep link checker that pings every URL in the repository to ensure it doesn't return a 404). Generates a report in the Action Summary UI.

---

## 🔑 Required GitHub Secrets
For the workflows to function properly, the following secrets must be configured in **Settings > Secrets and variables > Actions**:

- `WAKATIME_API_KEY`: Required by `update-readme.yml`. You must generate this from your WakaTime account settings. If this is missing, the workflow uses `continue-on-error: true` to skip the step gracefully without crashing the whole pipeline.

*(Note: `GITHUB_TOKEN` is used heavily, but it is automatically provided by GitHub. We enforce security by manually setting `permissions: contents: write` strictly on the jobs that need to commit code).*
