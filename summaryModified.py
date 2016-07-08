from cobra import flux_analysis
from cobra.io.sbml import create_cobra_model_from_sbml_file
import operator

def summaryModified(model):
    model.optimize()
    print model.solution.status, model.solution.f
    out_rxns = model.reactions.query(
        lambda rxn: rxn.x > (model.solution.f*0.1), None
        ).query(lambda x: x, 'boundary')
    in_rxns = model.reactions.query(
            lambda rxn: rxn.x < -(model.solution.f*0.1), None
        ).query(lambda x: x, 'boundary')
    in_fluxes = {}
    out_fluxes = {}
    for rxn in in_rxns:
        in_fluxes[rxn.name] = rxn.x
    for rxn in out_rxns:
        out_fluxes[rxn.name] = rxn.x
    sorted_out = sorted(out_fluxes.items(), key=operator.itemgetter(1), reverse=True)
    sorted_in = sorted(in_fluxes.items(), key=operator.itemgetter(1), reverse=False)

    print "Major in fluxes"
    for i in range(len(sorted_in)):
        print str(sorted_in[i][0]), ':', str(sorted_in[i][1])
    print "-------------------------------"
    print "Major out fluxes"
    for i in range(len(sorted_out)):
        print str(sorted_out[i][0]), ':', str(sorted_out[i][1])
    print "-------------------------------"

