import sys
import os

# Ensure cwd is in sys.path so a config.py next to the executable can be imported
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from data.data_process import process_and_save_results
from search.acm_digital_library_search import extract_acm_digital_library_information, search_acm_digital_library
from search.scienceDirect_search import extract_science_direct_information, search_science_direct
from search.scopus_search import search_scopus, scopus_extract_information 
from search.ieee_search import search_ieee, extract_ieee_information
from search.inspec_search import search_engineering_village, engineering_village_extract_information
from search.hal_open_science_search import search_hal_open_science, extract_hal_open_science_information
from search.springer_nature_search import extract_springer_nature_information, search_springer_nature
from queries.query import ACM_DIGITAL_LIBRARY_QUERY, ENGINEERING_VILLAGE_QUERY, IEEE_QUERY, SCIENCE_DIRECT_QUERY, SCOPUS_QUERY, HAL_OPEN_SCIENCE_QUERY, SPRINGER_NATURE_QUERY
try:
    from config import ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, IEEE_API_KEY, SPRINGER_API_KEY
except ImportError:
    raise ImportError("config.py not found. Please set up your API key as instructed in README.md")

# Constants for data_flags keys
SCOPUS_KEY = 'scopus'
IEEE_KEY = 'ieee'
ENGINEERING_VILLAGE_KEY = 'engineering_village'
SCIENCE_DIRECT_KEY = 'science_direct'
HAL_OPEN_SCIENCE_KEY = 'hal_open_science'
ACM_DIGITAL_LIBRARY_KEY = 'acm_digital_library'
SPRINGER_NATURE_KEY = 'springer_nature'

def rep_package_start(data_flags, queries=None):
    if queries is None:
        queries = {
            'scopus': SCOPUS_QUERY,
            'ieee': IEEE_QUERY,
            'engineering_village': ENGINEERING_VILLAGE_QUERY,
            'science_direct': SCIENCE_DIRECT_QUERY,
            'hal_open_science': HAL_OPEN_SCIENCE_QUERY,
            'acm_digital_library': ACM_DIGITAL_LIBRARY_QUERY,
            'springer_nature': SPRINGER_NATURE_QUERY
        }
    # Initialize result lists for each database
    
    scopus_results = []
    ieee_results = []
    engineering_village_results = []
    science_direct_results = []
    hal_open_science_results = []
    acm_digital_library_results = []
    springer_nature_results = []

    # Initialize flag variables to control the loop by retrieving from data_flags
    scopus_more_data = data_flags.get(SCOPUS_KEY, False)
    ieee_more_data = data_flags.get(IEEE_KEY, True)
    engineering_village_more_data = data_flags.get(ENGINEERING_VILLAGE_KEY, False)
    science_direct_more_data = data_flags.get(SCIENCE_DIRECT_KEY, False)
    hal_open_science_more_data = data_flags.get(HAL_OPEN_SCIENCE_KEY, False)
    acm_digital_library_more_data = data_flags.get(ACM_DIGITAL_LIBRARY_KEY, False)
    springer_nature_more_data = data_flags.get(SPRINGER_NATURE_KEY, False)
    
    more_data = scopus_more_data or ieee_more_data or engineering_village_more_data or science_direct_more_data or hal_open_science_more_data or acm_digital_library_more_data or springer_nature_more_data
    
    start_index = 0
    PAGE_SIZE = 25

    while (more_data and start_index <= 300):
        print(f"\n\nFetching results starting from index {start_index}")

        # Scopus search
        if scopus_more_data:
            scopus_data = search_scopus(queries['scopus'], ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, start=start_index, count=PAGE_SIZE)
            if scopus_data:
                scopus_info = scopus_extract_information({"search-results": {"entry": scopus_data}})
                scopus_results.extend(scopus_info)
            else:
                print("No more results from Scopus.")
                scopus_more_data = False

        # IEEE Xplore search
        if ieee_more_data:
            ieee_data = search_ieee(queries['ieee'], IEEE_API_KEY, start_record=start_index + 1, max_records=PAGE_SIZE)  # IEEE uses 1-indexing
            if ieee_data and 'articles' in ieee_data and ieee_data['articles']:
                ieee_info = extract_ieee_information(ieee_data)
                ieee_results.extend(ieee_info)
            else:
                print("No more results from IEEE Xplore.")
                ieee_more_data = False

        # Engineering Village search
        if engineering_village_more_data:
            engineering_village_data = search_engineering_village(queries['engineering_village'], ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, start=start_index, count=PAGE_SIZE)
            if engineering_village_data and engineering_village_data['PAGE']['RESULTS-PER-PAGE'] != 0:
                engineering_village_info = engineering_village_extract_information(engineering_village_data)
                engineering_village_results.extend(engineering_village_info)
            else:
                print("No more results from Engineering Village.")
                engineering_village_more_data = False

        # Science Direct search
        if science_direct_more_data:
            science_direct_data = search_science_direct(queries['science_direct'], ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, start=start_index, count=PAGE_SIZE)
            if science_direct_data and start_index <= int(science_direct_data['search-results']['opensearch:totalResults']):
                science_direct_info = extract_science_direct_information(science_direct_data)
                science_direct_results.extend(science_direct_info)
            else:
                print("No more results from Science Direct.")
                science_direct_more_data = False

        # Hal Open Science search
        if hal_open_science_more_data:
            hal_open_science_data = search_hal_open_science(queries['hal_open_science'], start=start_index, count=PAGE_SIZE)
            if hal_open_science_data:
                hal_open_science_info = extract_hal_open_science_information(hal_open_science_data)
                hal_open_science_results.extend(hal_open_science_info)
            else:
                print("No more results from Hal Open Science.")
                hal_open_science_more_data = False

        # ACM Digital Library search
        if acm_digital_library_more_data:
            acm_digital_library_data = search_acm_digital_library(queries['acm_digital_library'], start=start_index, count=PAGE_SIZE)
            if acm_digital_library_data and acm_digital_library_data['message']['total-results'] > 0 and len(acm_digital_library_data['message']['items']) > 0:
                acm_digital_library_info = extract_acm_digital_library_information(acm_digital_library_data)
                acm_digital_library_results.extend(acm_digital_library_info)
            else:
                print("No more results from ACM Digital Library.")
                acm_digital_library_more_data = False
        
        # Springer Nature search
        if springer_nature_more_data:
            springer_nature_data = search_springer_nature(queries['springer_nature'], SPRINGER_API_KEY, start=start_index, count=PAGE_SIZE)
            if springer_nature_data['records']:
                springer_nature_info = extract_springer_nature_information(springer_nature_data)
                springer_nature_results.extend(springer_nature_info)
            else:
                print("No more results from Springer Nature.")
                springer_nature_more_data = False

        more_data = scopus_more_data or ieee_more_data or engineering_village_more_data or science_direct_more_data or hal_open_science_more_data or acm_digital_library_more_data or springer_nature_more_data
        start_index += PAGE_SIZE

    process_and_save_results(scopus_results, ieee_results, engineering_village_results, science_direct_results,hal_open_science_results,acm_digital_library_results,springer_nature_results)
    
    # Return the results for display
    return {
        'scopus': scopus_results,
        'ieee': ieee_results,
        'engineering_village': engineering_village_results,
        'science_direct': science_direct_results,
        'hal_open_science': hal_open_science_results,
        'acm_digital_library': acm_digital_library_results,
        'springer_nature': springer_nature_results
    }
