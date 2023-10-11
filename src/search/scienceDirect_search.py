import requests

try:
    from config import ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN
except ImportError:
    raise ImportError("config.py not found. Please set up your API key as instructed in README.md")

def search_science_direct(query, api_key, inst_token, start=0, count=25):

    url = "https://api.elsevier.com/content/search/sciencedirect"
    
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key,
        "X-ELS-Insttoken" : inst_token
    }

    params = {
        "query": query,
        "start": start,
        "count": count,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def extract_science_direct_information(data):
    entries = data.get('search-results', {}).get('entry', [])
    extracted = []

    for entry in entries:
        title = entry.get('dc:title')
        author = entry.get('dc:creator')
        publication_year = entry.get('prism:coverDate', '').split('-')[0]  # Extract year from coverDate
        venue = entry.get('prism:publicationName')
        venue_type = None
        link = entry.get('prism:url')

        extracted.append({
            'Title': title,
            'Publication Year': publication_year,
            'Venue': venue,
            'Venue Type': venue_type,
            'Authors': author,
            'Link': link
        })

    return extracted

if __name__ == "__main__":
    query = "docops"
        
    results = search_science_direct(query, ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN)
    data = extract_science_direct_information(results)

    for item in data:
        print(item)
