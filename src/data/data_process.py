import pandas as pd
import os

def filter_after_agile_manifesto_date(df):
    """
    Removes rows from the DataFrame where the Publication Year is before 2001.

    Parameters:
    - df (DataFrame): DataFrame containing article or paper details

    Returns:
    - DataFrame: Filtered DataFrame
    """

    # Drop rows where 'Publication Year' is NaN (if any)
    df = df.dropna(subset=['Publication Year'])

    # Ensure 'Publication Year' is of type int
    try:
        df.loc[:, 'Publication Year'] = df['Publication Year'].astype(int)
    except ValueError:
        print("There are values in 'Publication Year' that cannot be converted to integers.")
        return df  

    # Filter rows where Publication Year is 2001 or later
    return df[df['Publication Year'] >= 2001]

def process_and_save_result(result, data_base, folder_name):
    """
    Transforms data into a DataFrame, marks the source of each row, and saves to CSV.

    Parameters:
    - result (List): Raw data.
    - data_base (str): The name of the database/source.

    Returns:
    - DataFrame: Processed DataFrame.
    """
    
    df = pd.DataFrame(result)
    df['Source'] = data_base
    
    # Make filename safe (replace spaces with underscores, etc.) and create the full path
    filename = os.path.join(folder_name, data_base.replace(" ", "_").lower() + ".csv")
    
    df.to_csv(filename, index=False)
    return df


def process_and_save_results(scopus_results, ieee_results, engineering_village_results, science_direct_results, hal_open_science_results, acm_digital_library_results, folder_name="data_results"):
    """
    Combines data from Scopus, IEEE, and Engineering Village, creates two CSVs: 
    one for unique results and another for repeated results.
    
    Parameters:
    - scopus_results (List): Results from Scopus
    - ieee_results (List): Results from IEEE
    - engineering_village_results (List): Results from Engineering Village
    - science_direct_results (List): Results from Science Direct

    Returns:
    None
    """

    # Ensure the folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    scopus_df = process_and_save_result(scopus_results, "Scopus",folder_name)
    ieee_df = process_and_save_result(ieee_results, "IEEE",folder_name)
    engineering_village_df = process_and_save_result(engineering_village_results, "Engineering Village",folder_name)
    science_direct_df = process_and_save_result(science_direct_results, "Science Direct",folder_name)
    hal_open_science_results_df = process_and_save_result(hal_open_science_results, "Hal Open Science",folder_name)
    acm_digital_library_results_df = process_and_save_result(acm_digital_library_results, "ACM Digital Library",folder_name)

    # Combine the DataFrames
    all_results_df = pd.concat([scopus_df, ieee_df, engineering_village_df,science_direct_df, hal_open_science_results_df,acm_digital_library_results_df], ignore_index=True, sort=False)

    # Create the processed title
    all_results_df['ProcessedTitle'] = all_results_df['Title'].str.lower().str.replace(r'[!@#$%^&*()_+\-=[\]\{};:\'",.<>?/~` |\\]+', '', regex=True)

    # Save all results to a CSV
    all_results_df.to_csv(os.path.join(folder_name,"all_results.csv"), index=False)

    # Group by Title and aggregate the sources
    source_agg = all_results_df.groupby('ProcessedTitle')['Source'].apply(lambda x: ', '.join(x)).reset_index()

    # Merge this aggregated source with the original dataframe
    all_results_df = all_results_df.drop('Source', axis=1).merge(source_agg, on='ProcessedTitle', how='left')

    # Drop duplicates from the all_results_df to only keep the first occurrence
    unique_results_df = all_results_df.drop_duplicates(subset='ProcessedTitle', keep='first')

    # Process unique_results_df using the filter_after_agile_manifesto_date function
    unique_results_df = filter_after_agile_manifesto_date(unique_results_df)

    # Save the unique results to CSV
    unique_results_df.to_csv(os.path.join(folder_name,"unique_results.csv"), index=False)

    # Drop duplicates using the processed title
    duplicated_df = all_results_df[all_results_df.duplicated(subset='ProcessedTitle', keep=False)].drop_duplicates(subset='ProcessedTitle', keep='first')

    # Save the duplicates to a CSV
    duplicated_df.to_csv(os.path.join(folder_name,"repeated.csv"), index=False)
