# Repository Guide

Welcome to the definitive architectural guide for the `mhdnazrul/mhdnazrul` GitHub Profile repository.

This repository is not a static Markdown file; it is a fully automated, cron-triggered static site generator that continuously updates your developer dashboard without manual intervention.

## 🏗️ Core Architecture
The architecture is strictly separated into three layers to ensure scalability and zero-maintenance:
1. **Presentation Layer:** The `README.md` containing HTML tables and SVG layouts.
2. **Logic Layer:** Python scripts located in `scripts/` that fetch and format live data.
3. **Automation Layer:** GitHub Actions in `.github/workflows/` that execute the logic and commit the changes.

## 📂 Directory Structure & Purpose

### `.github/`
The brain of the automation.
- `workflows/`: Contains the CI/CD pipelines (`generate-assets.yml`, `update-readme.yml`, `health-check.yml`).
- `dependabot.yml`: Automatically checks for newer versions of the GitHub Actions used in the workflows.
- `ISSUE_TEMPLATE/` & `PULL_REQUEST_TEMPLATE.md`: Developer experience configurations for open-source contributors.

### `assets/`
The visual asset hub. Isolating these prevents the root directory from becoming cluttered.
- `images/`: Contains `banner-dark.svg` and `banner-light.svg`, which are natively swapped in the README using HTML `<picture>` tags based on the user's OS theme.
- `branding/`: Contains your `BRANDING_GUIDELINES.md`, ensuring future UI changes match your specific hex color palette.

### `scripts/`
The custom backend logic.
- `update_cp_stats.py`: Securely connects to the Codeforces API, fetches live rating/rank data, handles timeouts, and prepares the Markdown snippet.
- `readme_formatter.py`: A utility module using strict Regex (`re.DOTALL`). It safely opens `README.md`, targets specific `START_SECTION` and `END_SECTION` tags, and injects the new data without corrupting surrounding HTML tables.

### `docs/`
The knowledge base (where this file lives). Refer to the other guides for specific operations:
- [Workflow Guide](WORKFLOW_GUIDE.md) - For understanding the CI/CD pipelines.
- [Troubleshooting Guide](TROUBLESHOOTING.md) - For fixing failing actions.
- [Maintenance Guide](MAINTENANCE.md) - For updating profile data locally.
