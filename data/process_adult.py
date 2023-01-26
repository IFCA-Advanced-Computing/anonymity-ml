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

"""
Process adult dataset for different anonymity levels.
"""


def delete_rows(file_name, quasi_ident, new_file, fillna=True):
    """Delete the rows of the given file in which all QIs are  set to *.
    Also fills NA values with 0."""
    df = pd.read_csv(file_name)
    df_qi = df[quasi_ident]
    df = df[:len(df_qi[df_qi != ['*'] * len(quasi_ident)].dropna(how='all'))]
    if fillna:
        df.fillna(0, inplace=True)
    df.to_csv(new_file, index=False)


QI = ['age', 'education', 'occupation', 'relationship', 'sex', 'native-country']
for i in [2, 5, 10, 15, 20, 25, 50, 75, 100]:
    file = f'data/adult_k{i}.csv'
    NEW_FILE_NAME = f'data/adult_k{i}_new.csv'
    delete_rows(file, QI, NEW_FILE_NAME)
    print(f'Saved file: {NEW_FILE_NAME}')

file = f'adult_k5_l2.csv'
NEW_FILE_NAME = f'adult_k5_l2_new.csv'
delete_rows(file, QI, NEW_FILE_NAME)
print(f'Saved file: {NEW_FILE_NAME}')

file = f'adult_k5_t07.csv'
NEW_FILE_NAME = f'adult_k5_t07_new.csv'
delete_rows(file, QI, NEW_FILE_NAME)
print(f'Saved file: {NEW_FILE_NAME}')

file = f'adult_k5_beta15.csv'
NEW_FILE_NAME = f'adult_k5_beta15_new.csv'
delete_rows(file, QI, NEW_FILE_NAME)
print(f'Saved file: {NEW_FILE_NAME}')
