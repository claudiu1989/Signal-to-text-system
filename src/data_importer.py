import pandas as pd
import os
import math
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt

class TimeSeries: 
    def __init__(self, name, values, min_year, max_year):
        self.name = name
        self.values = values
        self.min_year = min_year
        self.max_year = max_year

def load_data(data_path):
    data = pd.read_csv(data_path)
    return data

def plot_time_series(years, values, indicator_name):
    plt.plot(years, values)
    plt.ylabel('Value')
    plt.xlabel('Year')
    plt.title(indicator_name)
    plt.show()

def get_min_max_years(data, start_of_time_column_index):
    columns = data.columns 
    min_year = columns[start_of_time_column_index]
    max_year = columns[-1]
    return int(min_year), int(max_year)

def get_series(data, row_index, index_column_series_name, start_of_time_column_index):
    series = data[row_index:row_index+1] 
    min_year, max_year = get_min_max_years(data, start_of_time_column_index)
    return TimeSeries(series.to_numpy()[0][index_column_series_name], series.to_numpy()[0][start_of_time_column_index:], min_year, max_year)
    #return series.to_numpy()[0][index_column_series_name], series.to_numpy()[0][start_of_time_column_index:]

def get_all_Series(data):
    no_series = len(data.index)
    all_series = [get_series(data, i, 2, 4) for i in range(no_series)]
    return all_series

# Main function
def data_importer(data_file_path):
    data = load_data(data_file_path)
    all_series = get_all_Series(data)
    return all_series

if __name__ == '__main__':
    # Test
    cr_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.split(cr_dir)[0]
    data_path = os.path.join(parent_dir, 'DataWorldBank', 'Romania_data_test.csv')
    data = load_data(data_path)
    all = get_all_Series(data)
    

