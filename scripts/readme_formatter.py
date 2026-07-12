"""
README Formatter Utility

This module provides utility functions to manipulate and format the README.md file.
It is primarily used to inject dynamic content between specific section markers.
"""

import os
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def replace_in_readme(file_path: str, section_name: str, new_content: str) -> bool:
    """
    Replaces the content between <!-- START_SECTION:<section_name> --> 
    and <!-- END_SECTION:<section_name> --> in the given markdown file.

    Args:
        file_path (str): Path to the markdown file.
        section_name (str): The name of the section to replace.
        new_content (str): The content to inject.

    Returns:
        bool: True if replacement was successful, False otherwise.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    start_marker = f"<!-- START_SECTION:{section_name} -->"
    end_marker = f"<!-- END_SECTION:{section_name} -->"
    
    # Regex to find everything between the markers
    pattern = re.compile(
        rf"({re.escape(start_marker)}).*(?={re.escape(end_marker)})", 
        re.DOTALL
    )

    if not pattern.search(content):
        logger.warning(f"Section '{section_name}' not found in {file_path}")
        return False

    # Inject the new content with a newline
    replacement = f"\\1\n{new_content}\n"
    new_file_content = pattern.sub(replacement, content)

    if content == new_file_content:
        logger.info(f"No changes made to section '{section_name}'.")
        return True

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_file_content)
    
    logger.info(f"Successfully updated section '{section_name}' in {file_path}")
    return True

if __name__ == "__main__":
    logger.info("README Formatter module loaded.")
