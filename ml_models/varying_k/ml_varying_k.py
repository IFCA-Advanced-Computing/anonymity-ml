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
import sklearn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV


def train_models(data, test_split: int = 42):
    df = pd.read_csv(data)
    age = preprocessing.LabelEncoder().fit(df['age'])
    df['age'] = age.transform(df['age'])

    education = preprocessing.LabelEncoder().fit(df['education'])
    df['education'] = education.transform(df['education'])

    relationship = preprocessing.LabelEncoder().fit(df['relationship'])
    df['relationship'] = relationship.transform(df['relationship'])

    occupation = preprocessing.LabelEncoder().fit(df['occupation'])
    df['occupation'] = occupation.transform(df['occupation'])

    sex = preprocessing.LabelEncoder().fit(df['sex'])
    df['sex'] = sex.transform(df['sex'])

    nc = preprocessing.LabelEncoder().fit(df['native-country'])
    df['native-country'] = nc.transform(df['native-country'])

    X = df[['age', 'education', 'relationship', 'occupation', 'sex', 'native-country']].values
    y = df['salary-class'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=test_split, stratify=y)

    # kNN
    knn = KNeighborsClassifier(metric='minkowski')
    param_grid = {'n_neighbors': list(range(3, 51))}
    grid_knn = GridSearchCV(knn, param_grid, cv=5, refit=True)
    grid_knn.fit(X_train, y_train)
    knn = grid_knn.best_estimator_
    acc_knn = knn.score(X_test, y_test)
    pred_knn = knn.predict(X_test)
    pred_knn_bin = [0 if y == '<=50K' else 1 for y in pred_knn]
    y_test_bin = [0 if y == '<=50K' else 1 for y in y_test]
    fpr_knn, tpr_knn, thresholds = sklearn.metrics.roc_curve(y_test_bin, pred_knn_bin)
    auc_knn = sklearn.metrics.auc(fpr_knn, tpr_knn)

    # Random forest:
    rf = RandomForestClassifier(n_estimators=100, criterion='gini', random_state=42)
    param_grid = {'max_depth': [2, 3, 4, 5, 6, 7, 8, 9]}
    grid_rf = GridSearchCV(rf, param_grid, cv=5, refit=True)
    grid_rf.fit(X_train, y_train)
    rf = grid_rf.best_estimator_
    acc_rf = rf.score(X_test, y_test)
    pred_rf = rf.predict(X_test)
    pred_rf_bin = [0 if y == '<=50K' else 1 for y in pred_rf]
    fpr_rf, tpr_rf, thresholds = sklearn.metrics.roc_curve(y_test_bin, pred_rf_bin)
    auc_rf = sklearn.metrics.auc(fpr_rf, tpr_rf)

    # Adaptive Boosting
    ab = AdaBoostClassifier(random_state=42)
    param_grid = {'n_estimators': [50, 100, 150], 'learning_rate': [0.01, 0.1, 0.5, 1]}
    grid_ab = GridSearchCV(ab, param_grid, cv=5, refit=True)
    grid_ab.fit(X_train, y_train)
    ab = grid_ab.best_estimator_
    acc_ab = ab.score(X_test, y_test)
    pred_ab = ab.predict(X_test)
    pred_ab_bin = [0 if y == '<=50K' else 1 for y in pred_ab]
    fpr_ab, tpr_ab, thresholds = sklearn.metrics.roc_curve(y_test_bin, pred_ab_bin)
    auc_ab = sklearn.metrics.auc(fpr_ab, tpr_ab)

    # Gradient Tree Boosting
    gb = GradientBoostingClassifier(random_state=42)
    param_grid = {'n_estimators': [50, 100, 150],
                  'learning_rate': [0.01, 0.1, 0.5, 1],
                  'max_depth': [2, 4, 6, 8, 10]}
    grid_gb = GridSearchCV(gb, param_grid, cv=5, refit=True)
    grid_gb.fit(X_train, y_train)
    gb = grid_gb.best_estimator_
    acc_gb = gb.score(X_test, y_test)
    pred_gb = gb.predict(X_test)
    pred_gb_bin = [0 if y == '<=50K' else 1 for y in pred_gb]
    fpr_gb, tpr_gb, thresholds = sklearn.metrics.roc_curve(y_test_bin, pred_gb_bin)
    auc_gb = sklearn.metrics.auc(fpr_gb, tpr_gb)

    accuracy = [acc_knn, acc_rf, acc_ab, acc_gb]
    auc = [auc_knn, auc_rf, auc_ab, auc_gb]
    model = ['knn', 'rf', 'ab', 'gb']

    return model, accuracy, auc


for k in [2, 5, 10, 15, 20, 25, 50, 75, 100]:
    data = f'../../data/adult_k{k}_new.csv'
    models, accuracy, auc = train_models(data, test_split=42)
    print(f'k={k}:')
    for i, model in enumerate(models):
        print(f'Model: {model}. Accuracy: {accuracy[i]}. AUC: {auc[i]}')
