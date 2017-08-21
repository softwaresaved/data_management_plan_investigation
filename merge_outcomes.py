#!/usr/bin/env python
# encoding: utf-8


import pandas as pd
import numpy as np
import csv
import os.path

DATA_FILE_DIR = "./data/"


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


def get_data_and_merge():
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
        if file.endswith('.csv') & (file != 'all_outcomes.csv'):
            # Create a nice name for each df
            df_name = file[:-4]
            dfs_imports[df_name] = import_csv_to_df(DATA_FILE_DIR + str(file))
            # Lower case the colnames, because they haven't been consistently typed
            dfs_imports[df_name].columns = [x.lower() for x in dfs_imports[df_name].columns]
            # Lowercase all the columns that contain text
            for current_col in dfs_imports[df_name].columns:
                # i.e. if the column contains text...
                if dfs_imports[df_name][current_col].dtype == object:
                    dfs_imports[df_name][current_col].str.lower()
    # Merge all the dfs in the dict into a super-df
    df = pd.concat(dfs_imports.values())

    return df


def main():
    """
    Main function to run program
    """
    
    df = get_data_and_merge()
    
    print('The data frame contains ' + str(len(df)) + ' outcomes') 
    
    export_to_csv(df, DATA_FILE_DIR, 'all_outcomes')

if __name__ == '__main__':
    main()
    