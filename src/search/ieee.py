"""IEEE knowledge base search"""
import logging
from typing import List

import requests
from requests import HTTPError
from pydantic import ValidationError, validate_call

# FIXME
# try:
#     from config import IEEE_API_KEY
# except ImportError:
#     raise ImportError("config.py not found. Please set up your API key as instructed in README.md")


@validate_call
def search(
    query: str, api_key: str, start_record: int = 1, max_records: int = 25,
    debug: bool = False
) -> str | None:
    """
    Process a search and return the results.
    """
    logging.info("search() - Query: %s", query)

    base_url = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
    headers = {
        "Accept": "application/json",
    }
    params = {
        "querytext": query,
        "apikey": api_key,
        "start_record": start_record,
        "max_records": max_records
    }

    try:
        response = requests.get(
            url=base_url, headers=headers, params=params, timeout=60
        )
    except HTTPError as e:
        logging.error("search() - %s", e)
        return None

    if response.status_code == 200:
        if debug:
            logging.debug("search() - Results: %s", response.json())

        return response.json()


@validate_call
def extract_results_information(results: dict, debug: bool = False) -> List:
    """
    Extract and return the information from the search results.
    """
    results_information = []

    for item in results["articles"]:
        title = item.get("title")
        publication_year = item.get("publication_year")
        publisher = item.get("publisher")
        venue_type = item.get("content_type")
        link = item.get("html_url")

        # Adjusting extraction based on the observed data structure
        authors_dict = item.get("authors", {})
        authors_list = authors_dict.get("authors", [])

        authors_names = [
            author.get("full_name", "") for author in authors_list if isinstance(author, dict)  # noqa: E501 pylint: disable=C0301
        ]

        results_information.append({
            "Title": title,
            "Publication Year": publication_year,
            "Venue": publisher,
            "Venue Type": venue_type,
            "Authors": ", ".join(authors_names),
            "Link": link
        })

    logging.info(
        "extract_results_information() - Fetched %s results",
        len(results_information)
    )

    if debug:
        logging.debug(
            "extract_results_information() - Results information: %s",
            results_information
        )

    return results_information
