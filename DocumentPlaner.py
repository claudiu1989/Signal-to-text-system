# Standard library
import math

# Internal modules/packages
from DataImporter import data_importer, TimeSeries
from FactsDetector import getTrendEvents, TrendMagnitude

theme = ['indicator', 'period']

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

def levelOfImportanceByMagnitude(event_magnitude):
    if event_magnitude

def getInterestingEvents(all_events):
    pass

if __name__ == '__main__':
    print(levelOfImportanceByTimeSpan(1960,1980))
    