'''
Autor: Martin Lempp

Kurzbeschreibung:
Analysiere die Annotationen mit einem multivariablen Regressor

'''
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error, f1_score
from sklearn.ensemble import GradientBoostingRegressor
from scipy.stats import uniform, randint
from sklearn.model_selection import RandomizedSearchCV



#load
path = os.getcwd() + '/'
annotations = pd.read_csv(path + '_for_annotation2.csv', sep=';', index_col=0)

#prep
annotations = annotations[(annotations['annotation (-2 bis 2)'] != ' ') & ( annotations.Sentiment_score_2.isin(['negative', 'neutral', 'positive']))].copy()
annotations['Sentiment_score_2_update'] = annotations.Sentiment_score_2.replace({'negative': -1, 'neutral': 0, 'positive': 1})

train_test_split = int(0.9*annotations.shape[0])
ids = np.arange(annotations.shape[0])
np.random.shuffle(ids)
train = annotations.iloc[:train_test_split]
test = annotations.iloc[train_test_split:]
X_train, Y_train =train[['Sentiment_score_1', 'Sentiment_score_2_update', 'Sentiment_score_3','Sentiment_score_4', 'Sentiment_score_5',]],train['annotation (-2 bis 2)']
X_test, Y_test =test[['Sentiment_score_1', 'Sentiment_score_2_update', 'Sentiment_score_3','Sentiment_score_4', 'Sentiment_score_5',]],test['annotation (-2 bis 2)']


#ridge

ridge = Ridge()
distributions = {'alpha' : uniform(0,100)}
clf = RandomizedSearchCV(ridge, distributions, random_state=0, scoring= 'r2',n_iter = 100 )
search = clf.fit(X_train, Y_train)
Y_predict = search.best_estimator_.predict(X_test)
r2_ridge = r2_score(Y_test, Y_predict)
mse_ridge = mean_squared_error(Y_test, Y_predict)

#gbt
est = GradientBoostingRegressor(max_depth=1, random_state=0)
distributions = {'n_estimators' : randint(1,100), 'learning_rate': uniform(0,1)}
est = RandomizedSearchCV(est, distributions, random_state=0, scoring= 'r2',n_iter = 100 )
search = est.fit(X_train, Y_train)
Y_predict = search.best_estimator_.predict(X_test)
r2_gbt = r2_score(Y_test, Y_predict)
mse_gbt = mean_squared_error(Y_test, Y_predict)

# f1 = f1_score(Y_test, Y_predict)
