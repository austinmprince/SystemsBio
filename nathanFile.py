from cobra import Reaction, Model

f = open('Text Files'+'/ModelSEED-reactions-db.xlsEdited - Reactions.tsv', 'r')
temp = open('Text Files'+'/metabolites_H2.txt', 'r').read().split('\r\n')
smatrix_write_file = open('Text Files'+'/nathans_file_s_matrix.txt', 'w')
met_list_file = open('Text Files'+'/nathans_file_met_list', 'w')
met_list_check = []
met_list_in = []
met_list_not_in = []
next(f)
rxn_dict = {}
model_test = Model('Test Model')
for line in temp:
    met_list_check.append(line)
for line in f:
    rxn_items = line.split('\t')
    rxn_dict[rxn_items[0]] = rxn_items[6], rxn_items[1]
for rxnName in rxn_dict.keys():
    rxn = Reaction(rxnName)
    model_test.add_reaction(rxn)
    rxn.reaction = rxn_dict[rxnName][0]
    rxn.name = rxn_dict[rxnName][1]


for rxn in model_test.reactions:
    list = rxn.get_coefficients(rxn.metabolites)
# list = rxn_test.get_coefficients(rxn_test.metabolites)
    for item in rxn.metabolites.keys():
        string = (str(item) + '.' + str(rxn.id) + ' ' + str(rxn.metabolites[item]))
        print string
        smatrix_write_file.write(string)
        smatrix_write_file.write('\n')

for met in model_test.metabolites:
    met_list_in.append(met.id)
for met in met_list_in:
    if met not in met_list_check:
        met_list_not_in.append(met)
for item in met_list_not_in:
    met_list_file.write(item)
    met_list_file.write('\n')

