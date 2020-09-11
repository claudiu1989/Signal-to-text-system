# Standard library
import os
import math
from enum import Enum

# Third party libraries
import numpy as np

# Internal modules/packages
from DataImporter import data_importer, TimeSeries

RELATIVE_WINDOW_SIZES = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

NAN_VALIDATION_THRESHOLD = 0.1

TREND_INCONSISTENCY_THERESHOLD = 0.1

TREND_MAGNITUDE_THRESHOLD_CONSTANT = 0.01
TREND_MAGNITUDE_THRESHOLD_VERY_SLOWLY = 0.005
TREND_MAGNITUDE_THRESHOLD_SLOWLY = 0.01
TREND_MAGNITUDE_THRESHOLD_MODERATE = 0.04
TREND_MAGNITUDE_THRESHOLD_FAST = 0.07

class SeriesTrendEvent:
    def __init__(self, trend, trend_magnitude, start_year, end_year, relative_variation, first_value, last_value):
        self.trend = trend
        self.trend_magnitude = trend_magnitude
        self.start_year = start_year
        self.end_year = end_year
        self.relative_variation = relative_variation
        self.first_value = first_value
        self.last_value = last_value
    def print(self):
        print(f'Trend: {self.trend}, Trend magnitude: {self.trend_magnitude}, Start year: {self.start_year}, End year: {self.end_year}, Relative variation: {self.relative_variation}, First value: {self.first_value}, Last value: {self.last_value}')

class Trend(Enum):
    CONSTANT = 0
    GROWTH = 1
    DECREASE = 2

class TrendMagnitude(Enum):
    VERY_SLOWLY = 0
    SLOWLY = 1
    MODERATE = 2
    FAST = 3
    VERY_FAST = 4

class SeriesTrends:
    def __init__(self, trend:Trend, magnitude:TrendMagnitude):
        self.trend = trend
        self.magnitude = magnitude

def nanValidation(partial_series)->bool:
    no_nan = 0
    for value in partial_series:
        if math.isnan(value):
            no_nan += 1
    if float(no_nan)/float(len(partial_series)) <= NAN_VALIDATION_THRESHOLD:
        return True
    else:
        return False

def validateTrend(partial_series):
    no_global_trend_violations = 0
    global_diff = partial_series[-1] - partial_series[0]
    
    for first_value, next_value in zip(partial_series[:-1],partial_series[1:]):
        if (next_value - first_value)*global_diff < 0:
            no_global_trend_violations += 1
    if float(no_global_trend_violations)/float(len(partial_series)) <= TREND_INCONSISTENCY_THERESHOLD:
         return True
    else:
         return False

def  getTrendMagnitude(first_value, global_diff, time_interval_length):
    relative_variation_per_year = (np.abs(float(global_diff))/float(first_value))/float(time_interval_length)
    if relative_variation_per_year < TREND_MAGNITUDE_THRESHOLD_VERY_SLOWLY:
        return TrendMagnitude.VERY_SLOWLY
    elif relative_variation_per_year < TREND_MAGNITUDE_THRESHOLD_SLOWLY:
        return TrendMagnitude.SLOWLY
    elif relative_variation_per_year < TREND_MAGNITUDE_THRESHOLD_MODERATE:
        return TrendMagnitude.MODERATE
    elif relative_variation_per_year < TREND_MAGNITUDE_THRESHOLD_FAST:
        return TrendMagnitude.FAST
    else:
        return  TrendMagnitude.VERY_FAST

def typeOfTrend(relative_variation, global_diff):
    if relative_variation < TREND_MAGNITUDE_THRESHOLD_CONSTANT or global_diff == 0.0:
        return Trend.CONSTANT
    elif global_diff < 0.0:
        return Trend.DECREASE
    else:
        return  Trend.GROWTH

def trendDetection(partial_series):
    if not nanValidation(partial_series):
        return None, None, None, None, None
    if not validateTrend(partial_series):
        return None, None, None, None, None

    global_diff = partial_series[-1] - partial_series[0]
    relative_variation = np.abs(float(global_diff))/float(partial_series[0])
    # Get type of trend
    trend = typeOfTrend(relative_variation, global_diff)
    # Get magnitude of trend
    if trend != Trend.CONSTANT:
        trend_magnitude = getTrendMagnitude(partial_series[0], global_diff, len(partial_series))
    else:
        trend_magnitude = None
    return trend, trend_magnitude, relative_variation, partial_series[0], partial_series[-1]

def getTrendEventsForWindow(series:TimeSeries, relative_window_size:float):
    length = series.max_year - series.min_year
    window_size = int(relative_window_size*length)
    all_trend_events = []
    for year_index in range(length-window_size):
        data_in_window = series.values[year_index:year_index+window_size]
        trend, trend_magnitude, relative_variation, first_value, last_value = trendDetection(data_in_window)
        if trend:
            start_year = series.min_year + year_index
            end_year = start_year + window_size
            event = SeriesTrendEvent(trend, trend_magnitude, start_year, end_year, relative_variation, first_value, last_value)
            all_trend_events.append(event)
    return all_trend_events

# Main function
def getTrendEvents(list_of_series:TimeSeries):
    trends_events_for_series = {}
    for series in list_of_series:
        for relative_window_size in RELATIVE_WINDOW_SIZES:
            all_trend_events = getTrendEventsForWindow(series, relative_window_size)
            if len(all_trend_events)>0:
                trends_events_for_series[series.name] = all_trend_events
                break
    return trends_events_for_series

if __name__ == '__main__':
    data_path = f"{os.path.dirname(os.path.realpath(__file__))}//DataWorldBank//Romania_data_test.csv"
    all_series = data_importer(data_path)
    all_trend_events = getTrendEvents(all_series)
    for name, events in all_trend_events.items():
        print(name)
        for event in events:
            event.print()