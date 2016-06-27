import pandas
from time import time

import cobra.test
from cobra.flux_analysis import \
    single_gene_deletion, single_reaction_deletion, \
    double_gene_deletion, double_reaction_deletion

cobra_model = cobra.test.create_test_model("textbook")
ecoli_model = cobra.test.create_test_model("ecoli")

f = open('geneDeletionOutput.txt','w')

gr, s = single_reaction_deletion(cobra_model, cobra_model.reactions[:20])
f.write(str(pandas.DataFrame.from_dict({"growth_rates" : gr, "status" : s})))
#
# gr, s  = single_gene_deletion(cobra_model, cobra_model.genes[:5])
# print(pandas.DataFrame.from_dict({"growth_rates": gr, "status": s}))
#
# gr, st = single_gene_deletion(cobra_model)
# f.write(str(pandas.DataFrame.from_dict({"growth_rates": gr,
#                             "status": st}).round(5)))
#
# gr, st = single_reaction_deletion(cobra_model)
# f.write(str(pandas.DataFrame.from_dict({"growth_rates": gr,
#                                   "status": st}).round(5)))
# f.write(str(double_gene_deletion(cobra_model,cobra_model.genes[-5:],
#                      return_frame=True)))
#
# f.write(str(double_reaction_deletion(cobra_model, cobra_model.reactions[:5],
#                                      return_frame=True).round(4)))