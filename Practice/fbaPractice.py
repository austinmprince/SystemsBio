import cobra.test

model = cobra.test.create_test_model("textbook")


model.change_objective("CO2t")
model.optimize().f
print model.solution.status
model.summary()
model.metabolites.atp_c.summary()