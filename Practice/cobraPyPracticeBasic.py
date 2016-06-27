from __future__ import print_function
import cobra.test
# from cobra.test import test_all
# test_all()
from cobra import Reaction

# model = cobra.test.create_test_model("textbook")
#
# print (len(model.reactions))
# print (len(model.metabolites))
# print (len(model.genes))
# print(model.reactions[29])
# #
# pgi = model.reactions.get_by_id("PGI")
# print(pgi.check_mass_balance())
# pgi.add_metabolites({model.metabolites.get_by_id("h_c"):-1})
# print(pgi.reaction)
# pgi.pop(model.metabolites.get_by_id("h_c"))
# print (pgi.reaction)
#
# atp = model.metabolites.get_by_id("atp_c")
# print (atp.name)
# print (atp.compartment)
# print (atp.charge)
# print(atp.formula)
# print (len(atp.reactions))
#
# gpr = pgi.gene_reaction_rule
# print(gpr)
# pgi.gene_reaction_rule = ("spam or eggs")
# print(pgi.genes)
#
#
#
#
#
#
#
#
areaction = Reaction("Austins rxn")
areaction.add_metabolites()
areaction.reaction = "a -> b"