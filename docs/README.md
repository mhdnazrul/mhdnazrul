# 📚 mhdnazrul Profile Documentation

Welcome to the documentation hub for this automated GitHub Profile repository!

This directory contains everything you (or open-source contributors) need to understand, maintain, and extend the architecture of this repository without having to reverse-engineer the source code.

## 📑 Documentation Index

1. **[Repository Guide](REPOSITORY_GUIDE.md)**
   *Start here!* This guide explains the core architecture, the purpose of every folder (`.github/`, `scripts/`, `assets/`), and provides a visual Mermaid diagram of the cron-triggered automation flow.

2. **[Workflow Guide](WORKFLOW_GUIDE.md)**
   A deep dive into the GitHub Actions (`generate-assets.yml`, `update-readme.yml`, `health-check.yml`). Explains exactly when they run, what they do, the secrets they require (`WAKATIME_API_KEY`), and how they safely auto-commit changes to the `main` branch.

3. **[Maintenance Guide](MAINTENANCE.md)**
   Your day-to-day operations manual. Read this to learn how to add new projects to your profile, how to change your Competitive Programming handle, and how to safely test the Python scripts locally before pushing to production.

4. **[Troubleshooting Guide](TROUBLESHOOTING.md)**
   Hit a snag? This guide details common failures—like Cloudflare API blocks, missing WakaTime secrets, or failing Dependabot PRs—and provides immediate, actionable fixes.

---

### 💡 Quick Overview of the Architecture

- **The Logic:** Python scripts (e.g., `scripts/update_cp_stats.py`) fetch live data from external APIs.
- **The Engine:** GitHub Actions in `.github/workflows/` spin up on a schedule to run the Python scripts.
- **The Presentation:** The scripts use strict Regex (`scripts/readme_formatter.py`) to safely inject the fresh data into specific `<!-- START_SECTION -->` tags inside the root `README.md`.
- **The Security:** The entire pipeline operates under the Principle of Least Privilege, explicitly requesting only the permissions it needs, and strictly isolating assets into branches and directories.
