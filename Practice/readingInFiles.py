from cobra import Reaction, Model, flux_analysis
from cobra.io.sbml import create_cobra_model_from_sbml_file
from copy import deepcopy

toyModel = create_cobra_model_from_sbml_file("toy_model.xml")

f = open('toyModelrxns.txt','r')
Universal = Model("Universal Reactions")

rxn_dict = {}
for line in f:
    rxn_items = line.split('\t')
    rxn_dict[rxn_items[0]] = rxn_items[1]

for rxnName in rxn_dict.keys():
    rxn = Reaction(rxnName)
    Universal.add_reaction(rxn)
    rxn.reaction = rxn_dict[rxnName]

its = 4
result = flux_analysis.growMatch(toyModel, Universal, iterations=its)
growthValue = []
for x in range(its):
    toyModelTest = deepcopy(toyModel)
    for i in range(len(result[x])):
        addID = result[x][i].id
        rxn = Universal.reactions.get_by_id(addID)
        toyModelTest.add_reaction(rxn)
    growthValue.append(toyModelTest.optimize().f)
    toyModelTest = toyModel



