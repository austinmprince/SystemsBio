from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Model, Reaction, flux_analysis
from uniqAndSort import uniq, sort_and_deduplicate
import re
import time
start_time = time.time()
import operator


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
        in_fluxes = {}
        out_fluxes = {}
        for rxn in in_rxns:
            in_fluxes[rxn.name] = rxn.x
        for rxn in out_rxns:
            out_fluxes[rxn.name] = rxn.x
        sorted_out = sorted(out_fluxes.items(), key=operator.itemgetter(1), reverse=True)
        sorted_in = sorted(in_fluxes.items(), key=operator.itemgetter(1), reverse=True)
    funcModelTest = funcModel
    for i in range(len(resultShortened)):
        rxns_added[i] = resultShortened[i], growthValue[i], sorted_in, sorted_out
    return rxns_added

def printItems(model, database, runs):
    rxns_added = gapFillFunc(model, database, runs)
    for key in rxns_added.keys():
        print "-------------------------------"
        print "Run Number: " + str(key)
        print "-------------------------------"
        for i in range(len(rxns_added[key][0])):
            rxn_name = re.sub('\+ dummy\S+', '', rxns_added[key][0][i].reaction)
            print "%s : %s" %(rxns_added[key][0][i].id, rxn_name)
        print "-------------------------------"
        print "Objective function value: " + str(rxns_added[key][1])
        print "-------------------------------"
        print "Major in fluxes"
        for i in range(len(rxns_added[key][2])):
            print str(rxns_added[key][2][i][0]) + ": " + str(rxns_added[key][2][i][1])
        print "-------------------------------"
        print "Major out fluxes"
        for i in range(len(rxns_added[key][3])):
            print str(rxns_added[key][3][i][0]) + ": " + str(rxns_added[key][3][i][1])


