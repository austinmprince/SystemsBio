from gapFillFunction import gapfillfunc, findInsAndOuts, printAndWriteOutput
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import flux_analysis
from cobra import Reaction
from summaryModified import summaryModified


# printAndWriteOutput('2016_06_23_gapped_meoh_producing.xml', 'ModelSEED-reactions-db.xlsEdited - Reactions.tsv', 200
#                     , True, 'gapFillOutput.txt')

model = create_cobra_model_from_sbml_file('2016_06_23_gapped_meoh_producing.xml')


x = model.metabolites.get_by_id('cpd00047_c0')
print(x.name)






