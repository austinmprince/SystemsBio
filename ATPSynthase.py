from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Reaction
import pickle
import re

model = create_cobra_model_from_sbml_file('2016_06_23_gapped_meoh_producing.xml')

rxn_list = pickle.load(open('rxn_dict.p', 'rb'))
f = open('OtherRxns.txt', 'w')
b = open('ATPRxns.txt', 'w')
atps_list = {}
other_mechanism = {}
for run in rxn_list.keys():
    model_test = model.copy()
    for rxn in rxn_list[run]:
        addID = re.search('(rxn\d{5}_reverse)|(rxn\d{5})', rxn).group(0)
        formula = re.search('(cpd\d{5}.*$)|(\d+.\d+\scpd\d{5}.*$)', rxn).group(0)
        rxn = Reaction(addID)
        model_test.add_reaction(rxn)
        rxn.reaction = formula
    model_test.optimize()
    met = model_test.reactions.get_by_id('EX_cpd01024_LSQBKT_e0_RSQBKT_')
    if model_test.reactions.get_by_id('ATPS').x > (467.049840321*0.75):
        atps_list[run] = model_test.reactions.get_by_id('ATPS').x, rxn_list[run], \
                         met.x, model_test.solution.f
    else:
        other_mechanism[run] = model_test.reactions.get_by_id('ATPS').x, rxn_list[run], \
                               met.x, model_test.solution.f

for key in atps_list.keys():
    b.write('Run Number: ' + str(key))
    b.write('\n')
    print 'Run Number: ' + str(key)
    for rxn in atps_list[key][1]:
        b.write(rxn)
        b.write('\n')
        print rxn
    print 'Biomass Flux: ' + str(atps_list[key][3])
    b.write('Biomass Flux: ' + str(atps_list[key][3]))
    b.write('\n')
    print 'ATP Synthase Flux: ' + str(atps_list[key][0])
    b.write('ATP Synthase Flux: ' + str(atps_list[key][0]))
    b.write('\n')
    print 'Methane Flux: ' + str(atps_list[key][2])
    b.write('Methane Flux: ' + str(atps_list[key][2]))
    b.write('\n')
    print '--------------------'
    b.write('--------------------')
    b.write('\n')

for key in other_mechanism.keys():
    f.write('Run Number: ' + str(key))
    f.write('\n')
    print 'Run Number: ' + str(key)
    for rxn in other_mechanism[key][1]:
        f.write(rxn)
        f.write('\n')
        print rxn
    print 'Biomass Flux: ' + str(other_mechanism[key][3])
    f.write('Biomass Flux: ' + str(other_mechanism[key][3]))
    f.write('\n')
    print 'ATP Synthase Flux: ' + str(other_mechanism[key][0])
    f.write('ATP Synthase Flux: ' + str(other_mechanism[key][0]))
    f.write('\n')
    print 'Methane Flux: ' + str(other_mechanism[key][2])
    f.write('Methane Flux: ' + str(other_mechanism[key][2]))
    f.write('\n')
    print '--------------------'
    f.write('--------------------')
    f.write('\n')




