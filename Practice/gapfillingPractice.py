import cobra.test
import pandas
from cobra import Reaction



model = cobra.test.create_test_model("salmonella")


Universal = cobra.Model("Universal Reactions")
for i in [i.id for i in model.metabolites.f6p_c.reactions]:
    reaction = model.reactions.get_by_id(i)
    Universal.add_reaction(reaction.copy())
    reaction.remove_from_model()


# print(model.optimize().f)
#
# r = cobra.flux_analysis.growMatch(model, Universal)
# for e in r[0]:
#     print (e.id)

# result = cobra.flux_analysis.growMatch(model, Universal,
#                                        iterations = 4)
#
# for i, entries in enumerate(result):
#     print("---- Run %d ----" % (i + 1))
#     for e in entries:
#         print(e.id)



# print model.reactions
