"""
Author                      : Drew Heasman
Date(last updated)          : 5 December 2020
Description : API tools. Uses Crossref and xDD.
"""
### Import libraries ###
import requests
import json
import pandas as pd


pd.options.display.max_columns = 2000
###############################################################################################################
# Functions
# prints jsons in more easily readable formats.
def jprint(obj):
    """ Prints an easier to read json.
        
        Parameters:
           obj (object): json file.
                  
        Raises:
                   
        Returns:
            None
    """
    text = json.dumps(obj, sort_keys=True, indent=2)
    print(text)

# Basic request from api. 
def request_api(url, params, headers):
    """ Requests a response from an API, given the url, paramaters, and headers.
        
        Parameters:
           url (str)     : URL of the API.
           params (dict) : Parameters of the API search.
           headers (dict): Headers for the search.
                  
        Raises:
            ValueError: Could not parse the JSON
        Returns:
            A json response.
    """
    try:
        response = requests.get(url, params=params, headers=headers)
    except ValueError:
        print("Could not parse the JSON.")
    return response.json()

def get_df_xDD_articles(data):
    """ Accepts a response from an API call from xDD articles. Returns a flat and tidy pandas dataframe.
        
        Parameters:
           data: A json response from API
                  
        Raises:
            
        Returns:
            A flat and tidy dataframe with article metadata.
    """
    df = pd.json_normalize(data)
    df = df['success.data']
    dic = df[0]
    df = pd.DataFrame.from_dict(dic)
    df['link_url'] = df.link.apply(lambda row: row[0]['url'] if type(row) != float else row)
    df['link_type'] = df.link.apply(lambda row: row[0]['type'] if type(row) != float else row)
    df['identifier_type'] = df.identifier.apply(lambda row: row[0]['type'] if type(row) != float else row)
    df['identifier_id'] = df.identifier.apply(lambda row: row[0]['id'] if type(row) != float else row)
    df['authors'] = df.author.apply(lambda row: ';'.join(d['name'] for d in row))
    df = df.drop(columns=['author','link', 'identifier'])
    df['year'] = pd.to_numeric(df['year'])
    return df

def transform_pipeline_to_DDB(df, search_term):
    df['search_tag'] = search_term
    return df



