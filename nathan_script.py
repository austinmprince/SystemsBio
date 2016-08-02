from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Reaction, flux_analysis, Model
import pickle
import re

f = open('Text Files'+'/print_ferrodoxin_flux.txt','w')

model = create_cobra_model_from_sbml_file('Models'+'/2016_06_23_gapped_meoh_producing.xml')
Universal = Model('Universal Reactions')

rxns = model.metabolites.cpd11620_c0.reactions

rxn_list = pickle.load(open('Text Files'+'/rxn_dict.p', 'rb'))
rxns_added = []
total_rxns = {}
for run in rxn_list.keys():
    model_test = model.copy()
    fva_list = [model_test.reactions.ATPS]
    for rxn in rxn_list[run]:
        addID = re.search('(rxn\d{5}_reverse)|(rxn\d{5})', rxn).group(0)
        formula = re.search('(cpd\d{5}.*$)|(\d+.\d+\scpd\d{5}.*$)', rxn).group(0)
        rxn = Reaction(addID)
        model_test.add_reaction(rxn)
        rxn.reaction = formula
        rxns_added.append(rxn)
    total_rxns[run] = rxns_added
    rxns_added = []
    pfba_sol = flux_analysis.optimize_minimal_flux(model_test)
    rxns_list = []

    if model_test.reactions.rxn07191_LSQBKT_c0_RSQBKT_.x != 0 or model_test.reactions.rxn05939_LSQBKT_c0_RSQBKT_.x != 0 \
            or model_test.reactions.rxn07191_LSQBKT_c0_RSQBKT_.x != 0 or model_test.reactions.HdrABC.x != 0 or \
                    model_test.reactions.rxn05938_LSQBKT_c0_RSQBKT_.x != 0 or model_test.reactions.rxn06874_LSQBKT_c0_RSQBKT_.x != 0 or \
                    model_test.reactions.Hdr_formate.x != 0 or model_test.reactions.rxn10562_LSQBKT_c0_RSQBKT_.x != 0 or \
                    model_test.reactions.rxn11938_LSQBKT_c0_RSQBKT_.x != 0 or model_test.reactions.Eha_FSLASH_Ehb.x != 0 or\
                    model_test.reactions.rxn10561_LSQBKT_c0_RSQBKT_.x != 0 or model_test.reactions.CODH.x != 0 or \
                    model_test.reactions.rxn10563_LSQBKT_c0_RSQBKT_.x != 0:
        print '%s : %s' %(run, model_test.reactions.rxn07191_LSQBKT_c0_RSQBKT_.x)
        stx = str(run) + ' : ' + str(round(model_test.reactions.ATPS.x/model_test.reactions.Eha_FSLASH_Ehb.x, 2)) + ' : ' + str(round(model_test.solution.f, 2))
        f.write(stx)
        f.write('\n')
    print '%s : %s : %s' %(run, round(model_test.reactions.ATPS.x/model_test.reactions.Eha_FSLASH_Ehb.x, 3), round(model_test.solution.f, 3))
    string = str(run) + ' : ' + str(model_test.reactions.rxn07191_LSQBKT_c0_RSQBKT_.x)
    f.write(string)
    f.write('\n')
    for reactions in total_rxns[run]:
        print reactions.build_reaction_string(True)
        f.write(reactions.build_reaction_string(True))
        f.write('\n')
    f.write('\n')




