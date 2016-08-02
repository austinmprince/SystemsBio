from Functions import parsFBA
# gapFillFunction.printAndWriteOutput('Models'+'/2016_06_23_gapped_meoh_producing.xml', 'Text Files'+'/ModelSEED-reactions-db.xlsEdited - Reactions.tsv', 2,
#                    False)
# parsFBA.parsimoniousFBA('Models' + '/2016_06_23_gapped_meoh_producing.xml', 'Text Files' + '/rxn_dict.p')
print parsFBA.categorize_reactions('Models' + '/2016_06_23_gapped_meoh_producing.xml', 'Text Files' + '/rxn_dict.p', 3)
















