from gapFillFunction import gapFillFunc, printItems, writeItems
from cobra import flux_analysis
import re
# print gapFillFunc('2016_06_23_gapped_meoh_producing.xml', '2015_test_db.txt', 4)


# printItems('2016_06_23_gapped_meoh_producing.xml', 'ModelSEED-reactions-db.xlsEdited - Reactions.tsv', 2)
writeItems('gapFillOutput.txt','2016_06_23_gapped_meoh_producing.xml', 'ModelSEED-reactions-db.xlsEdited - Reactions.tsv', 2 )



