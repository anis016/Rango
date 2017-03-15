import json
import urllib.parse
import urllib.request
import os

## Python anti-pattern rule : http://docs.quantifiedcode.com/python-anti-patterns/maintainability/
# using wildcard imports (from ... import *)
# Not using with to open files
# Returning more than one variable type from function call
# Using the global statement
# Using single letter to name your variables
# Dynamically creating variable/method/function names

def read_webhos_key():
    webhose_api_key = None
    API_DIR = os.path.dirname(os.path.abspath(__file__))
    API_FILE = os.path.join(API_DIR, 'search.key')
    print("API_FILE", API_FILE)
    try:
        with open(API_FILE, 'r') as f:
            webhose_api_key = f.readline().strip()
    except:
        raise IOError('search.key file not found')

    return webhose_api_key

def run_query(search_terms, size=10):
    webhose_api_key = read_webhos_key()
    if not webhose_api_key:
        raise KeyError('Webhose key not found')

    root_url = 'http://webhose.io/search'
    query_string = urllib.parse.quote(search_terms)
    search_url = '{root_url}?token={api_key}&format=json&q={query_string}&sort=relevancy&size={size}'.\
                                                                                    format( root_url = root_url,
                                                                                            api_key  = webhose_api_key,
                                                                                            query_string = query_string,
                                                                                            size = size )

    results = []
    try:
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)

        for post in json_response['posts']:
            results.append({'title': post['title'],
                            'link' : post['url'],
                            'summary': post['text'][:200]})
    except:
        print("Error when querying the webhose API")

    return results

if __name__ == '__main__':
    print("Testing the Webhose API")
    results = run_query("Bangladesh")
    print(results)