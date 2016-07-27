import parsimoniousFBA

# gapFillFunction.printAndWriteOutput('Models'+'/2016_06_23_gapped_meoh_producing.xml', 'Text Files'+'/ModelSEED-reactions-db.xlsEdited - Reactions.tsv', 2,
#                    False)
parsimoniousFBA('Models' + '/2016_06_23_gapped_meoh_producing.xml', 'Text Files' + '/rxn_dict.p', 'Text Files' + '/parsFBAResult.txt')

# model = create_cobra_model_from_sbml_file('2016_06_23_gapped_meoh_producing.xml')
# rxn = Reaction('rxn00435')
# model.add_reaction(rxn)
# rxn.reaction = 'cpd00047_c0 + cpd00067_c0 + cpd00116_c0 --> cpd00001_c0 + 2.0 cpd00055_c0'
# model.optimize()
# met = model.metabolites.get_by_id('cpd00002_c0')
# met.summary()









