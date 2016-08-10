from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Reaction, flux_analysis
import re
import pickle
from Functions.gapFillFunction import findInsAndOuts

def parsimonious_fba(model, db):
    '''
    :param model: Takes in a model in SBML format and converts it into a cobrapy model
    :param db: Takes in a database of reactions to be added to the model that will make
    it feasible to solve
    :return: Will run a parsimonious FBA on the model which reduces the sum of total fluxes through the model.
     Then the sources and sinks of ATP in the reaction will be printed so that we can analyze where ATP comes from
     and where it goes in this model as that will give us insight into the mechanism by which the GrowMatch algorithm has
     added a reaction that allows the model to produce methanol.
    '''
    model = create_cobra_model_from_sbml_file(model)
    rxn_list = pickle.load(open(db, 'rb'))
    # For loop that adds the reactions in a given run present in the dictionary to the model using regular expressions
    for run in rxn_list.keys():
        model_test = model.copy()
        fva_list = [model_test.reactions.ATPS]
        for rxn in rxn_list[run]:
            addID = re.search('(rxn\d{5}_reverse)|(rxn\d{5})', rxn).group(0)
            formula = re.search('(cpd\d{5}.*$)|(\d+.\d+\scpd\d{5}.*$)', rxn).group(0)
            rxn = Reaction(addID)
            model_test.add_reaction(rxn)
            rxn.reaction = formula
        # Creates a test model to run ParsFBA on and then prints out the run as well as the sources/sinks of ATP in the
        # reactions
        model_fba_test = model_test.copy()
        flux_analysis.optimize_minimal_flux(model_fba_test)
        # fluxes = findInsAndOuts(model_fba_test)
        # sorted_outs = fluxes[0]
        # sorted_ins = fluxes[1]
        print run
        model_fba_test.metabolites.get_by_id('cpd00002_c0').summary()

def categorize_reactions(model, db, category):
    fva_result_dict = {}
    # Wide range of ATP Synthase flux values can be positive or negative
    category_1_dict = {}
    # ATP Synthase flux can only be negative
    category_2_dict = {}
    # ATP Synthase flux can only be positive
    category_3_dict = {}
    model = create_cobra_model_from_sbml_file(model)
    rxn_list = pickle.load(open(db, 'rb'))
    for run in rxn_list.keys():
        model_test = model.copy()
        fva_list = [model_test.reactions.ATPS]
        for rxn in rxn_list[run]:
            addID = re.search('(rxn\d{5}_reverse)|(rxn\d{5})', rxn).group(0)
            formula = re.search('(cpd\d{5}.*$)|(\d+.\d+\scpd\d{5}.*$)', rxn).group(0)
            rxn = Reaction(addID)
            model_test.add_reaction(rxn)
            rxn.reaction = formula
            fva_list.append(rxn)
        fva_result = flux_analysis.flux_variability_analysis(model_test, fva_list)
        fva_result_dict[run] = fva_result
    for run in fva_result_dict:
        if fva_result_dict[run]['ATPS']['maximum'] > 0 and fva_result_dict[run]['ATPS']['minimum'] < 0:
            category_1_dict[run] = fva_result_dict[run]
        elif fva_result_dict[run]['ATPS']['maximum'] > 0:
            category_2_dict[run] = fva_result_dict[run]
        else:
            category_3_dict[run] = fva_result_dict[run]
    if category == 1:
        return category_1_dict.keys()
    elif category == 2:
        return category_2_dict.keys()
    else:
        return category_3_dict.keys()







