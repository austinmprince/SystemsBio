from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Model, Reaction, flux_analysis
from uniqAndSort import uniq, sort_and_deduplicate
import re
import time
import operator
from copy import deepcopy

start_time = time.time()


def gapfillfunc(model, database, runs):
    """ This function gapfills the model using the growMatch algorithm that is built into cobrapy

    Returns a dictionary which contains the pertinent information about the gapfilled model such as
    the reactions added, the major ins and outs of the system and the objective value of the gapfilled
    model.
    This function calls on two other functions sort_and_deduplicate to assure the uniqueness of the solutions
    and findInsAndOuts to find major ins and outs of the model when gapfilled when certain reactions
    Args:
        model: a model in SBML format
        database: an external database database of reactions to be used for gapfilling
        runs: integer number of iterations the gapfilling algorithm will run through
    """
    # Read model from SBML file and create Universal model to add reactions to
    func_model = create_cobra_model_from_sbml_file(model)
    Universal = Model("Universal Reactions")
    f = open(database, 'r')
    next(f)
    rxn_dict = {}
    # Creates a dictionary of the reactions from the tab delimited database, storing their ID and the reaction string
    for line in f:
        rxn_items = line.split('\t')
        rxn_dict[rxn_items[0]] = rxn_items[6], rxn_items[1]
    # Adds the reactions from the above dictionary to the Universal model
    for rxnName in rxn_dict.keys():
        rxn = Reaction(rxnName)
        Universal.add_reaction(rxn)
        rxn.reaction = rxn_dict[rxnName][0]
        rxn.name = rxn_dict[rxnName][1]

    # Runs the growMatch algorithm filling gaps from the Universal model
    result = flux_analysis.growMatch(func_model, Universal, iterations=runs)
    resultShortened = sort_and_deduplicate(uniq(result))
    rxns_added = {}
    rxn_met_list = []
    print resultShortened
    for x in range(len(resultShortened)):
        func_model_test = deepcopy(func_model)
        # print func_model_test.optimize().f
        for i in range(len(resultShortened[x])):
            addID = resultShortened[x][i].id
            rxn = Reaction(addID)
            func_model_test.add_reaction(rxn)
            rxn.reaction = resultShortened[x][i].reaction
            rxn.reaction = re.sub('\+ dummy\S+', '', rxn.reaction)
            rxn.name = resultShortened[x][i].name
            mets = re.findall('cpd\d{5}_c0|cpd\d{5}_e0', rxn.reaction)
            for met in mets:
                y = func_model_test.metabolites.get_by_id(met)
                rxn_met_list.append(y.name)
        obj_value = func_model_test.optimize().f
        fluxes = findInsAndOuts(func_model_test)
        sorted_outs = fluxes[0]
        sorted_ins = fluxes[1]
        rxns_added[x] = resultShortened[x], obj_value, sorted_ins, sorted_outs, rxn_met_list
        rxn_met_list = []
    return rxns_added


def printAndWriteOutput(model, database, runs, writeCommand, writeFile='gapFillOuput.txt'):
    """
    This function prints and writes the output gained from the gapfilling function in a nice form
    Args
        :param model: the gapped model that is to be filled
        :param database: a database of reactions that will fill the model
        :param runs: the number of iterations the gapfilling algorithm will run through
        :param writeCommand: boolean variable of whether the output should be written to a file
        :param writeFile: the destination file
    """
    f = open(writeFile, 'w')
    rxns_added = gapfillfunc(model, database, runs)
    # print rxns_added
    for key in rxns_added.keys():
        print "-------------------------------"
        print "Run Number: " + str(key)
        print "-------------------------------"
        for i in range(len(rxns_added[key][0])):
            rxn_name = re.sub('\+ dummy\S+', '', rxns_added[key][0][i].reaction)
            print "%s : %s" % (rxns_added[key][0][i].id, rxn_name)
        for y in rxns_added[key][4]:
            print y
        print "-------------------------------"
        print "Objective function value: " + str(rxns_added[key][1])
        print "-------------------------------"
        print "Major in fluxes"
        for i in range(len(rxns_added[key][3])):
            print str(rxns_added[key][3][i][0]) + ": " + str(rxns_added[key][3][i][1])
        print "-------------------------------"
        print "Major out fluxes"
        for i in range(len(rxns_added[key][3])):
            print str(rxns_added[key][2][i][0]) + ": " + str(rxns_added[key][2][i][1])
        print "-------------------------------"
    time_final = time.time()
    print "Time to run: " + str(time_final - start_time)
    if writeCommand == True:
        for key in rxns_added.keys():
            f.write("-------------------------------\n")
            f.write("Run Number: " + str(key) + '\n')
            f.write("-------------------------------\n")
            for i in range(len(rxns_added[key][0])):
                rxn_name = re.sub('\+ dummy\S+', '', rxns_added[key][0][i].reaction)
                f.write("%s : %s" % (rxns_added[key][0][i].id, rxn_name) + '\n')
            for y in rxns_added[key][4]:
                f.write(y)
            f.write("-------------------------------\n")
            f.write("Objective function value: " + str(rxns_added[key][1]) + '\n')
            f.write("-------------------------------\n")
            f.write("Major in fluxes\n")
            for i in range(len(rxns_added[key][3])):
                f.write(str(rxns_added[key][3][i][0]) + ": " + str(rxns_added[key][3][i][1]) + '\n')
            f.write("-------------------------------\n")
            f.write("Major out fluxes\n")
            for i in range(len(rxns_added[key][2])):
                f.write(str(rxns_added[key][2][i][0]) + ": " + str(rxns_added[key][2][i][1]) + '\n')
            f.write("-------------------------------\n")
        f.write("Time to run: " + str(time_final - start_time) + '\n')
    else:
        pass


def findInsAndOuts(model):
    testModel = model.copy()
    testModel.optimize()
    threshold = 1E-8
    out_rxns = testModel.reactions.query(
        lambda rxn: rxn.x > threshold, None
    ).query(lambda x: x, 'boundary')
    in_rxns = testModel.reactions.query(
        lambda rxn: rxn.x < -threshold, None
    ).query(lambda x: x, 'boundary')
    in_fluxes = {}
    out_fluxes = {}
    for rxn in in_rxns:
        in_fluxes[rxn.name] = rxn.x
    for rxn in out_rxns:
        out_fluxes[rxn.name] = rxn.x
    sorted_out = sorted(out_fluxes.items(), key=operator.itemgetter(1), reverse=True)
    sorted_in = sorted(in_fluxes.items(), key=operator.itemgetter(1), reverse=False)
    return sorted_out, sorted_in

def return_reaction_list(model, database, runs, write_file):
    f = open(write_file, 'w')
    rxns_added = gapfillfunc(model, database, runs)
    for key in rxns_added.keys():
        for i in range(len(rxns_added[key][0])):
                rxn_name = re.sub('\+ dummy\S+', '', rxns_added[key][0][i].reaction)
                f.write(rxns_added[key][0][i].id)
                f.write('\t')
                f.write(rxn_name)
        f.write('\n')

def findTransportRxns(database):
    f = open(database, 'r')
    next(f)
    rxn_dict = {}
    transRxnList = []
    for line in f:
        rxn_items = line.split('\t')
        rxn_dict[rxn_items[0]] = rxn_items[6]
    for rxn in rxn_dict:
        if re.search(r'_c0', rxn_dict[rxn]) and re.search(r'_e0', rxn_dict[rxn]):
            transRxnList.append(rxn)

    return transRxnList

# def removeTransportRxns(database, writingFile):
#     x = open(writingFile, 'w')
#     f = open
#     rxnList = findTransportRxns(database)
#     for i in range(len(rxnList)):
#         for line in x:
#             re.sub(rxnList[i], '',line)
