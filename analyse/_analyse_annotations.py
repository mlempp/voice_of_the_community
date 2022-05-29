'''
Autor: Martin Lempp

Kurzbeschreibung:
Analysiere die Annotationen mit einem multivariablen Regressor

'''
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error, f1_score, roc_auc_score
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from scipy.stats import uniform, randint
from sklearn.model_selection import RandomizedSearchCV
import pickle
from datetime import datetime as timer
from datetime import date
from _helper_functions import *
d = date.today().strftime("%y%m%d") + '_' + timer.now().strftime("%H%M%S")


#load
path = os.getcwd() + '/'
annotations = pd.read_csv(path + '_for_annotation2.csv', sep=';', index_col=0)

#prep
annotations = annotations[(annotations['annotation (-2 bis 2)'] != ' ') & ( annotations.Sentiment_score_2.isin(['negative', 'neutral', 'positive']))].copy()
annotations['annotation (-2 bis 2)'] = annotations['annotation (-2 bis 2)'].astype(int)
annotations['Sentiment_score_2_update'] = annotations.Sentiment_score_2.replace({'negative': -1, 'neutral': 0, 'positive': 1})
annotations['annotation_classified'] = annotations['annotation (-2 bis 2)'].apply(translate_to_class)

train_test_split = int(0.9*annotations.shape[0])
ids = np.arange(annotations.shape[0])
np.random.shuffle(ids)
train = annotations.iloc[:train_test_split]
test = annotations.iloc[train_test_split:]
X_train, Y_train =train[['Sentiment_score_1', 'Sentiment_score_2_update', 'Sentiment_score_3','Sentiment_score_4', 'Sentiment_score_5',]],train['annotation (-2 bis 2)']
X_test, Y_test =test[['Sentiment_score_1', 'Sentiment_score_2_update', 'Sentiment_score_3','Sentiment_score_4', 'Sentiment_score_5',]],test['annotation (-2 bis 2)']

models = []
metrics = []

#ridge
ridge_reg = Ridge()
distributions = {'alpha' : uniform(0,100)}
rscv_ridge_reg = RandomizedSearchCV(ridge_reg, distributions, random_state=0, scoring= 'r2',n_iter = 100 )
search_ridge_reg = rscv_ridge_reg.fit(X_train, Y_train)
Y_predict = search_ridge_reg.best_estimator_.predict(X_test)
r2_ridge = r2_score(Y_test, Y_predict)
mse_ridge = mean_squared_error(Y_test, Y_predict)
f1_ridge = f1_score(Y_test.apply(translate_pos),list(map(translate_pos, Y_predict)), average='weighted')
rand_pos_ridge = annotations.loc[X_test.iloc[np.argsort(Y_predict)[-10:]].index.values].comment
models.append(search_ridge_reg.best_estimator_)
metrics.append(f1_ridge)
filename = f'analyse/{d}_ridge_reg.sav'
pickle.dump(search_ridge_reg.best_estimator_, open(filename, 'wb'))


#gbt regressor
gbt_reg = GradientBoostingRegressor(max_depth=1, random_state=0)
distributions = {'n_estimators' : randint(1,100), 'learning_rate': uniform(0,1)}
rscv_gbt_reg = RandomizedSearchCV(gbt_reg, distributions, random_state=0, scoring= 'r2',n_iter = 100 )
search_gbt_reg = rscv_gbt_reg.fit(X_train, Y_train)
Y_predict = search_gbt_reg.best_estimator_.predict(X_test)
r2_gbt_reg = r2_score(Y_test, Y_predict)
mse_gbt_reg = mean_squared_error(Y_test, Y_predict)
f1_gbt_reg = f1_score(Y_test.apply(translate_pos),list(map(translate_pos, Y_predict)), average='weighted')
rand_pos_gbt_reg = annotations.loc[X_test.iloc[np.argsort(Y_predict)[-10:]].index.values].comment
models.append(search_gbt_reg.best_estimator_)
metrics.append(f1_gbt_reg)
filename = f'analyse/{d}_gbt_reg.sav'
pickle.dump(search_gbt_reg.best_estimator_, open(filename, 'wb'))


#gbt classifier
X_train_clf, Y_train_clf =train[['Sentiment_score_1', 'Sentiment_score_2_update', 'Sentiment_score_3','Sentiment_score_4', 'Sentiment_score_5',]],train['annotation_classified']
X_test_clf, Y_test_clf =test[['Sentiment_score_1', 'Sentiment_score_2_update', 'Sentiment_score_3','Sentiment_score_4', 'Sentiment_score_5',]],test['annotation_classified']

gbt_clf = GradientBoostingClassifier(random_state=0)
distributions = {'n_estimators' : randint(1,200), 'learning_rate': uniform(0,1), 'min_samples_split':  randint(2,15)}
rscv_gbt_clf = RandomizedSearchCV(gbt_clf, distributions, random_state=0, scoring= 'f1_weighted',n_iter = 20, verbose=1 )
search_gbt_clf = rscv_gbt_clf.fit(X_train_clf, Y_train_clf)
Y_predict_clf = search_gbt_clf.best_estimator_.predict(X_test_clf)
f1_gbt_clf = f1_score(Y_test_clf,Y_predict_clf, average='weighted')
rand_pos_gbt_clf = annotations.loc[X_test_clf.iloc[np.argsort(Y_predict_clf)[-10:]].index.values].comment
models.append(search_gbt_clf.best_estimator_)
metrics.append(f1_gbt_clf)
filename = f'analyse/{d}_gbt_clf.sav'
pickle.dump(search_gbt_clf.best_estimator_, open(filename, 'wb'))


#save best
model_names=['ridge_reg', 'gbt_reg', 'gbt_clf']
filename = f'analyse/{d}_best_model_{model_names[np.argmax(metrics)]}.sav'
pickle.dump(models[np.argmax(metrics)], open(filename, 'wb'))
