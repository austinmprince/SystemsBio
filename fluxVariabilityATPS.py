import mpld3
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Reaction, flux_analysis, Model
import pickle
import re
import matplotlib.pyplot as plt
import numpy as np
import operator
# mpld3.enable_notebook()


model = create_cobra_model_from_sbml_file('Models'+'/2016_06_23_gapped_meoh_producing.xml')
Universal = Model('Universal Reactions')

# f = open('ModelSEED-reactions-db.xlsEdited - Reactions.tsv', 'r')
# next(f)
# rxn_dict = {}
# Creates a dictionary of the reactions from the tab delimited database, storing their ID and the reaction string
# for line in f:
#     rxn_items = line.split('\t')
#     rxn_dict[rxn_items[0]] = rxn_items[6], rxn_items[1]
# # Adds the reactions from the above dictionary to the Universal model
# for rxnName in rxn_dict.keys():
#     rxn = Reaction(rxnName)
#     Universal.add_reaction(rxn)
#     rxn.reaction = rxn_dict[rxnName][0]
#     rxn.name = rxn_dict[rxnName][1]

rxn_list = pickle.load(open('Text Files'+'/rxn_dict.p', 'rb'))
fva_result_dict = {}
fva_result_dict_testing = {}
atps_list = {}
other_mechanism = {}
# Wide range of ATP Synthase flux values can be positive or negative
category_1_dict = {}
# ATP Synthase flux can only be negative
category_2_dict = {}
# ATP Synthase flux can only be positive
category_3_dict = {}
category_1_dict_testing = {}
category_2_dict_testing = {}
category_3_dict_testing = {}
run_not_1512 = {}

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


    model_fba_test = model_test.copy()
    # print run
    # print model_fba_test.optimize().f
    # for rxn in model_fba_test.reactions:
    #     fba = model_fba_test.reactions.get_by_id('rxn01512_LSQBKT_c0_RSQBKT_').x
    #     if model_fba_test.reactions.get_by_id(rxn.id).x > fba:
    #         print rxn.id
    #         print run
    # print run
    # print model_fba_test.metabolites.get_by_id('cpd00002_c0').summary()
    fva_result = flux_analysis.flux_variability_analysis(model_test, fva_list)
    if fva_result['ATPS']['maximum'] == 1000.0:
        x = 1
    elif fva_result['ATPS']['maximum'] >= 0:
        x = 2
    else:
        x = 3
    fva_result_dict[run] = fva_result
    fva_result_dict_testing[run] = fva_result, fva_list
    flux_analysis.optimize_minimal_flux(model_fba_test)
    list = {}
    list[run] = x,  (model_fba_test.solution.f/model_fba_test.reactions.rxn10568_LSQBKT_c0_RSQBKT_.x) * 1000

    print '%s : %s : %s' %(run, ((model_fba_test.solution.f/model_fba_test.reactions.rxn10568_LSQBKT_c0_RSQBKT_.x) * 1000), x)

print list
# for run in fva_result_dict:
#     if fva_result_dict[run]['ATPS']['minimum'] > 0:
#         atps_list[run] = fva_result_dict[run]
#     else:
#         other_mechanism[run] = fva_result_dict[run]
atp_min = {}
atp_max = {}
# print fva_result_dict
#
for run in fva_result_dict:
    atp_min[run] = round(fva_result_dict[run]['ATPS']['minimum'])
    atp_max[run] = round(fva_result_dict[run]['ATPS']['maximum'])




# for run in fva_result_dict:
#     if fva_result_dict[run]['ATPS']['maximum'] > 0 and fva_result_dict[run]['ATPS']['minimum'] < 0:
#         category_1_dict[run] = fva_result_dict[run]
#     elif fva_result_dict[run]['ATPS']['maximum'] > 0:
#         category_2_dict[run] = fva_result_dict[run]
#     else:
#         category_3_dict[run] = fva_result_dict[run]
#
#
#
# for run in fva_result_dict_testing:
#     if fva_result_dict_testing[run][0]['ATPS']['maximum'] > 0 and fva_result_dict_testing[run][0]['ATPS']['minimum'] < 0:
#         category_1_dict_testing[run] = fva_result_dict_testing[run]
#     elif fva_result_dict_testing[run][0]['ATPS']['maximum'] > 0:
#         category_2_dict_testing[run] = fva_result_dict_testing[run]
#     else:
#         category_3_dict_testing[run] = fva_result_dict_testing[run]

# for run in category_3_dict_testing:
#     print category_3_dict_testing[run][1]
#     for rxn in category_3_dict_testing[run][1]:
#         print Universal.reactions.get_by_id(rxn.id).reaction

# rxn_list = []
# met =
# for run in category_1_dict:
#     for rxn in fva_result_dict[run]:
#         rxn_list.append(fva_result_dict[run].keys())

# plt.hist(atp_max)
# plt.title('ATP Synthase Flux Histogram')
# plt.xlabel('Max flux value')
# plt.ylabel('Frequency')
# plt.savefig('SynthaseMax.pdf')

# plt.hist(atp_min)
# plt.title('ATP Synthase Flux Histogram')
# plt.xlabel('Min flux value')
# plt.ylabel('Frequency')
# plt.savefig('SynthaseMin.pdf')

#
# fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
# N = len(atp_min)
#
# ax.grid(color='white', linestyle='solid')
#
# ax.set_title("ATP Synthase Scatter Plot", size=20)
# ax.set_xlabel('ATP Synthase FVA Max Flux')
# ax.set_ylabel('ATP Synthase FVA Min Flux')
# scatter = ax.scatter(atp_max.values(),
#                      atp_min.values(),
#                      c=np.random.random(size=N),
#                      s=1000 * np.random.random(size=N),
#                      alpha=0.3,
#                      cmap=plt.cm.jet)
# labels = ['point {0}'.format(i) for i in atp_min.keys()]
# tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
# mpld3.plugins.connect(fig, tooltip)
#
# mpld3.show()

