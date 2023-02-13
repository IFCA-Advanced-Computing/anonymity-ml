# Copyright 2022 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pandas as pd
from pycanon.report import print_report

"""
Check the level of anonymity according to several metrics in the
different scenarios".
"""

# Quasi-identifiers and sensitive attribute:
QI = ['age', 'education', 'occupation', 'relationship', 'sex', 'native-country']
SA = ['salary-class']

print('Use case: k=5:')
print_report(pd.read_csv('../data/adult_k5_new.csv'), QI, SA)

print('\nUse case: k=5, l=2:')
print_report(pd.read_csv('../data/adult_k5_l2_new.csv'), QI, SA)

print('\nUse case: k=5, t=0.7:')
print_report(pd.read_csv('../data/adult_k5_t07_new.csv'), QI, SA)

print('\nUse case: k=5, delta=1.5:')
print_report(pd.read_csv('../data/adult_k5_delta15_new.csv'), QI, SA)

