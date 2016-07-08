from gapFillFunction import gapFillFunc, findInsAndOuts, printAndWriteOutput
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import flux_analysis
from cobra import Reaction
from summaryModified import summaryModified


printAndWriteOutput('2016_06_23_gapped_meoh_producing.xml', 'ModelSEED-reactions-db.xlsEdited - Reactions.tsv', 2
                    , False)

# model = create_cobra_model_from_sbml_file('2016_06_23_gapped_meoh_producing.xml')
# modelTest = create_cobra_model_from_sbml_file('2016_06_23_sbml.xml')
#
# rxn = Reaction('rxn11987')
# model.add_reaction(rxn)
# rxn.reaction = '3.0 cpd00001_c0 + cpd01078_c0 + 6.0 cpd11621_c0 --> 6.0 cpd00067_c0 + cpd03387_c0 + 6.0 cpd11620_c0'
# summaryModified(model)





