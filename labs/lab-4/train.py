import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from model import create_model

data = pd.read_csv('data/data.csv')
X = data[['feature1', 'feature2']]
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = create_model()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
