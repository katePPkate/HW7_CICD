import numpy as np
import pandas as pd
import pickle
import os
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# DummyClassifier
model = DummyClassifier(strategy='stratified', random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f'Точность STABLE модели (DummyClassifier): {accuracy:.2f}')

# Сохранение модели
os.makedirs("models", exist_ok=True)
with open("models/stable_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("STABLE модель сохранена в models/stable_model.pkl")
