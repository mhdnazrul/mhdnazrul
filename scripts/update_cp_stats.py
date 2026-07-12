"""
Competitive Programming Stats Fetcher

This script fetches real-time competitive programming statistics 
from official APIs and injects them into the README.md.
"""

import os
import sys
import logging
import urllib.request
import json
from typing import Dict, Any, Optional

# Add the current directory to sys.path to import readme_formatter
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from readme_formatter import replace_in_readme

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurable variables (Fallback to defaults if not in ENV)
CF_HANDLE = os.getenv("CF_HANDLE", "nazrulislam_7")
README_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
SECTION_NAME = "cp_stats"
LAST_UPDATED_SECTION = "last_updated"

def fetch_codeforces_stats(handle: str) -> Optional[Dict[str, Any]]:
    """
    Fetches user statistics from the official Codeforces API.

    Args:
        handle (str): The Codeforces username handle.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing user stats or None if it fails.
    """
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    logger.info(f"Fetching Codeforces stats for handle: {handle}")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get("status") == "OK" and data.get("result"):
                return data["result"][0]
            else:
                logger.error(f"Codeforces API error: {data.get('comment')}")
                return None
    except Exception as e:
        logger.error(f"Failed to fetch Codeforces stats: {e}")
        return None

def generate_markdown(cf_stats: Dict[str, Any]) -> str:
    """
    Generates the markdown snippet for the competitive programming stats.

    Args:
        cf_stats (Dict[str, Any]): The Codeforces stats dictionary.

    Returns:
        str: The formatted markdown string.
    """
    if not cf_stats:
        logger.warning("No Codeforces data provided for markdown generation.")
        return "<p><i>Stats currently unavailable.</i></p>"

    rating = cf_stats.get("rating", "Unrated")
    max_rating = cf_stats.get("maxRating", "Unrated")
    rank = str(cf_stats.get("rank", "Unknown")).title()

    markdown = (
        f"<code><b>Codeforces Rating:</b> {rating} ({rank})</code><br>\n"
        f"<code><b>Max Rating:</b> {max_rating}</code>"
    )
    return markdown

def main() -> None:
    """Main execution function."""
    logger.info("Starting CP stats update job.")
    
    # 1. Fetch data from official APIs
    cf_stats = fetch_codeforces_stats(CF_HANDLE)
    
    # Note: CodeChef and HackerRank lack robust public open APIs. 
    # For a stable production script, we rely on Codeforces as the primary API metric.
    
    # 2. Generate Markdown
    if cf_stats:
        stats_md = generate_markdown(cf_stats)
        
        # 3. Inject into README
        logger.info("Injecting stats into README.md")
        success = replace_in_readme(README_PATH, SECTION_NAME, stats_md)
        
        if not success:
            logger.error("Failed to update README.md with CP stats")
            sys.exit(1)
    else:
        logger.warning("Failed to retrieve primary stats, skipping README update.")

    # 4. Inject Last Updated Timestamp
    from datetime import datetime, timezone
    now_utc = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
    last_updated_md = f"<i>Last updated: {now_utc}</i>"
    
    logger.info("Injecting Last Updated timestamp into README.md")
    if not replace_in_readme(README_PATH, LAST_UPDATED_SECTION, last_updated_md):
        logger.warning("Failed to update Last Updated timestamp")

if __name__ == "__main__":
    main()
