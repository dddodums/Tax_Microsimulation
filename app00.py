"""
app00.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app0.py > app0.res
CHECK: Use your favorite Windows diff utility to confirm that app0.res is
       the same as the app0.out file that is in the repository.
"""
import pandas as pd
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

grecs = GSTRecords()

# create CorpRecords object using cross-section data
crecs1 = CorpRecords(data='cit_cross.csv', weights='cit_cross_wgts.csv')
# Note: weights argument is optional
assert isinstance(crecs1, CorpRecords)
assert crecs1.current_year == 2017

# create CorpRecords object using panel data
crecs2 = CorpRecords(data='cit_panel.csv', data_type='panel')
assert isinstance(crecs2, CorpRecords)
assert crecs2.current_year == 2017

policy_filename = "current_law_policy_cmie.json"
# create Policy object containing current-law policy
pol = Policy(DEFAULTS_FILENAME=policy_filename)

# specify Calculator objects for current-law policy
calc1 = Calculator(policy=pol, corprecords=crecs1)
calc2 = Calculator(policy=pol, corprecords=crecs2)

# NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
#       so we can continue to use pol and recs in this script without any
#       concern about side effects from Calculator method calls on calc1.

assert isinstance(calc1, Calculator)
assert calc1.current_year == 2017
assert isinstance(calc2, Calculator)
assert calc2.current_year == 2017

# Produce DataFrame of results using cross-section
calc1.calc_all()
AggInc17c = calc1.carray('GTI_Before_Loss')
GTI17c = calc1.carray('deductions')
citax17c = calc1.carray('citax')
wgt17c = calc1.carray('weight')
calc1.increment_year()
calc1.calc_all()
AggInc18c = calc1.carray('GTI_Before_Loss')
GTI18c = calc1.carray('deductions')
citax18c = calc1.carray('citax')
wgt18c = calc1.carray('weight')
results_cross = pd.DataFrame({'Aggregate_Income2017': AggInc17c,
                              'citax2017': citax17c,
                              'Aggregate_Income2018': AggInc18c,
                              'citax2018': citax18c})
results_cross.to_csv('app00-dump-crosssection.csv', index=False,
                     float_format='%.0f')

# Produce DataFFrame of results using panel
# First do 2017
calc2.calc_all()
AggInc17p = calc2.carray('GTI_Before_Loss')
GTI17p = calc2.carray('deductions')
citax17p = calc2.carray('citax')
id17p = calc2.carray('ID_NO')
wgt17p = calc2.carray('weight')
results_panel17 = pd.DataFrame({'ID_NO': id17p,
                                'Aggregate_Income2017': AggInc17p,
                                'citax2017': citax17p})
# Then do 2018
calc2.increment_year()
calc2.calc_all()
AggInc18p = calc2.carray('GTI_Before_Loss')
GTI18p = calc2.carray('deductions')
citax18p = calc2.carray('citax')
id18p = calc2.carray('ID_NO')
wgt18p = calc2.carray('weight')
results_panel18 = pd.DataFrame({'ID_NO': id18p,
                                'Aggregate_Income2017': AggInc18p,
                                'citax2017': citax18p})
# Merge them together
results_panel = results_panel17.merge(right=results_panel18, how='outer',
                                      on='ID_NO')
results_panel.drop(['ID_NO'], axis=1, inplace=True)
results_panel.to_csv('app00-dump-panel.csv', index=False, float_format='%.0f')


print('GTI before loss, 2017, cross-section: ' +
      str(sum(AggInc17c * wgt17c) / 10**7))
print('Deductions, 2017, cross-section: ' +
      str(sum(GTI17c * wgt17c) / 10**7))
print('Total liability, 2017, cross-section: ' +
      str(sum(citax17c * wgt17c) / 10**7))
print('Tax rate, 2017, cross-section: ' +
      str(sum(citax17c * wgt17c) / sum(GTI17c * wgt17c)))
print('\n')
print('GTI before loss, 2017, panel: ' +
      str(sum(AggInc17p * wgt17p) / 10**7))
print('Deductions, 2017, panel: ' +
      str(sum(GTI17p * wgt17p) / 10**7))
print('Total liability, 2017, panel: ' +
      str(sum(citax17p * wgt17p) / 10**7))
print('Tax rate, 2017, panel: ' +
      str(sum(citax17p * wgt17p) / sum(GTI17p * wgt17p)))
print('\n')
print('GTI before loss, 2018, cross-section: ' +
      str(sum(AggInc18c * wgt18c) / 10**7))
print('Deductions, 2018, cross-section: ' + str(sum(GTI18c * wgt18c) / 10**7))
print('Total liability, 2018, cross-section: ' +
      str(sum(citax18c * wgt18c) / 10**7))
print('Tax rate, 2018, cross-section: ' +
      str(sum(citax18c * wgt18c) / sum(GTI18c * wgt18c)))
print('\n')
print('GTI before loss, 2018, panel: ' + str(sum(AggInc18p * wgt18p) / 10**7))
print('Deductions, 2018, panel: ' + str(sum(GTI18p * wgt18p) / 10**7))
print('Total liability, 2018, panel: ' + str(sum(citax18p * wgt18p) / 10**7))
print('Tax rate, 2018, panel: ' +
      str(sum(citax18p * wgt18p) / sum(GTI18p * wgt18p)))
print('\n')
print('Average liability, 2017, cross-section: ' +
      str(sum(citax17c * wgt17c) / sum(wgt17c) / 10**7))
print('Average liability, 2017, panel: ' +
      str(sum(citax17p * wgt17p) / sum(wgt17p) / 10**7))
