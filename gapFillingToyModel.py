from cobra.io.sbml import create_cobra_model_from_sbml_file
import csv
from cobra import Reaction, Model, flux_analysis
from copy import deepcopy
import re
import pandas as pd
# Creates a toy model by reading in Matt's toy model file
# written in smbl format
toyModel = create_cobra_model_from_sbml_file("toy_model.xml")
# Creates a model of universal reactions and reads through the database
# of reactions getting the reaction ID and overall reaction and adding them to
# the universal reactions model
Universal = Model("Universal Reactions")
f = open('toyModelrxns.txt', 'r')
# These two functions are used to make our list of functions unique so that no duplicate
# functions are run through the optimization protocol
def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item
def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=True)))
# Reads through the text file and takes out different data fields (id, reaction)
# that are tab delimited adds them to an dictionary from which they can be added to the
# universal reactions model
rxn_dict = {}
for line in f:
    rxn_items = line.split('\t')
    rxn_dict[rxn_items[0]] = rxn_items[1]
# Reads through the two arrays in which data from the text file was stored and
# creates reaction objects from these which are added to universal
for rxnName in rxn_dict.keys():
    rxn = Reaction(rxnName)
    Universal.add_reaction(rxn)
    rxn.reaction = rxn_dict[rxnName]
# Creates an array to add the value of the objective function after it is optimized
# so that we can compare the various gapfilling solutions
growthValue = []
its = 4
# Runs growMatch gapfilling algorithm on the toyModel taking reactions from universal
result = flux_analysis.growMatch(toyModel, Universal, iterations=4)
resultShortened = sort_and_deduplicate(uniq(result))
# Because grow match algorithm adds faulty metabolites to the model we instead go back and
# identify the reaction id which growMatch says needs to be added to the model. Then this
# code identifies this reaction and pulls it from universal to be inserted into our model
# this code also creates a test model called toyModelTest that reactions are added to and
# the optimal solution is then tested on for the different iterations of the growMatch algorithm
for x in range(len(resultShortened)):
    toyModelTest = Model.copy(toyModel)
    for i in range(len(resultShortened[x])):
        addID = resultShortened[x][i].id
        rxn = Reaction(addID)
        toyModelTest.add_reaction(rxn)
        rxn.reaction = resultShortened[x][i].reaction
        rxn.reaction = re.sub('\+ dummy\S+', '', rxn.reaction)
    solution = toyModelTest.optimize()
    growthValue.append(solution.x)
    print solution.f
    toyModelTest = toyModel

for i in range(len(growthValue)):
    print growthValue[i]