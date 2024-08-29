import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#loading the dataset to a pandas df
df = pd.read_csv('diabetes.csv')

#printing the first 5 rows
df.head()

#no of rows and cols
df.shape

#getting the statistical measures of the df
df.describe()

#no of diabetics and non-diabetics
df['Outcome'].value_counts()

print('Before dropping duplicates: ', df.shape)
df = df.drop_duplicates()
print('After dropping duplicates: ', df.shape)

df.isnull().sum()

"""Check for missing values"""

print('No of missing values in Glucose: ', df[df['Glucose'] == 0].shape[0])
print('No of missing values in BloodPressure: ', df[df['BloodPressure'] == 0].shape[0])
print('No of missing values in SkinThickness: ', df[df['SkinThickness'] == 0].shape[0])
print('No of missing values in Insulin: ', df[df['Insulin'] == 0].shape[0])
print('No of missing values in BMI: ', df[df['BMI'] == 0].shape[0])

"""Replace missing values with mean"""

df['Glucose'] = df['Glucose'].replace(0, df['Glucose'].mean())
df['BloodPressure'] = df['BloodPressure'].replace(0, df['BloodPressure'].mean())
df['SkinThickness'] = df['SkinThickness'].replace(0, df['SkinThickness'].mean())
df['Insulin'] = df['Insulin'].replace(0, df['Insulin'].mean())
df['BMI'] = df['BMI'].replace(0, df['BMI'].mean())

df.describe()

"""Data Visualisation

Count plot
"""

import matplotlib.pyplot as plt
f, ax = plt.subplots(1,2,figsize=(10,5))
df['Outcome'].value_counts().plot.pie(explode=[0,0.1],autopct='%1.1f%%', ax=ax[0],shadow=True)
ax[0].set_title('Outcome')
ax[0].set_ylabel('')

import seaborn as sns
sns.countplot('Outcome', data=df, ax=ax[1])
ax[1].set_title('Outcome')
N, P = df['Outcome'].value_counts()
print('Negative(0) ->', N)
print('Positive(1) ->', P)

plt.grid()
plt.show()

"""Dataset is not balanced

Histogram (data is balanced or skewed)
"""

df.hist(bins=10,figsize=(10,10))
plt.show()

"""Analysing relationships bw variables

Correlation analysis
"""

#get correlations of each feature in the dataset
corr_mat = df.corr()
top_corr_features = corr_mat.index
plt.figure(figsize=(10,10))
#plot heat map
g = sns.heatmap(df[top_corr_features].corr(), annot=True, cmap='RdYlGn')

"""Split data into X and y"""

#separating the independent and dependent variables
X = df.drop(columns='Outcome', axis=1)
y = df['Outcome']
print(X.head())
print(y.head())

"""Data Standardisation - Feature Scaling"""

scaler = StandardScaler()
scaler.fit(X)
standardised_data = scaler.transform(X)
print(standardised_data)

X = standardised_data
y = df.Outcome
print(X)
print(y)

"""Split data into training and testing data"""

#80% is train, 20% is test
#random state is used to ensure a specific split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)

print(X.shape, X_train.shape, X_test.shape)

"""Classification Models

1) Logistic Regression
"""

from sklearn.linear_model import LogisticRegression
lr_model = LogisticRegression(solver='liblinear', multi_class='ovr')
lr_model.fit(X_train, y_train)

"""2) K Neighbours Classifier"""

from sklearn.neighbors import KNeighborsClassifier
knn_model = KNeighborsClassifier()
knn_model.fit(X_train, y_train)

"""3) Naive Bayes Classifier"""

from sklearn.naive_bayes import GaussianNB
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)

"""4) Support Vector Machine(SVM)"""

from sklearn.svm import SVC
svm_model = SVC()
svm_model.fit(X_train, y_train)

"""5) Decision tree"""

from sklearn.tree import DecisionTreeClassifier
dt_model = DecisionTreeClassifier()
dt_model.fit(X_train, y_train)

"""6) Random Forest"""

from sklearn.ensemble import RandomForestClassifier
rf_model = RandomForestClassifier(criterion='entropy')
rf_model.fit(X_train, y_train)

"""Predicting & Evaluating the Models"""

#make the predictions using test data for all 6 models
lr_preds = lr_model.predict(X_test)

knn_preds = knn_model.predict(X_test)

nb_preds = nb_model.predict(X_test)

svm_preds = svm_model.predict(X_test)

dt_preds = dt_model.predict(X_test)

rf_preds = rf_model.predict(X_test)

#get the accuracy of the models
print('Accuracy score of Logistic Regression:', round(accuracy_score(y_test, lr_preds) * 100, 2))
print('Accuracy score of KNN:', round(accuracy_score(y_test, knn_preds) * 100, 2))
print('Accuracy score of Naive Bayes:', round(accuracy_score(y_test, nb_preds) * 100, 2))
print('Accuracy score of SVM:', round(accuracy_score(y_test, svm_preds) * 100, 2))
print('Accuracy score of Decision Tree:', round(accuracy_score(y_test, dt_preds) * 100, 2))
print('Accuracy score of Random Forest:', round(accuracy_score(y_test, rf_preds) * 100, 2))

"""Save the Model with the Highest Accuracy using pickle"""

import pickle
pickle.dump(svm_model, open('svm_model.pkl', 'wb')) #svm has the highest accuracy

pickle.dump(scaler, open('scaler.pkl', 'wb')) #save the std scaler too