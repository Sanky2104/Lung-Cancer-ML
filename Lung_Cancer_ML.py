import pandas as pd
df = pd.read_csv("hf://datasets/nateraw/lung-cancer/survey lung cancer.csv")
df.head()
df.tail(2)
df.shape
df.columns
df.isnull().sum()
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
df_encoded = pd.get_dummies(df, columns=['GENDER'])
X = df_encoded.drop(columns=['LUNG_CANCER'])
Y = df_encoded['LUNG_CANCER']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
logReg = LogisticRegression()
logReg.fit(X_train,y_train)
y_pred = logReg.predict(X_test)
from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test, y_pred)
print(acc)
import pickle
with open('logistic_regression_model.pkl', 'wb') as f:
    pickle.dump(logReg, f)