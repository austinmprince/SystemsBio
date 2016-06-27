from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Model, Reaction, flux_analysis
from uniqAndSort import uniq, sort_and_deduplicate
import re
import time
start_time = time.time()
import pandas as pd


def gapFillFunc(model, database, runs):
    funcModel = create_cobra_model_from_sbml_file(model)
    Universal = Model("Universal Reactions")
    f = open(database, 'r')
    rxn_dict = {}
    for line in f:
        rxn_items = line.split('\t')
        rxn_dict[rxn_items[0]] = rxn_items[2]
    for rxnName in rxn_dict.keys():
        rxn = Reaction(rxnName)
        Universal.add_reaction(rxn)
        rxn.reaction = rxn_dict[rxnName]
    growthValue = []
    result = flux_analysis.growMatch(funcModel, Universal, iterations=runs)
    resultShortened = sort_and_deduplicate(uniq(result))
    rxns_added = {}
    for x in range(len(resultShortened)):
        funcModelTest = Model.copy(funcModel)
        for i in range(len(resultShortened[x])):
            addID = resultShortened[x][i].id
            rxn = Reaction(addID)
            funcModelTest.add_reaction(rxn)
            rxn.reaction = resultShortened[x][i].reaction
            rxn.reaction = re.sub('\+ dummy\S+', '', rxn.reaction)
        solution = funcModelTest.optimize()
        growthValue.append(solution.f)
        out_rxns = funcModelTest.reactions.query(
            lambda rxn: rxn.x > solution.f*0.1, None
        ).query(lambda x: x, 'boundary')
        in_rxns = funcModelTest.reactions.query(
            lambda rxn: rxn.x < -solution.f*0.1, None
        ).query(lambda x: x, 'boundary')



        funcModelTest = funcModel
    for i in range(len(resultShortened)):
        rxns_added[i] = resultShortened[i], growthValue[i]
    return rxns_added