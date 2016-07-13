from gapFillFunction import gapfillfunc, findInsAndOuts, printAndWriteOutput, return_reaction_list, findTransportRxns
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import flux_analysis
from cobra import Reaction
from summaryModified import summaryModified

#
# printAndWriteOutput('2016_06_23_gapped_meoh_producing.xml', 'ModelSEED-reactions-db.xlsEdited - Reactions.tsv', 2,
#                    False)



removeTransportRxns('ModelSEED-reactions-db.xlsEdited - Reactions.tsv')





