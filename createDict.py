from cobra import Model, Reaction
# Reads through the text file and takes out different data fields (id, reaction)
# that are tab delimited adds them to an dictionary from which they can be added to the
# universal reactions model
def createDict(file):
    Universal = Model("Universal Reactions")
    f = open('file', 'r')
    rxn_dict = {}
    for line in f:
        rxn_items = line.split('\t')
        rxn_dict[rxn_items[0]] = rxn_items[2]
    for rxnName in rxn_dict.keys():
        rxn = Reaction(rxnName)
        Universal.add_reaction(rxn)
        rxn.reaction = rxn_dict[rxnName]
    return Universal