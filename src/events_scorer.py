# Standard library
import os

# Internal modules/packages
from data_importer import data_importer, TimeSeries
from facts_detector import getTrendEvents, TrendMagnitude, Trend

# The trend events are interesting if they span long periods, are more extrem and more general 

MAGNITUDE_WEIGHT = 0.5
PERIOD_WEIGHT = 0.75
GENERALITY_WEIGHT = 1.0

def getNoWordsInMainPart(name):
    parts = name.split('(')
    main_part = parts[0]
    no_words = len(main_part.split())
    return no_words

def levelOfGeneralityByNoWords(name):
    no_words = getNoWordsInMainPart(name)
    if no_words == 1:
        return 1
    elif no_words == 2:
        return 1
    elif no_words == 3:
        return 0.9
    elif no_words == 4:
        return 0.7
    else:
         return 0.5

def levelOfImportanceByTimeSpan(min_year, max_year):
    no_years = max_year - min_year
    return min(no_years*0.02, 1.0)

def levelOfImportanceByTrendTypeAndMagnitude(event_type, event_magnitude):
    if event_type == Trend.CONSTANT:
        return 0.5
    elif event_magnitude == TrendMagnitude.VERY_SLOWLY:
        return 0.1
    elif event_magnitude == TrendMagnitude.SLOWLY:
        return 0.2
    elif event_magnitude == TrendMagnitude.MODERATE:
        return 0.5
    elif event_magnitude == TrendMagnitude.FAST:
        return 0.8
    else:
        return 1

def getInterestingEvents(all_events_by_series):
    events_and_importances = {}
    for (series_name, all_events_for_series) in all_events_by_series.items():
        events_and_importances[series_name] = []
        for event in all_events_for_series:
            importance = MAGNITUDE_WEIGHT * levelOfImportanceByTrendTypeAndMagnitude(event.trend, event.trend_magnitude) 
            + PERIOD_WEIGHT * levelOfImportanceByTimeSpan(event.start_year, event.end_year) 
            + GENERALITY_WEIGHT * levelOfGeneralityByNoWords(series_name)
            events_and_importances[series_name].append((event, importance))
    return events_and_importances

def filterOutUnimportantEvets(events_and_importances, importance_threshold):

    filtered_events_and_importances = dict()
    for series_name in events_and_importances:
        filtered_events_for_cr_series = list(filter(lambda event: event[1]>=importance_threshold, events_and_importances[series_name]))
        if filtered_events_for_cr_series:
            filtered_events_and_importances[series_name] = filtered_events_for_cr_series
    return filtered_events_and_importances

if __name__ == '__main__':
     # Test
    cr_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.split(cr_dir)[0]
    data_path = os.path.join(parent_dir, 'DataWorldBank', 'Romania_data_test.csv')
    all_events_by_series = data_importer(data_path)
    all_trend_events = getTrendEvents(all_events_by_series)
    events = getInterestingEvents(all_trend_events)
    #print(events)
    filtered_events = filterOutUnimportantEvets(events,importance_threshold=0.5)
    print(filtered_events)