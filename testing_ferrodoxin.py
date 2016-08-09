from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Reaction, flux_analysis, Model
import pickle
import re

f = open('Text Files'+'/print_ferrodoxin_flux.txt','w')

model = create_cobra_model_from_sbml_file('Models'+'/2016_06_23_gapped_meoh_producing.xml')
Universal = Model('Universal Reactions')

rxn_list = pickle.load(open('Text Files'+'/rxn_dict.p', 'rb'))
fva_result_dict = {}
atps_dict = {}

for run in rxn_list.keys():
    model_test = model.copy()
    rxns_added = []
    fva_list = [model_test.reactions.ATPS, model_test.reactions.Eha_FSLASH_Ehb]
    for rxn in rxn_list[run]:
        addID = re.search('(rxn\d{5}_reverse)|(rxn\d{5})', rxn).group(0)
        formula = re.search('(cpd\d{5}.*$)|(\d+.\d+\scpd\d{5}.*$)', rxn).group(0)
        rxn = Reaction(addID)
        model_test.add_reaction(rxn)
        rxn.reaction = formula
        fva_list.append(rxn)
        rxns_added.append(rxn)
    fva_result = flux_analysis.flux_variability_analysis(model_test, fva_list)
    fva_result_dict[run] = fva_result, rxns_added
    rxns_added = []

for run in fva_result_dict.keys():
    if fva_result_dict[run][0]['ATPS']['minimum'] > 0 and fva_result_dict[run][0]['ATPS']['maximum'] == 1000 \
        and fva_result_dict[run][0]['Eha_FSLASH_Ehb']['maximum'] < 0:
        atps_dict[run] = fva_result_dict[run]

for run in atps_dict.keys():
    print run
    model_testing = model.copy()
    for i in range(len(atps_dict[run][1])):
        model_testing.add_reaction(atps_dict[run][1][i])
        print atps_dict[run][1][i].build_reaction_string(True)
        print atps_dict[run][1][i].reaction
    flux_analysis.optimize_minimal_flux(model_testing)
    model_testing.metabolites.cpd11620_c0.summary()
    model_testing = model.copy()
    print '\n'



