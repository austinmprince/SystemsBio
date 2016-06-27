from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Model, Reaction, flux_analysis
from copy import deepcopy
import re

mattModel = create_cobra_model_from_sbml_file("2016_06_23_gapped_meoh_producing.xml")
Universal = Model("Universal Reactions")
f = open('2015_test_db.txt', 'r')

def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item
def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=True)))

rxn_dict = {}
for line in f:
    rxn_items = line.split('\t')
    rxn_dict[rxn_items[0]] = rxn_items[2]

for rxnName in rxn_dict.keys():
    rxn = Reaction(rxnName)
    Universal.add_reaction(rxn)
    rxn.reaction = rxn_dict[rxnName]

growthValue = []
its = 4

result = flux_analysis.growMatch(mattModel, Universal, iterations=4)
resultShortened = sort_and_deduplicate(uniq(result))
print resultShortened
for x in range(len(resultShortened)):
    mattModelTest = deepcopy(mattModel)
    for i in range(len(resultShortened[x])):
        addID = resultShortened[x][i].id
        rxn = Reaction(addID)
        # rxn = Universal.reactions.get_by_id(addID)
        mattModelTest.add_reaction(rxn)
        rxn.reaction = resultShortened[x][i].reaction
        rxn.reaction = re.sub('\+ dummy\S+', '', rxn.reaction)
    growthValue.append(mattModelTest.optimize().f)
    mattModelTest = mattModel

for i in range(len(growthValue)):
    print growthValue[i]


