import cobra.test
import os
from cobra.io.sbml import create_cobra_model_from_sbml_file
import pandas

f = open('modelPractice.txt','w')
mouseModel = create_cobra_model_from_sbml_file('iMM1415.xml')

# for x in cobra_model.metabolites:
#     f.write("%s : %s" %(x.id, x.name))
#     f.write('\n')

# mouseModel.optimize()
# print(mouseModel.solution.status)
# print(mouseModel.solution.f)
#
# fva_output = cobra.flux_analysis.flux_variability_analysis(mouseModel, mouseModel.reactions[3700:])
# f.write(str(pandas.DataFrame.from_dict(fva_output).T.round(5)))

checkvar = mouseModel.optimize()

gr, s = cobra.flux_analysis.single_gene_deletion(mouseModel, mouseModel.genes)
# f.write(str(pandas.DataFrame.from_dict({"growth_rates" : gr, "status" : s})))

for key in gr:
    if gr[key] != checkvar:
        print gr[key]












