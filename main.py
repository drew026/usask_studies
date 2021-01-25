"""
Author                      : Drew Heasman
Date(last updated)          : 19 January 2021
Description : Main is used to test the functionality of various tools in sub-packages, as
              well as the development of future tools.  
              
"""

from api_tools import xDD_api as api
from gplates_tools import track_point
from fuzzy_tools import fuzzy as fz
import time
import sys
import pandas as pd
sys.path.append('C:\\USask Python')
from sqlalchemy import create_engine
from config import passwords as user

###############################################################################################################
''' API transform pipeline testing code'''
### Variables Block for api_tools ###
username = user.username
password = user.password
crossref = "https://api.crossref.org/works"
xDD = "https://geodeepdive.org/api/articles?"
params = {
#         'pubname': '',                 # Publication Name, exact match
#         'pubname_like': 'Computers',            # Publication Name, partial match
#         'publisher': '',               # Publisher
#         'recent': '',                  # Most recent articles
         'term': 'intrusion breccia',                    # Full text term search
#         'no_word_stemming': False,     # True = no word stemming to search term
#         'case_sensitive': False,       # require case sensitivity
#         'full_results': '',            # Overview of total number of matching articles
#         'docid': '',                   # Internal ID of the article
#         'doi': '',                     # Digital Object Identifier
#         'title': '',                   # Title, exact match
#         'title_like':'Geology',        # Title, partial match
#         'min_acquired': 1900,          # Restrict by time aquired.
#         'max_acquired': 2020,          # Restrict by time aquired.
#         'min_published': 1996,         # Restrict by time published.
#         'max_published': 1998,         # Restrict by time published.
#         'fields': 'title',                  # Fields to return, default all
#         'firstname': '',               # First name of author, case insensitive
#         'lastname': '',                # Last name of author, case insensitive
         'max':10000,                    # Max number of articles to return
#         'dataset': '',                 # Filter results by predefined sets
#         'known_terms': False,             # If true, include summary of known terms indexed in xDD
#         'dict': '',                    # Include known terms summary for specified dictionaries, comma seperated list of names
#         'dict_id': '',                 # Include known terms summary for specified dictionaries, comma seperated list of IDs
#         'known_entities': '',          # Include known entities extracted via external tools
          }
headers = {}
date = time.strftime("%Y-%m-%d__%H-%M-%S")    # Date in exact time to attach to output filename                
output_file = 'output/' + date + ' api_output.csv'
###############################################################################################################
#data = api.request_api(xDD,params,headers)
#df = api.get_df_xDD_articles(data)
#df = api.transform_pipeline_to_DDB(df, "intrusion breccias")
#
##engine = create_engine('postgresql://{username}:{password}@localhost:5432/xDD'.format(username, password))
##postgreSQLConnection = engine.connect()
##df.to_sql('article_metadata', postgreSQLConnection, if_exists='append', index=False)
#
#print(df.head())
#print(df.shape)
#
#df.to_csv(output_file)
###############################################################################################################
'''gplates_tools testing code'''
### Variables Block for gplates_tools ###
reconstruction_time = 200.00             # This is the input date for creating the feature point
filename = "Test"                        # Output filename for use
date = time.strftime("%Y%m%d-%H%M%S")    # Date in exact time to attach to output filename                
feature_file = r"C:\USask Python\Gplates Data\GDUs+Rotation\PlatePolygons2016Continental.shp"
rotation_file = r"C:\USask Python\Gplates Data\GDUs+Rotation\T_Rot_Model_PalaeoPlates_20200131be.rot"
latitude, longitude = -50, 50
###############################################################################################################
#present_day = track_point.getPresentDayPoint(feature_file, rotation_file, latitude, longitude, reconstruction_time)
#print(present_day)
###############################################################################################################
'''fuzzy_tools testing code'''
###############################################################################################################
### Variables Block ###
test_list = ['Abbott, G. (1997)',
             'Abbott, G. 1997 , Geology of the Upper Hart river area, eastern Ogilvie mountains, Yukon T()',
             'Abbott, S.A., Sweet, I.P., Plumb, K.A., Young, D. Cutovinos, A., and Ferenczi, P., 2000, ()',
             'Ahrendt et al(1983a)',
             'Ahrendt et al(1983b)',
             'Ames, D.E., van Breenmen, O. and Scoates, J.S. (2002)',
             'Ames, D.E., van Breenmen, O. and Scoates, J.S. (2002) 2',
             ]

reference = 'reference'
date = time.strftime("%Y%m%d-%H%M%S")    # Date in exact time to attach to output filename 
output_file = date + '_output.csv'
###############################################################################################################
print(fz.levenshtein_ratio_and_distance('Marialite', 'marcasite', ratio_calc = False))

df = pd.DataFrame(test_list, columns=[reference])
df = fz.create_unique_id(df)
df = fz.extract_years(df, reference)
df = fz.extract_authors(df, reference)
df = fz.find_max_partial_ratio(df, reference, 75)
poss_duplicates = fz.drop_unique_entries(df)

print(poss_duplicates)

df.to_csv(output_file)