from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Reaction, flux_analysis
import re
import pickle
from Functions.gapFillFunction import findInsAndOuts

# model = create_cobra_model_from_sbml_file('Models'+'/2016_06_23_gapped_meoh_producing.xml')

rxn_list = pickle.load(open('Text Files'+'/rxn_dict.p', 'rb'))

for run in rxn_list.keys():
    model_test = model.copy()
    fva_list = [model_test.reactions.ATPS]
    for rxn in rxn_list[run]:
        addID = re.search('(rxn\d{5}_reverse)|(rxn\d{5})', rxn).group(0)
        formula = re.search('(cpd\d{5}.*$)|(\d+.\d+\scpd\d{5}.*$)', rxn).group(0)
        rxn = Reaction(addID)
        model_test.add_reaction(rxn)
        rxn.reaction = formula
    model_fba_test = model_test.copy()
    pFBA_sol = flux_analysis.optimize_minimal_flux(model_fba_test)
    fluxes = findInsAndOuts(model_fba_test)
    sorted_outs = fluxes[0]
    sorted_ins = fluxes[1]
    print run
    model_fba_test.metabolites.get_by_id('cpd00002_c0').summary()



