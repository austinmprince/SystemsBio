
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('png', 'pdf')

import cobra.test
from cobra.flux_analysis import calculate_phenotype_phase_plane

model = cobra.test.create_test_model("textbook")

data = calculate_phenotype_phase_plane(
    model, "EX_glc__D_e", "EX_o2_e")
data.plot_matplotlib();
