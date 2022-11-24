
import numpy as np
from facts_detector import Trend

# Define a mock PCFG

no_distinct_sentences = float(3)

PCFG = {'<text>':[(['<paragraph>', '<text_fragment>'],0.5), (['<paragraph>'], 0.5)], 
        '<text_fragment>':[(['<paragraph>', '<text_fragment>'],0.5), (['<paragraph>'], 0.5)],
        '<paragraph>':[(['<sentence>', '<paragraph>', '\n'],0.5), (['<sentence>'], 0.5)],
        '<sentence>':[(['The', '[series_name]', 'has', '[change]','between', '[interval]'],1.0/no_distinct_sentences),
                      (['The', '[series_name]', 'has', '[change]','[change_rate]','between', '[interval]'],1.0/no_distinct_sentences),
                      (['The', '[series_name]', 'has', '[change]','[change_rate]','between', '[interval]'],1.0/no_distinct_sentences)]
        }


def generatePCFG(events_and_importances):
    C_PCFG = {'<text>':[(['<intro_paragraph>', '<text_fragment>', '<concluding_paragraph>'], 1.0)]}
    C_PCFG['<intro_paragraph>'] = [('In the next paragraphs you will find the main findings.', 0.25),
                                   ('The following text contains a summary of the main findings.', 0.25),
                                   ('In this text you will find the most interesting aspects of the data.', 0.25),
                                   ('We are now presenting the main conclusions.', 0.25)]
    
    C_PCFG['<concluding_paragraph>'] = [(['These were the main findings.'], 0.25),
                                   (['We hope you found the analysis useful.'], 0.25),
                                   (['These were the most interesting facts about the data.'], 0.25),
                                   ([''], 0.25)]
    paragraphs = list()
    C_PCFG['<text_fragment>'] = [(paragraphs, 1.0)]
    for i, series_events in enumerate(events_and_importances.items()):
        C_PCFG['<text_fragment>'][0][0].append(f'<paragraph{i}>')
        sentences = list()
        C_PCFG[f'<paragraph{i}>'] = [(sentences, 1.0)]
        for j, event in enumerate(series_events[1]):
            C_PCFG[f'<paragraph{i}>'][0][0].append(f'<sentence{j}>')
            C_PCFG[f'<sentence{j}>'] = [([f'A {convertTrendEnumObjectToWord(event[0].trend)} trend had been detected between {event[0].start_year} and {event[0].end_year} for the series "{series_events[0].lower()}". '], 0.25), 
                ([f'For the series "{series_events[0].lower()}", a {convertTrendEnumObjectToWord(event[0].trend)} trend was detected between {event[0].start_year} and {event[0].end_year}. '], 0.25),
                ([f'For the indicator "{series_events[0].lower()}", a {convertTrendEnumObjectToWord(event[0].trend)} trend was detected in the time interval {event[0].start_year} - {event[0].end_year}. '], 0.25), 
                ([f'Between {event[0].start_year} and {event[0].end_year}, a {convertTrendEnumObjectToWord(event[0].trend)} trend was detected  for the indicator "{series_events[0].lower()}". '], 0.25)]
        C_PCFG[f'<paragraph{i}>'][0][0].append('\n\n')
    return C_PCFG

def convertTrendEnumObjectToWord(trend):
    if trend == Trend.GROWTH:
        return 'growth'
    elif trend == Trend.DECREASE:
        return 'decrease'
    else:
        return 'constant'


def getRandomIndex(p):
    sample = np.random.multinomial(1, p, size=1)
    return np.where(sample==1.0)[1][0]

def isTerminal(symbol):
    if symbol[0] == '<' and symbol[-1] == '>':
        return False
    else:
        return True

def generateTextFromPCFG(PCFG):
    work_list = ['<text>']
    cr_work_index = 0
    list_of_rules = PCFG['<text>']
    non_terminals_available = True
    while non_terminals_available:
        # Get derivations probabilities for the current symbol
        p = []
        for rule in list_of_rules:
            p.append(rule[1])
        # Get derivation index
        rule_index = getRandomIndex(p)
        # Get the symbols for the choosen derivation
        new_symbols = list_of_rules[rule_index][0]
        # Replace the non-terminal symbol by it's derivation
        del work_list[cr_work_index]
        for i, symbol in enumerate(new_symbols):
            work_list.insert(cr_work_index+i, symbol)
        cr_symbol = work_list[cr_work_index]
        # Ignore the terminals
        notTheEnd = True  
        while isTerminal(cr_symbol) and notTheEnd:
            cr_work_index += 1
            if cr_work_index <= len(work_list)-1:
                cr_symbol = work_list[cr_work_index]
            else:
                notTheEnd = False
        # Get the derivation for the current non-terminal symbol
        if notTheEnd:
            list_of_rules = PCFG[cr_symbol]
        else:
            non_terminals_available = False
        print(work_list)

    return work_list

if __name__ == '__main__':
    # Test
    work_list = generateTextFromPCFG(PCFG)
    print(work_list)