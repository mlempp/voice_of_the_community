'''
Autor: Martin Lempp

Kurzbeschreibung:
Analysiere die Annotationen mit einem multivariablen Regressor

'''
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error, f1_score, roc_auc_score, precision_score, recall_score,balanced_accuracy_score
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier, RandomForestClassifier
from scipy.stats import uniform, randint
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
import pickle
from datetime import datetime as timer
from datetime import date
from imblearn.over_sampling import SMOTE

import json
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")


#load
path = os.getcwd() + '/'
sys.path.insert(0, path + 'functions/')
from _helper_functions import *
annotations = pd.read_csv(path + '_for_annotation2.csv', sep=';', index_col=0)

#prep
annotations = annotations[(annotations['annotation (-2 bis 2)'] != ' ') & ( annotations.Sentiment_score_2.isin(['negative', 'neutral', 'positive']))].copy()
df_comments = load_newest_comment_file(path)
columns_OI =['Sentiment_score_1', 'Sentiment_score_2', 'Sentiment_score_3', 'Sentiment_score_4', 'Sentiment_score_5', 'Sentiment_score_6',
             'Sentiment_score_10', 'Sentiment_score_11', 'Sentiment_score_7', 'Sentiment_score_8', 'Sentiment_score_9', 'Sentiment_score_12',
             'Sentiment_score_13', 'Sentiment_score_14']
for col in columns_OI:
    annotations[col] = 0

for i,row in annotations.iterrows():
    tmp = df_comments[df_comments.comment_ID == row.comment_ID].copy().iloc[0]
    annotations.loc[i,columns_OI] = tmp[columns_OI].values


annotations['annotation (-2 bis 2)'] = annotations['annotation (-2 bis 2)'].astype(int)
annotations['Sentiment_score_2_update'] = annotations.Sentiment_score_2.replace({'negative': -1, 'neutral': 0, 'positive': 1})
annotations['annotation_classified'] = annotations['annotation (-2 bis 2)'].apply(translate_to_class)

columns_OI =['Sentiment_score_1', 'Sentiment_score_2_update', 'Sentiment_score_3', 'Sentiment_score_4', 'Sentiment_score_5', 'Sentiment_score_6',
             'Sentiment_score_10', 'Sentiment_score_11', 'Sentiment_score_7', 'Sentiment_score_8', 'Sentiment_score_9', 'Sentiment_score_12',
             'Sentiment_score_13', 'Sentiment_score_14']



train_test_split = int(0.9*annotations.shape[0])
ids = np.arange(annotations.shape[0])
np.random.shuffle(ids)
train = annotations.iloc[:train_test_split]
test = annotations.iloc[train_test_split:]

class_imbalance = train.annotation_classified.value_counts()
missing_samples_neg = class_imbalance.max() - class_imbalance[class_imbalance.index== -1].values[0]
missing_samples_neu = class_imbalance.max() - class_imbalance[class_imbalance.index== 0].values[0]
missing_samples_pos = class_imbalance.max() - class_imbalance[class_imbalance.index== 1].values[0]
train_resampled = pd.concat([train, train[train.annotation_classified== -1].sample(missing_samples_neg, replace = True), train[train.annotation_classified== 0].sample(missing_samples_neu, replace = True), train[train.annotation_classified== 1].sample(missing_samples_pos, replace = True)] )


X_train, Y_train =train[columns_OI],train['annotation (-2 bis 2)']
X_test, Y_test =test[columns_OI],test['annotation (-2 bis 2)']

models = {}
models_and_metrics = {}



#ridge
ridge_reg = Ridge()
distributions = {'alpha' : uniform(0,100)}
rscv_ridge_reg = RandomizedSearchCV(ridge_reg, distributions, random_state=0, scoring= 'r2',n_iter = 100 )
search_ridge_reg = rscv_ridge_reg.fit(X_train, Y_train)
Y_predict_ridge = search_ridge_reg.best_estimator_.predict(X_test)
rand_pos_ridge = annotations.loc[X_test.iloc[np.argsort(Y_predict_ridge)[-10:]].index.values].comment

models['ridge_reg'] = {}
models_and_metrics['ridge_reg'] = {}
models['ridge_reg']['model'] = search_ridge_reg.best_estimator_
models_and_metrics['ridge_reg']['f1'] = f1_score(Y_test.apply(translate_pos),list(map(translate_pos, Y_predict_ridge)), average='weighted')
models_and_metrics['ridge_reg']['precision'] = precision_score(Y_test.apply(translate_pos),list(map(translate_pos, Y_predict_ridge)), average='weighted')
models_and_metrics['ridge_reg']['recall'] = recall_score(Y_test.apply(translate_pos),list(map(translate_pos, Y_predict_ridge)), average='weighted')
filename = f'analyse/{d}_ridge_reg.sav'
pickle.dump(search_ridge_reg.best_estimator_, open(filename, 'wb'))




#gbt regressor
gbt_reg = GradientBoostingRegressor(max_depth=1, random_state=0)
distributions = {'n_estimators' : randint(1,100), 'learning_rate': uniform(0,1)}
rscv_gbt_reg = RandomizedSearchCV(gbt_reg, distributions, random_state=0, scoring= 'r2',n_iter = 100 )
search_gbt_reg = rscv_gbt_reg.fit(X_train, Y_train)
Y_predict_gbt_reg = search_gbt_reg.best_estimator_.predict(X_test)
f1_gbt_reg = f1_score(Y_test.apply(translate_pos),list(map(translate_pos, Y_predict_gbt_reg)), average='weighted')
rand_pos_gbt_reg = annotations.loc[X_test.iloc[np.argsort(Y_predict_gbt_reg)[-10:]].index.values].comment

models['gbt_reg'] = {}
models_and_metrics['gbt_reg'] = {}
models['gbt_reg']['model'] = search_gbt_reg.best_estimator_
models_and_metrics['gbt_reg']['f1'] = f1_score(Y_test.apply(translate_pos),list(map(translate_pos, Y_predict_gbt_reg)), average='weighted')
models_and_metrics['gbt_reg']['precision'] = precision_score(Y_test.apply(translate_pos),list(map(translate_pos, Y_predict_gbt_reg)), average='weighted')
models_and_metrics['gbt_reg']['recall'] = recall_score(Y_test.apply(translate_pos),list(map(translate_pos, Y_predict_gbt_reg)), average='weighted')
filename = f'analyse/{d}_gbt_reg.sav'
pickle.dump(search_gbt_reg.best_estimator_, open(filename, 'wb'))



#gbt classifier
X_train_clf, Y_train_clf =train[columns_OI],train['annotation_classified']
X_test_clf, Y_test_clf =test[columns_OI],test['annotation_classified']

gbt_clf = GradientBoostingClassifier(random_state=0)
distributions = {'n_estimators' : randint(1,200), 'learning_rate': uniform(0,1), 'min_samples_split':  randint(2,15)}
rscv_gbt_clf = RandomizedSearchCV(gbt_clf, distributions, random_state=0, scoring= 'f1_weighted',n_iter = 20, verbose=1 )
search_gbt_clf = rscv_gbt_clf.fit(X_train_clf, Y_train_clf)
Y_predict_gbt_clf = search_gbt_clf.best_estimator_.predict(X_test_clf)
rand_pos_gbt_clf = annotations.loc[X_test_clf.iloc[np.argsort(Y_predict_gbt_clf)[-10:]].index.values].comment

models['gbt_clf'] = {}
models_and_metrics['gbt_clf'] = {}
models['gbt_clf']['model'] = search_gbt_clf.best_estimator_
models_and_metrics['gbt_clf']['f1'] = f1_score(Y_test_clf,Y_predict_gbt_clf, average='weighted')
models_and_metrics['gbt_clf']['precision'] = precision_score(Y_test_clf,Y_predict_gbt_clf, average='weighted')
models_and_metrics['gbt_clf']['recall'] = recall_score(Y_test_clf,Y_predict_gbt_clf, average='weighted')
models_and_metrics['gbt_clf']['acc_pos'] = balanced_accuracy_score(Y_test_clf.apply(translate_pos), list(map(translate_pos, Y_predict_gbt_clf)))
models_and_metrics['gbt_clf']['acc_neuf'] = balanced_accuracy_score(Y_test_clf.apply(translate_neu), list(map(translate_neu, Y_predict_gbt_clf)))
models_and_metrics['gbt_clf']['acc_neg'] = balanced_accuracy_score(Y_test_clf.apply(translate_neg), list(map(translate_neg, Y_predict_gbt_clf)))
filename = f'analyse/{d}_gbt_clf.sav'
pickle.dump(search_gbt_clf.best_estimator_, open(filename, 'wb'))



#rf classifier
X_train_clf, Y_train_clf =train[columns_OI],train['annotation_classified']
X_test_clf, Y_test_clf =test[columns_OI],test['annotation_classified']
rf_clf = RandomForestClassifier(random_state=0)
distributions = {'n_estimators' : randint(1,200), 'min_samples_split':  randint(2,15)}
rscv_rf_clf = RandomizedSearchCV(rf_clf, distributions, random_state=0, scoring= 'f1_weighted',n_iter = 20, verbose=1 )
search_rf_clf = rscv_rf_clf.fit(X_train_clf, Y_train_clf)
Y_predict_rf_clf = search_rf_clf.best_estimator_.predict(X_test_clf)
rand_pos_rf_clf = annotations.loc[X_test_clf.iloc[np.argsort(Y_predict_rf_clf)[-10:]].index.values].comment

models['rf_clf'] = {}
models_and_metrics['rf_clf'] = {}
models['rf_clf']['model'] = search_rf_clf.best_estimator_
models_and_metrics['rf_clf']['f1'] = f1_score(Y_test_clf,Y_predict_rf_clf, average='weighted')
models_and_metrics['rf_clf']['precision'] = precision_score(Y_test_clf,Y_predict_rf_clf, average='weighted')
models_and_metrics['rf_clf']['recall'] = recall_score(Y_test_clf,Y_predict_rf_clf, average='weighted')
models_and_metrics['rf_clf']['acc_pos'] = balanced_accuracy_score(Y_test_clf.apply(translate_pos), list(map(translate_pos, Y_predict_rf_clf)))
models_and_metrics['rf_clf']['acc_neuf'] = balanced_accuracy_score(Y_test_clf.apply(translate_neu), list(map(translate_neu, Y_predict_rf_clf)))
models_and_metrics['rf_clf']['acc_neg'] = balanced_accuracy_score(Y_test_clf.apply(translate_neg), list(map(translate_neg, Y_predict_rf_clf)))
filename = f'analyse/{d}_rf_clf.sav'
pickle.dump(search_rf_clf.best_estimator_, open(filename, 'wb'))




#neigh
X_train_clf, Y_train_clf =train[columns_OI],train['annotation_classified']
X_test_clf, Y_test_clf =test[columns_OI],test['annotation_classified']
neigh_clf = KNeighborsClassifier()
distributions = {'n_neighbors' : randint(1,20), 'leaf_size': randint(1,200), 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
rscv_neigh_clf = RandomizedSearchCV(neigh_clf, distributions, random_state=0, scoring= 'f1_weighted',n_iter = 20, verbose=1 )
search_neigh_clf = rscv_neigh_clf.fit(X_train_clf, Y_train_clf)
Y_predict_neigh_clf = search_neigh_clf.best_estimator_.predict(X_test_clf)
rand_pos_neigh_clf = annotations.loc[X_test_clf.iloc[np.argsort(Y_predict_neigh_clf)[-10:]].index.values].comment

models['neigh_clf'] = {}
models_and_metrics['neigh_clf'] = {}
models['neigh_clf']['model'] = search_neigh_clf.best_estimator_
models_and_metrics['neigh_clf']['f1'] = f1_score(Y_test_clf,Y_predict_neigh_clf, average='weighted')
models_and_metrics['neigh_clf']['precision'] = precision_score(Y_test_clf,Y_predict_neigh_clf, average='weighted')
models_and_metrics['neigh_clf']['recall'] = recall_score(Y_test_clf,Y_predict_neigh_clf, average='weighted')
models_and_metrics['neigh_clf']['acc_pos'] = balanced_accuracy_score(Y_test_clf.apply(translate_pos), list(map(translate_pos, Y_predict_neigh_clf)))
models_and_metrics['neigh_clf']['acc_neuf'] = balanced_accuracy_score(Y_test_clf.apply(translate_neu), list(map(translate_neu, Y_predict_neigh_clf)))
models_and_metrics['neigh_clf']['acc_neg'] = balanced_accuracy_score(Y_test_clf.apply(translate_neg), list(map(translate_neg, Y_predict_neigh_clf)))
filename = f'analyse/{d}_neigh_clf.sav'
pickle.dump(search_neigh_clf.best_estimator_, open(filename, 'wb'))



from scipy import stats
#ensemble clfs

Y_predict_ensemble = stats.mode(np.array([Y_predict_gbt_clf, Y_predict_rf_clf, Y_predict_neigh_clf])).mode[0]
models_and_metrics['ensemble'] = {}
models_and_metrics['ensemble']['f1'] = f1_score(Y_test_clf,Y_predict_ensemble, average='weighted')
models_and_metrics['ensemble']['precision'] = precision_score(Y_test_clf,Y_predict_ensemble, average='weighted')
models_and_metrics['ensemble']['recall'] = recall_score(Y_test_clf,Y_predict_ensemble, average='weighted')
models_and_metrics['ensemble']['acc_pos'] = balanced_accuracy_score(Y_test_clf.apply(translate_pos), list(map(translate_pos, Y_predict_ensemble)))
models_and_metrics['ensemble']['acc_neuf'] = balanced_accuracy_score(Y_test_clf.apply(translate_neu), list(map(translate_neu, Y_predict_ensemble)))
models_and_metrics['ensemble']['acc_neg'] = balanced_accuracy_score(Y_test_clf.apply(translate_neg), list(map(translate_neg, Y_predict_ensemble)))



#save best
model_names = list(models_and_metrics.keys())
models_ = [models[x]['model'] for x in model_names if x != 'ensemble']
model_f1s = [models_and_metrics[x]['f1'] for x in model_names if x != 'ensemble']

filename = f'analyse/{d}_best_model_{list(model_names)[np.argmax(model_f1s)]}.sav'
pickle.dump(models_[np.argmax(model_f1s)], open(filename, 'wb'))

with open(f'analyse/{d}_metrics.json', 'w') as fp:
    json.dump(models_and_metrics, fp,  indent=4)

