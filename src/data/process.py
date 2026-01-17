"""Data process"""
import logging
import os
from typing import List

import pandas as pd
from langdetect import detect, LangDetectException
from pydantic import validate_call

from data.validation import validate_results


# @validate_call
def filter_after_agile_manifesto_date(
    df: pd.DataFrame, debug: bool = False
) -> pd.DataFrame:
    """
    Removes rows from the DataFrame where the Publication Year is before 2001.
    """
    logging.info("filter_after_agile_manifesto_date()")

    df = df.dropna(subset=["Publication Year"])

    if debug:
        logging.debug(
            "filter_after_agile_manifesto_date() - Dataframe: %s", df
        )

    try:
        df.loc[:, "Publication Year"] = df["Publication Year"].astype(int)
    except ValueError:
        print(
            "There are values in 'Publication Year' that cannot be converted to integers."  # noqa: E501 pylint: disable=C0301
        )

        return df

    return df[df["Publication Year"] >= 2001]


# @validate_call
def filter_venues(df: pd.DataFrame, exclude_venues_file: str) -> pd.DataFrame:
    """
    Filters out rows from a DataFrame based on a list of venues to exclude
    provided in a text file.
    """
    with open(exclude_venues_file, "r", encoding="utf-8") as file:
        exclude_venues = [line.strip() for line in file]

    filtered_df = df[~df['Venue'].isin(exclude_venues)]

    return filtered_df


@validate_call
def is_english(text: str) -> bool:
    """
    Return if the received text is English
    """
    # Check if the text is a string and not NaN
    if not isinstance(text, str) or pd.isna(text):
        return False

    # If the text is very short, it might be erroneously detected as
    # non-English. Adjust the threshold as needed.
    threshold_for_short_text = 3

    if len(text.split()) <= threshold_for_short_text:
        return True

    # TODO: Find a replacement for this very outdated package.
    try:
        return detect(text) == "en"
    except LangDetectException:
        return False


@validate_call
def process_and_save_result(
    result: List, knowledge_base_name: str, folder_name: str,
    debug: bool = False
) -> pd.DataFrame | None:
    """
    Transform data, add the source for each row and save to CSV.
    """
    logging.info("process_and_save_result()")

    filename = os.path.join(
        folder_name, knowledge_base_name.replace(" ", "_").lower() + ".csv"
    )

    df = pd.DataFrame(result)
    df["Source"] = knowledge_base_name

    if debug:
        logging.debug("process_and_save_result() - Filename: %s", filename)
        logging.debug("process_and_save_result() - Dataframe: %s", df)

    try:
        df.to_csv(filename, index=False)
    except FileNotFoundError as e:
        logging.error("process_and_save_result() - %s", e)
        return None

    return df


@validate_call
def process_and_save_results(
    ieee_results: List, folder_name: str = "output", debug: bool = False
) -> None:
    """
    Combines results to create CSVs with unique and repeated search results.
    """
    logging.info("process_and_save_results()")

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    ieee_df = process_and_save_result(
        result=ieee_results, knowledge_base_name="IEEE",
        folder_name=folder_name, debug=debug
    )

    # Combine the DataFrames
    all_results_df = pd.concat([ieee_df], ignore_index=True, sort=False)
    if debug:
        logging.debug("process_and_save_results() - All results dataframe: %s", all_results_df)  # noqa: E501 pylint: disable=C0301

    # Create the processed title
    all_results_df["ProcessedTitle"] = all_results_df["Title"].str.lower().str.replace(r'[!@#$%^&*()_+\-=[\]\{};:\'",.<>?/~`|\\]+', '', regex=True)  # noqa: E501 pylint: disable=C0301
    if debug:
        logging.debug("process_and_save_results() - All results with processed title: %s", all_results_df)  # noqa: E501 pylint: disable=C0301

    # Create the processed Venue
    all_results_df["ProcessedVenue"] = all_results_df["Venue"].str.lower().str.replace(r'[!@#$%^&*()_+\-=[\]\{};:\'",.<>?/~`|\\]+', '', regex=True)  # noqa: E501 pylint: disable=C0301
    if debug:
        logging.debug("process_and_save_results() - All results with processed venue: %s", all_results_df)  # noqa: E501 pylint: disable=C0301

    try:
        all_results_df.to_csv(os.path.join(
            folder_name, "all_results.csv"), index=False
        )
    except FileNotFoundError as e:
        logging.error("process_and_save_results() - %s", e)

    # Group by ProcessedTitle and aggregate the sources
    source_agg = all_results_df.groupby("ProcessedTitle")["Source"].apply(lambda x: ', '.join(x)).reset_index()  # noqa: E501 pylint: disable=C0301

    # Merge this aggregated source with the original dataframe
    all_results_df = all_results_df.drop("Source", axis=1).merge(source_agg, on="ProcessedTitle", how="left")  # noqa: E501 pylint: disable=C0301
    if debug:
        logging.debug("process_and_save_results() - All results with aggregated sources: %s", all_results_df)  # noqa: E501 pylint: disable=C0301

    unique_results_df = all_results_df.drop_duplicates(
        subset="ProcessedTitle", keep="first"
    )
    if debug:
        logging.debug("process_and_save_results() - Unique sources: %s", unique_results_df)  # noqa: E501 pylint: disable=C0301

    # TODO: This cannot run by default, and must be moved into an option or
    # something else
    unique_results_df = filter_after_agile_manifesto_date(unique_results_df)
    if debug:
        logging.debug("process_and_save_results() - Filtered Agile Manifesto: %s", unique_results_df)  # noqa: E501 pylint: disable=C0301

    # TODO: This cannot run by default, and must be moved into an option or
    # something else
    unique_results_df = remove_non_english_rows(unique_results_df, "ProcessedTitle", "ProcessedVenue")  # noqa: E501 pylint: disable=C0301
    if debug:
        logging.debug("process_and_save_results() - Filtered non-English: %s", unique_results_df)  # noqa: E501 pylint: disable=C0301

    current_dir = os.path.dirname(os.path.abspath(__file__))
    exclude_venues_txt = os.path.normpath(
        os.path.join(current_dir, "venues_to_exclude.txt")
    )
    if debug:
        logging.debug("process_and_save_results() - Venues to exclude file: %s", exclude_venues_txt)  # noqa: E501 pylint: disable=C0301

    unique_results_df = filter_venues(
        df=unique_results_df, exclude_venues_file=exclude_venues_txt
    )
    if debug:
        logging.debug("process_and_save_results() - Filtered venues: %s", unique_results_df)  # noqa: E501 pylint: disable=C0301

    # unique_results_df['Venue'] = unique_results_df['Venue'].str.lower().str.replace(r'[!@#$%^&*()_+\-=[\]\{};:\'",.<>?/~`|\\]+', '', regex=True)
    # data_to_pdf(unique_results_df, 'Venue')

    unique_results_df.to_csv(
        os.path.normpath(
            os.path.join(folder_name, "unique_results.csv")
        ), index=False
    )

    # Drop duplicates using the processed title
    duplicated_df = all_results_df[all_results_df.duplicated(subset="ProcessedTitle", keep=False)].drop_duplicates(subset='ProcessedTitle', keep='first')  # noqa: E501 pylint: disable=C0301
    if debug:
        logging.debug("process_and_save_results() - Dropped duplicated: %s", duplicated_df)  # noqa: E501 pylint: disable=C0301

    duplicated_df.to_csv(
        os.path.join(folder_name, "repeated.csv"), index=False
    )

    validate_results()


# @validate_call
def remove_non_english_rows(
    df: pd.DataFrame, col1, col2, folder_name: str = "output",
    debug: bool = False
) -> pd.DataFrame:
    """
    Remove the non-English rows from the dataframe
    """
    logging.info("remove_non_english_rows()")

    def row_is_non_english(row):
        logging.info("row_is_non_english()")

        return not (is_english(row[col1]) or is_english(row[col2]))

    non_english_rows = df[df.apply(row_is_non_english, axis=1)]

    if debug:
        logging.debug(
            "remove_non_english_rows() - Non-English rows: %s", non_english_rows  # noqa: E501
        )

    non_english_rows.to_csv(
        path_or_buf=f"{folder_name}/non_english.csv", index=False
    )

    return df[~df.apply(row_is_non_english, axis=1)]
