# from cobra.io.sbml import create_cobra_model_from_sbml_file
# from cobra import Model, Reaction, flux_analysis
# import pandas
#
#
#
# mattModel = create_cobra_model_from_sbml_file("2016_06_23_gapped_meoh_producing.xml")
#
# mattTest = mattModel.to_array_based_model()
# pandas.DataFrame(
#     data=mattTest.S.todense(),
#     columns=mattTest.reactions.list_attr("id"),
#     index=mattTest.metabolites.list_attr("id"))
#
#
# def findExcRxns(model):
#     print model.S

import cobra.test
import pandas
m = cobra.test.create_test_model("mini")
m = m.to_array_based_model()
pandas.DataFrame(
    data=m.S.todense(),
    columns=m.reactions.list_attr("id"),
    index=m.metabolites.list_attr("id"))