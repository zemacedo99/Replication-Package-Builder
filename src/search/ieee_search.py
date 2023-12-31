import requests
try:
    from config import IEEE_API_KEY
except ImportError:
    raise ImportError("config.py not found. Please set up your API key as instructed in README.md")

def search_ieee(query, api_key, start_record=1, max_records=25):
    print("\nQuerying IEEE Xplore")

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
    
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def extract_ieee_information(data):
    extracted = []
    
    for item in data['articles']:
        title = item.get('title')
        publication_year = item.get('publication_year')
        publisher = item.get('publisher')
        venue_type = item.get('content_type')
        link = item.get('html_url')
        
        # Adjusting extraction based on the observed data structure
        authors_dict = item.get('authors', {})
        authors_list = authors_dict.get('authors', [])
        
        authors_names = [author.get('full_name', '') for author in authors_list if isinstance(author, dict)]
        
        extracted.append({
            'Title': title,
            'Publication Year': publication_year,
            'Venue': publisher,
            'Venue Type': venue_type,
            'Authors': ', '.join(authors_names),
            'Link': link
        })
        
    print(f"Fetched {len(extracted)} results from IEEE Xplore.")
    return extracted

if __name__ == "__main__":
    query = "Improving Documentation Agility in Safety-Critical Software Systems Development For Aerospace" 
        
    start_index = 0
    PAGE_SIZE = 25
    results = search_ieee(query, IEEE_API_KEY,  start_record=start_index + 1, max_records=PAGE_SIZE)

    print(results)