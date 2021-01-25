"""
Author                      : Drew Heasman
Date(last updated)          : 7 December 2020
Description : Fuzzy Match Strings and process data for matching and finding duplicates.
              Various functions to process data also included.
              
"""
### Import libraries ###
import numpy as np
from fuzzywuzzy import fuzz
import pandas as pd
import re
from nltk import pos_tag
import time
import uuid

###############################################################################################################
# Functions
# Raw Levenshtein ratio and distance calculator for demonstration processes.
def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ Function computes the minimum edit distance between to strings using Levenshteins algorithm.
        Implements dynamic programming.
        Can give a ratio calculation or print a string showing the number of edits needed.
        
        Parameters:
           s (string): string to compare
           t (string): string to compare
           ratio_calc (boolean): if true, returns a ratio instead of the number of edits.
        
        Raises:
                   
        Returns:
            Either a integer showing number of edits, or a ratio 
            (length of both strings - number of edits) / length of both strings
    """
    # Define the state space of the algorithm as a zero matrix.
    rows = len(s) + 1
    cols = len(t) + 1
    distance = np.zeros((rows,cols),dtype=int)  
    
    # Assign the index of each character of each string to the matrix.
    for i in range(1, rows):
        for k in range(1,cols):                  
            distance[i][0] = i
            distance[0][k] = k
    
    # Calculate the cost of deletion, insertion, or substitutions.
    for col in range(1,cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0                # Base case: Letters are the same, no change needed, cost is 0.
            else:
                if ratio_calc == True:  # In the case of a ratio calculation, a substitution is 
                    cost = 2            # considered both a deletion and insertion, therefore cost = 2.
                else:
                    cost = 1
            # Take the minimum of:
            distance[row][col] = min(distance[row-1][col] + 1,          # Deletion
                                     distance[row][col-1] + 1,          # Insertion
                                     distance[row-1][col-1] + cost)     # Substitution
    # if statement to return ratio or number of edits.
    if ratio_calc == True:
        ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return ratio
    else:
        print(distance)                # print the matrix showing the algorithm result.
        return distance[row][col]
    
# Find out if the author is similar using fuzzywuzzy partial ratio.
def similar_ref(a1, a2, sensitivity=85):
    """ Function returns the partial ratio of two strings if it exceeds a given sensitivity.
        
        Parameters:
           a1 (string): string to compare
           a2 (string): string to compare
           sensitivity (int): integer from 0 to 100 to determine cutoff
        
        Raises:
                   
        Returns:
            The partial ratio or 0.
    """
    p_ratio = fuzz.partial_ratio(a1, a2)
    if p_ratio > sensitivity:
        return p_ratio
    else:
        return 0    

# Find out if two strings are the same, returns True or False.
def same_ref(a1,a2):

    return a1 == a2

# Extract the publication year of a reference.
def extract_years(df, column):
    """ Function takes a dataframe and column with imbedded year information and inserts a new column
        'publication_years', with attempted extraction of the year from another named column.
        
        Parameters:
           df (dataframe): dataframe with the source column
           reference (str): name of the source column
                   
        Raises:
                   
        Returns:
           A dataframe with the column publication_year added.
    """
    df['publication_year'] = df[column].apply(lambda x: re.findall('(\d{4})', x)[0]).astype(int)
    return df

# Extract the author names. Not perfect.
def extract_authors(df, column):
    """ Function takes a dataframe and inserts a new column 'author_list', with attempted extraction
        of the authors from another named column. Does not always perform perfectly.
        
        Parameters:
           df (dataframe): dataframe with the source column
           reference (str): name of the source column
                   
        Raises:
                   
        Returns:
           A dataframe with the column author_list added.
    """
    df['author_list'] = df[column].apply\
                            (lambda x: [word for word,pos in pos_tag(x.replace(',', '').split())\
                                        if pos == 'NNP'])
    return df

# Finds the max partial ratio of each entry, and finds the index related to that entry.
def find_max_partial_ratio(df, column, sensitivity=85):
    """ Function takes a dataframe and inserts two new columns 'partial_ratio_max' and 'max_duplicate_index'.
        The first column compares each entry from a df column with each other, and tracks the partial_ratio
        values. The max is then added to the list, and the index of this max is added to the second column.
        
        Parameters:
           df (dataframe): dataframe with the source column
           reference (str): name of the source column
           sensitivity (int): integer from 0 to 100 to determine cutoff
                   
        Raises:
                   
        Returns:
           A dataframe with the columns partial_ratio_max and max_duplicate_index added.
    """
    list_to_match = df[column]               # create a list to iterate over.
    list_of_max = []                            
    list_of_max_indexed = []                    # instantiate our two lists to add to the df.
    for i in list_to_match:
        max_list = []                           # create a temp max_list
        for column in df[[column]]:
            columnSeriesObj = df[column]
            for ref in columnSeriesObj:
                if same_ref(i,ref) == False:    # If these two strings are False, it assumes a duplicate
                    max_list.append(similar_ref(i,ref,sensitivity))
        list_of_max.append(max(max_list))
        list_of_max_indexed.append(np.argmax(max_list))
    df['partial_ratio_max'] = list_of_max
    df['max_duplicate_index'] = list_of_max_indexed
    
    return df

def create_unique_id(df):
    """ Simple function to add a unique id to any dataframe.
        
        Parameters:
           df (dataframe): Dataframe
                   
        Raises:
                   
        Returns:
           A dataframe with a unique ID column added.
    """
    df['id'] = [uuid.uuid4() for _ in range(len(df.index))]
    return df

def drop_unique_entries(df):
    """ Simple function to add drops unique entries processed by find_max_partial ratio.
        
        Parameters:
           df (dataframe): Dataframe
                   
        Raises:
                   
        Returns:
           A dataframe with only possible duplicates showing (i.e. where max_partial_ratio is not 0).
    """
    df = df[df.partial_ratio_max != 0]
    return df
 


