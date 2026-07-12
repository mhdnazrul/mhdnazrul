"""
Competitive Programming Stats Fetcher

This script fetches real-time competitive programming statistics 
from official APIs and injects them into the README.md.
"""

import os
import re
import json
import urllib.request
import logging
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurable variables (Fallback to defaults if not in ENV)
CF_HANDLE = os.getenv("CF_HANDLE", "nazrulislam_7")
AC_HANDLE = os.getenv("AC_HANDLE", "nazrulislam_7")
CC_HANDLE = os.getenv("CC_HANDLE", "nazrulislam_7")
README_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
LAST_UPDATED_SECTION = "last_updated"

@dataclass
class CPStats:
    username: str
    rank: str
    rating: str
    max_rating: str
    solved: str
    stars: str = "N/A"

def fetch_codeforces(handle: str) -> CPStats:
    """Fetches user statistics from the official Codeforces API."""
    stats = CPStats(username=handle, rank="N/A", rating="N/A", max_rating="N/A", solved="N/A")
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    
    try:
        # User-Agent header is required to prevent 403 Forbidden errors from basic scrapers
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get("status") == "OK" and data.get("result"):
                user = data["result"][0]
                stats.rank = str(user.get("rank", "Unrated")).title()
                stats.rating = str(user.get("rating", "N/A"))
                stats.max_rating = str(user.get("maxRating", "N/A"))
    except Exception as e:
        logger.warning(f"Codeforces fetch failed: {e}")
        
    return stats

def fetch_atcoder(handle: str) -> CPStats:
    """Scrapes stats from AtCoder user profile."""
    stats = CPStats(username=handle, rank="N/A", rating="N/A", max_rating="N/A", solved="N/A")
    url = f"https://atcoder.jp/users/{handle}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
            rating_match = re.search(r"<th class=\"no-break\">Rating</th><td><span class='user-.*?'>(.*?)</span>", html)
            if rating_match:
                stats.rating = rating_match.group(1)
                
            max_rating_match = re.search(r"<th class=\"no-break\">Highest Rating</th><td><span class='user-.*?'>(.*?)</span>", html)
            if max_rating_match:
                stats.max_rating = max_rating_match.group(1)
                
            rank_match = re.search(r"<th class=\"no-break\">Rank</th><td>(.*?)</td>", html)
            if rank_match:
                stats.rank = rank_match.group(1)
                
    except Exception as e:
        logger.warning(f"AtCoder fetch failed: {e}")
        
    return stats

def fetch_codechef(handle: str) -> CPStats:
    """Scrapes stats from CodeChef user profile."""
    stats = CPStats(username=handle, rank="N/A", rating="N/A", max_rating="N/A", solved="N/A")
    url = f"https://www.codechef.com/users/{handle}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
            rating_match = re.search(r'class="rating-number">(\d+)?</div>', html)
            if rating_match:
                stats.rating = rating_match.group(1)
                
            stars_match = re.search(r'class="rating">(\d)★</span>', html)
            if stars_match:
                stats.stars = f"{stars_match.group(1)}★"
                
            max_rating_match = re.search(r'Highest Rating (\d+)', html)
            if max_rating_match:
                stats.max_rating = max_rating_match.group(1)
                
    except Exception as e:
        logger.warning(f"CodeChef fetch failed: {e}")
        
    return stats

def update_readme(cf: CPStats, cc: CPStats, ac: CPStats) -> None:
    """Replaces placeholders in the README with live stats."""
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Codeforces Replacements
        content = re.sub(r'<!-- CF_USERNAME -->', cf.username, content)
        content = re.sub(r'<!-- CF_RANK -->', cf.rank, content)
        content = re.sub(r'<!-- CF_CURRENT_RATING -->', cf.rating, content)
        content = re.sub(r'<!-- CF_MAX_RATING -->', cf.max_rating, content)
        content = re.sub(r'<!-- CF_SOLVED -->', cf.solved, content)

        # CodeChef Replacements
        content = re.sub(r'<!-- CC_USERNAME -->', cc.username, content)
        content = re.sub(r'<!-- CC_STARS -->', cc.stars, content)
        content = re.sub(r'<!-- CC_MAX_RATING -->', cc.max_rating, content)
        content = re.sub(r'<!-- CC_SOLVED -->', cc.solved, content)

        # AtCoder Replacements
        content = re.sub(r'<!-- AC_USERNAME -->', ac.username, content)
        content = re.sub(r'<!-- AC_RANK -->', ac.rank, content)
        content = re.sub(r'<!-- AC_RATING -->', ac.rating, content)
        content = re.sub(r'<!-- AC_MAX_RATING -->', ac.max_rating, content)

        # Handle last_updated section
        now_utc = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
        last_updated_md = f"<i>Last updated: {now_utc}</i>"
        content = re.sub(
            r'(<!-- START_SECTION:last_updated -->\n).*?(\n\s*<!-- END_SECTION:last_updated -->)',
            rf'\g<1>  {last_updated_md}\g<2>',
            content,
            flags=re.DOTALL
        )

        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)
            
        logger.info("Successfully updated README.md with live stats.")
        
    except Exception as e:
        logger.error(f"Failed to update README.md: {e}")

def main() -> None:
    """Main execution function."""
    logger.info("Starting Competitive Programming data synchronization...")
    
    cf_stats = fetch_codeforces(CF_HANDLE)
    ac_stats = fetch_atcoder(AC_HANDLE)
    cc_stats = fetch_codechef(CC_HANDLE)
    
    update_readme(cf_stats, cc_stats, ac_stats)
    logger.info("Synchronization complete.")

if __name__ == "__main__":
    main()
