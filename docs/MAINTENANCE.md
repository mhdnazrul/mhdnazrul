# Maintenance Guide

This document explains how to safely update personal information, configure the scripts, and test changes locally.

## ✏️ Updating Your Profile (README.md)

### Adding a New Project
To add a new project to the "Featured Projects & Expertise" section:
1. Open `README.md`.
2. Locate the `## 🚀 Featured Projects & Expertise` section.
3. Add a new bullet point under the `Key Expertise & Past Work:` list.
   *Example:* `- **NewApp:** A scalable iOS application built with Swift (Lead Developer).`
4. **Important:** Do NOT use dummy URLs like `[NewApp](#)`. The CI Health Check (Lychee) will flag it as a broken link. Only use real URLs.

### Changing Your Codeforces Handle
If you change your Codeforces username, you must update the Python script configuration:
1. Open `scripts/update_cp_stats.py`.
2. On line 24, locate: 
   `CF_HANDLE = os.getenv("CF_HANDLE", "nazrulislam_7")`
3. Change `"nazrulislam_7"` to your new handle.
4. Commit the change. The workflow will automatically pull data for the new handle tonight at 00:30 UTC.

---

## 💻 Local Development

If you want to modify the Python automation scripts or Regex logic, you should always test it locally before pushing to `main`.

### Prerequisites
- Python 3.10 or higher.
- Git.

### Testing Scripts Locally
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/mhdnazrul/mhdnazrul.git
   cd mhdnazrul
   ```
2. The scripts use zero external dependencies, so no `pip install` or virtual environment is required.
3. Run the CP stats script:
   ```bash
   python scripts/update_cp_stats.py
   ```
4. Look at the console output. You should see:
   `INFO - Fetching Codeforces stats for handle: nazrulislam_7`
   `INFO - Successfully updated README.md with new stats`
5. Open your local `README.md` file and verify that the stats were injected correctly without breaking the surrounding Markdown/HTML layout.
6. Once verified, commit and push your changes.

---

## 🔄 Forcing an Immediate Update

You do not have to wait for the midnight cron jobs to update your profile.

**To manually update Stats, WakaTime, and Activity:**
1. Go to the **Actions** tab on GitHub.
2. Click **Update README** on the left menu.
3. Click the **Run workflow** dropdown on the right side.
4. Click **Run workflow**.

**To manually regenerate the Snake Animation:**
1. Go to the **Actions** tab on GitHub.
2. Click **Generate Assets** on the left menu.
3. Click the **Run workflow** dropdown on the right side.
4. Click **Run workflow**.
