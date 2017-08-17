#!/usr/bin/env python
# encoding: utf-8


import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import math
import seaborn as sns
from textwrap import wrap


DATAFILENAME1 = "./data/researchdatabaseandmodelsearch-1502793915306.csv"
DATAFILENAME2 = "./data/researchmaterialsearch-1502793014976.csv"
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

    df1 = import_csv_to_df(file1)
    df2 = import_csv_to_df(file2)

    frames = [df1, df2]
    
    df = pd.concat(frames)

    return df


def get_counts(df):

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
    
    dfs_counts = get_counts(df)
    print(df.columns)
    
    redraw = input('Should I re-draw the charts? (y/n): ')
    plot_basic_seaborn(dfs_counts, redraw)
    
if __name__ == '__main__':
    main()
