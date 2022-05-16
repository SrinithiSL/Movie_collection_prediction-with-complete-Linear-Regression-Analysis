# -*- coding: utf-8 -*-
"""movie_collection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ptHW6JSz9LoSAz_eRS7trZM96pcrFVfP

##Importing libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""##Loading Datasets"""

df=pd.read_csv("/content/Movie_collection_train.csv")
df

"""##Data preprocessing

####EDD (Extended Data Dictionary)
"""

df.describe()

"""###Outliers detection and Treatment"""

plt.scatter(df.Marketin_expense,df.Collection)
plt.xlabel('marketing expenses')

plt.scatter(df.Twitter_hastags,df.Collection)
plt.xlabel('Twitter_hastags')

uv=np.percentile(df.Twitter_hastags,[99])[0]
df.Twitter_hastags[df.Twitter_hastags>3*uv]=3*uv

#EDD after outliers treatment
df.describe()

"""###Detecting and imputing missing values"""

#detecting the number of missing value in a particular column
df.isna().sum()

#Imputation of missing values
df.Time_taken=df.Time_taken.fillna(df.Time_taken.mean())

"""###Variable Transformation"""

df.Marketin_expense=np.log(1+df.Marketin_expense)
plt.scatter(df.Marketin_expense,df.Collection)
plt.xlabel('marketing expenses')

"""###Deletion of unnecessary variables"""

del df['MPAA_film_rating']

"""##Handling qualitative data
###Dummy variable creation:
"""

df=pd.get_dummies(df)
df.head()

#delete unnecessary columns
del df['3D_available_NO']

del df['Genre_Action']

"""##Correlation Analysis"""

df.corr()

"""from the correlation analysis, we can see that the feature which is atmost correlated with the 'collection'(target) is 'Budget'.

##Simple Linear regression
"""

from sklearn.linear_model import LinearRegression
lr=LinearRegression()
y=df['Collection']
x=df[['Budget']]
lr.fit(x,y)
regression_line=lr.predict(x)
print(lr.intercept_,lr.coef_)

plt.scatter(x,y)
plt.plot(x,regression_line,color='red',linewidth=4)
plt.xlabel('Budget')
plt.ylabel('collection')

"""##Multiple Linear Regression"""

x_multi=df.drop("Collection",axis=1)
x_multi.head()

y_multi=df['Collection']

#model taining without splitting
lr.fit(x_multi,y_multi)
print(lr.intercept_,lr.coef_)

#Splitting the datainto train and test data
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x_multi,y_multi,test_size=0.2,random_state=0)

#model training and prediction for test data
lr.fit(x_train,y_train)
y_pred_test=lr.predict(x_test)
y_pred_test

#prediction for train data
y_pred_train=lr.predict(x_train)
y_pred_train

#Accuracy of the model using r square method
from sklearn.metrics import r2_score
r2_score(y_test,y_pred_test)

r2_score(y_train,y_pred_train)

"""##Linear models other than OLS (Ordinary least squares)

####Standardization of data
"""

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
x_train_s=sc.fit_transform(x_train)
x_test_s=sc.fit_transform(x_test)

"""##Shrinkage methods:
###1.Ridge
"""

from sklearn.linear_model import Ridge
rd=Ridge(alpha=0.5)
rd.fit(x_train_s,y_train)
y_pred_s=rd.predict(x_test_s)
y_pred_s

#accuracy 
r2_score(y_test,y_pred_s)

"""To find the alpha value for which r^2 value is maximum, we use validation curve"""

from sklearn.model_selection import validation_curve

param_range=np.logspace(-2,8,100)
param_range

train_score,test_score=validation_curve(Ridge(),x_train_s,y_train,param_name="alpha",param_range=param_range,scoring='r2')

print(train_score)
print(test_score)

test_mean=np.mean(test_score, axis=1)
train_mean=np.mean(train_score,axis=1)

max(test_mean)

plt.scatter(x=np.log(param_range),y=test_mean)

#to find the loction of max test_mean in param_range
np.where(test_mean==max(test_mean))

param_range[35]

"""####Model training using the best alpha value for greater accuracy"""

#model training using ridge
rd_best=Ridge(alpha=param_range[35])
rd_best.fit(x_train_s,y_train)

#prediction
r2_score(y_test,rd_best.predict(x_test_s))

r2_score(y_train,rd_best.predict(x_train_s))

"""###2.Lasso"""

from sklearn.linear_model import Lasso
ls=Lasso(alpha=0.4)
ls.fit(x_train_s,y_train)

"""To find the alpha value for which r^2 value is maximum, we use validation curve"""

train_lsc,test_lsc=validation_curve(Lasso(),x_train_s,y_train,param_name='alpha',param_range=param_range,scoring='r2')
train_ls_mean=np.mean(train_lsc,axis=1)
test_lsc_mean=np.mean(test_lsc,axis=1)

max(test_lsc_mean)

plt.scatter(x=np.log(param_range),y=test_lsc_mean)

np.where(test_lsc_mean==max(test_lsc_mean))

param_range[44]

#model training using Lasso
ls_best=Lasso(alpha=param_range[44])
ls_best.fit(x_train_s,y_train)

#model testing/prediction
r2_score(y_test,ls_best.predict(x_test_s))

r2_score(y_train,ls_best.predict(x_train_s))