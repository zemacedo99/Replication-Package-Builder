"""Data process"""
import logging
import os
from typing import List

import pandas as pd
from pydantic import validate_call


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
        logging.debug("process_and_save_result() - File name: %s", filename)
        logging.debug("process_and_save_result() - Data frame: %s", df)

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
        logging.debug("process_and_save_results() - All results data frame: %s", all_results_df)  # noqa: E501 pylint: disable=C0301

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

    # TODO: WiP
    # # Process unique_results_df using the filter_after_agile_manifesto_date function
    # unique_results_df = filter_after_agile_manifesto_date(unique_results_df)

    # unique_results_df = remove_non_english_rows(unique_results_df, 'ProcessedTitle', 'ProcessedVenue')

    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # exclude_venues_txt = os.path.normpath(os.path.join(current_dir, 'venues_to_exclude.txt')) # Path to your text file with venues

    # unique_results_df = filter_venues(unique_results_df, exclude_venues_txt)

    # # unique_results_df['Venue'] = unique_results_df['Venue'].str.lower().str.replace(r'[!@#$%^&*()_+\-=[\]\{};:\'",.<>?/~`|\\]+', '', regex=True)
    # # data_to_pdf(unique_results_df, 'Venue')

    # # Save the unique results to CSV
    # unique_results_df.to_csv(os.path.normpath(os.path.join(folder_name,"unique_results.csv")), index=False)

    # # Drop duplicates using the processed title
    # duplicated_df = all_results_df[all_results_df.duplicated(subset='ProcessedTitle', keep=False)].drop_duplicates(subset='ProcessedTitle', keep='first')

    # # Save the duplicates to a CSV
    # duplicated_df.to_csv(os.path.join(folder_name,"repeated.csv"), index=False)

    # validate_results()
