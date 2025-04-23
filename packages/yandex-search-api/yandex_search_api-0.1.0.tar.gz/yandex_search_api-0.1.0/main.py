#!/usr/bin/env python3
"""
Yandex Search API Usage Example

This script demonstrates how to use the Yandex Search API client with:
1. Direct IAM token authentication
2. OAuth token authentication (automatic conversion to IAM token)

Environment variables needed:
- YANDEX_FOLDER_ID: Your Yandex Cloud folder ID
- YANDEX_IAM_TOKEN: Your IAM token (for direct auth)
- YANDEX_OAUTH_TOKEN: Your OAuth token (for OAuth flow)
"""

import logging

from src.yandex_search_api import YandexSearchAPIClient, YandexSearchAPIError
from src.yandex_search_api.client import SearchType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def search_and_display_results(client, query):
    """Perform search and display results"""
    try:
        logger.info(f"Searching for: '{query}'")

        # Perform search and wait for results (timeout after 5 minutes)
        links = client.get_links(
            query_text=query,
            search_type=SearchType.RUSSIAN,
            max_wait=300,
            interval=10,
        )


        logger.info(f"{links}")

        return True

    except YandexSearchAPIError as e:
        logger.error(f"Search failed: {str(e)}")
        return False


def main():
    """Main execution function"""
    # Get credentials from environment variables
    folder_id = "b1gh198vm9k97rpvsl27"
    iam_token = None
    oauth_token = "y0__xCdssJXGMHdEyCwwvnbEqbqDqcjXUoukwbk_iRiXb0x_BLC"

    if not folder_id:
        logger.error("YANDEX_FOLDER_ID environment variable not set")
        return

    # Example 1: Using direct IAM token
    if iam_token:
        logger.info("\n=== Example 1: Using direct IAM token ===")
        try:
            client = YandexSearchAPIClient(
                folder_id=folder_id,
                iam_token=iam_token
            )
            search_and_display_results(client, "Василий исаев python")
        except Exception as e:
            logger.error(f"IAM token auth failed: {str(e)}")
    else:
        logger.warning("YANDEX_IAM_TOKEN not set, skipping direct IAM example")

    # Example 2: Using OAuth token
    if oauth_token:
        logger.info("\n=== Example 2: Using OAuth token ===")
        try:
            client = YandexSearchAPIClient(
                folder_id=folder_id,
                oauth_token=oauth_token
            )
            search_and_display_results(client, "Василий исаев python")
        except Exception as e:
            raise e
    else:
        logger.warning("YANDEX_OAUTH_TOKEN not set, skipping OAuth example")


if __name__ == '__main__':
    main()