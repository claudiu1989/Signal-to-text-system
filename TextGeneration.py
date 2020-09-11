

import numpy as np

# Define the PCFG

no_distinct_sentences = float(3)

PCFG = {'<text>':[(['<paragraph>', '<text_fragment>'],0.5), (['<paragraph>'], 0.5)], 
        '<text_fragment>':[(['<paragraph>', '<text_fragment>'],0.5), (['<paragraph>'], 0.5)],
        '<paragraph>':[(['<sentence>', '<paragraph>', '\n'],0.5), (['<sentence>'], 0.5)],
        '<sentence>':[(['The', '[series_name]', 'has', '[change]','between', '[interval]'],1.0/no_distinct_sentences),
                      (['The', '[series_name]', 'has', '[change]','[change_rate]','between', '[interval]'],1.0/no_distinct_sentences),
                      (['The', '[series_name]', 'has', '[change]','[change_rate]','between', '[interval]'],1.0/no_distinct_sentences)]
        }

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
    #p = [0.5,0.2,0.3]
    #sample = getProbabilitiesForProductionRules(p)
    work_list = generateTextFromPCFG(PCFG)
    print(work_list)