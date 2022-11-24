import os
# Internal modules/packages
from data_importer import data_importer, TimeSeries
from facts_detector import getTrendEvents, TrendMagnitude, Trend
from events_scorer import getInterestingEvents, filterOutUnimportantEvets
from text_generator import generatePCFG, generateTextFromPCFG

cr_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.split(cr_dir)[0]
data_path = os.path.join(parent_dir, 'DataWorldBank', 'Romania_data_test.csv')
all_events_by_series = data_importer(data_path)
all_trend_events = getTrendEvents(all_events_by_series)
events = getInterestingEvents(all_trend_events)
#print(events)
filtered_events = filterOutUnimportantEvets(events,importance_threshold=0.5)
#print(filtered_events)
C_PCFG  = generatePCFG(filtered_events)
print(C_PCFG)
sentences = generateTextFromPCFG(C_PCFG)
print(''.join(sentences))