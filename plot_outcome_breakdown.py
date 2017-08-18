#!/usr/bin/env python
# encoding: utf-8


import pandas as pd
import numpy as np
import csv
import os.path
import matplotlib.pyplot as plt
import math
import seaborn as sns
from textwrap import wrap

DATA_FILE_DIR = "./data/"
STOREFILENAME = "./output/"


def import_csv_to_df(filename):
    """
    Imports a csv file into a Pandas dataframe
    :params: get an xls file and a sheetname from that file
    :return: a df
    """
    
    return pd.read_csv(filename)


def export_to_csv(df, location, filename):
    """
    Exports a df to a csv file
    :params: a df and a location in which to save it
    :return: nothing, saves a csv
    """

    return df.to_csv(location + filename + '.csv')

def get_data_and_merge(file1, file2):
    """
    Build dataframes from each of the outcome classes and
    merge them.
    :params: nothing
    :return: a dataframe built from csvs in a folder
    """
    
    dfs_imports = {}

    # Go through all the csvs in the dir, import them into
    # dfs and then add each one to a dict of dfs
    for file in os.listdir(DATA_FILE_DIR):
        if file.endswith('.csv'):
            # Create a nice name for each df
            df_name = file[:-4]
            dfs_imports[df_name] = import_csv_to_df(DATA_FILE_DIR + str(file))

#    frames = list(dfs_imports.keys())
#    df1 = import_csv_to_df(file1)
#    df2 = import_csv_to_df(file2)
#    frames = [df1, df2]
    
    # Merge all the dfs in the dict into a super-df
    df = pd.concat(dfs_imports.values())

    return df


def lower_case(df):
    """
    Make all string-holding fields lower case to
    make matching easier later in the program
    :params: a df
    :return: a df with all string fields lower-cased
    """

    for current_col in df.columns:
        try:
            df[current_col].str.lower()
        except:
            print('Could not convert \"' + current_col + '\" column to lower case')

    return df


def basic_stats(df):
    """
    Get some basic stats on the data
    :params: a df
    :return: Just text
    """

    print('The data frame contains ' + str(len(df)) + ' outcomes') 

    return


def find_strings(df):
    """
    Look for the number of times that particular words are
    present in the dataframe
    :params: a df
    :return: just text
    """

    # Want to cycle through different words to see how well they are
    # represented in the df
    find_strings = ['doi', 'digital object identifier']

    # Go through each word in the list and get some stats
    for search_string in find_strings:
        not_found_cols = []
        # Make up a regex from the search string
        # The \b is used to do only whole word searches
        find_regex = '\\b' + search_string + '\\b'
        # Go through each column
        for current_col in df.columns:
            # Using try/except because not all cols hold strings and doing
            # a str.contains on a float col causes a crash
            try:
                # Count how times the regex is found in the current column
                found = df[current_col].str.contains(find_regex).sum()
            except:
                # If the regex can't be found (e.g. the col holds floats rather than strings)
                # set the found to 0
                found = 0
            # Only output if 
            if found != 0:
                print(current_col + ' contains ' + str(found) + ' rows which mentions ' + search_string)
            else:
                not_found_cols.append(current_col)
        print('The search term ' + search_string + ' was not found in the following cols: ' + str(not_found_cols))
    return


def get_counts(df):
    """
    Go through each field in the dataframe, and summarise the number of
    times each entry is present
    :params: a df
    :return: a dict of dfs, each of which includes a summary of a specific
             field
    """

    dict_of_dfs = {}

    for field in df.columns:
        df_temp = pd.DataFrame(data = (df[field].value_counts(sort=True)))
        dict_of_dfs[field] = df_temp

    return dict_of_dfs


def plot_basic_seaborn(dict_of_dfs, redraw):
    """
    Create a basic plot for each question. Plots of more specific interest will
    be created in a separate function, because it's impossible to automate it.
    Uses Seaborn to try and make things prettier
    :params: a dict of dataframe, the imported plot details
    :return: A list of saved charts
    """
    
    """
    Potential columns that could be printed
           'Department', 'Description', 'Funding OrgName', 'FundingOrgId',
           'GTR Outcome URL', 'GTRProjectUrl', 'Impact', 'LeadRO Name', 'LeadROId',
           'Outcome Title', 'Outcome Type', 'PI First Name', 'PI Orcid iD',
           'PI Surname', 'PIId', 'Project Reference', 'ProjectCategory',
           'ProjectId', 'Provided to Others?', 'Software Developed?',
           'Software Open Source?', 'Type of Material', 'Url', 'Year Produced'
    """
    
    things_to_print = ['Funding OrgName', 'LeadRO Name',
           'Outcome Type', 'Type of Material', 'Year Produced']
    
    labels=[]
    
    for current in things_to_print:
        # Read the dfs one at the time
        df_temp = dict_of_dfs[current]
        # Title's from the lookup table
        title = current
        labels = df_temp.index
        
        # Some labels are floats, but they represent years, so they
        # don't plot right. Hence, convert these to integers
        if labels.dtype == float:
            labels = labels.astype(int)

        # Some of the labels are really long so I cut them up
        # Note the str() function that's needed because one of
        # the sets of labels is a list of floats (which can't be split)
        labels = [ '\n'.join(wrap(str(l), 15)) for l in labels ]

        # Added this to make testing quicker
        if redraw == 'y':
            # Now plot first plot
            sns.barplot(x = labels, y = df_temp[current], data = df_temp).set_title(title)
            # Make gap at bottom bigger for labels (it's a fraction, not a measurement)
            plt.subplots_adjust(bottom=0.3)
            plt.ylabel('No. of outcomes')
            plt.xticks(rotation=90)
            plt.savefig(STOREFILENAME + 'basic_counts/' + title + '.png', format = 'png', dpi = 150)
            plt.show()
            # Funnliy enough, Seaborn seems a bit sticky. There's a weird kind of
            # colour bleed from one plot to the next. However, by explicitly clearing the 
            # frame in the following step, it's all sorted
            plt.clf()

    return


def main():
    """
    Main function to run program
    """
    
    df = get_data_and_merge(DATAFILENAME1, DATAFILENAME2)

    df = lower_case(df)

    basic_stats(df)

    find_strings(df)
    
    dfs_counts = get_counts(df)
    print(df.columns)
    
    redraw = input('Should I re-draw the charts? (y/n): ')
    plot_basic_seaborn(dfs_counts, redraw)
    

    
if __name__ == '__main__':
    main()