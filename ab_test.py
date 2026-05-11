import numpy as np
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from scipy.stats import fisher_exact
from statsmodels.stats.proportion import proportions_ztest

# Загрузка данных
iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Загрузка моделей
with open("models/stable_model.pkl", "rb") as f:
    model_A = pickle.load(f)

with open("models/new_model.pkl", "rb") as f:
    model_B = pickle.load(f)

# Предсказания
y_pred_A = model_A.predict(X_test)
y_pred_B = model_B.predict(X_test)

# Подсчёт правильных ответов
cm_A = confusion_matrix(y_test, y_pred_A)
correct_A = cm_A.trace()
incorrect_A = cm_A.sum() - correct_A

cm_B = confusion_matrix(y_test, y_pred_B)
correct_B = cm_B.trace()
incorrect_B = cm_B.sum() - correct_B

print(f"Модель A (stable): верных {correct_A}, неверных {incorrect_A}")
print(f"Модель B (canary): верных {correct_B}, неверных {incorrect_B}")

# Статистический тест
contingency_table = [[correct_A, incorrect_A],
                     [correct_B, incorrect_B]]

odds_ratio, p_value = fisher_exact(contingency_table, alternative='two-sided')
print(f"P-значение: {p_value:.6f}")

alpha = 0.05
if p_value < alpha:
    print("Есть статистически значимая разница между моделями.")
else:
    print("Статистически значимой разницы нет.")

# Последовательный тест
group_a = (y_pred_A == y_test).astype(int)
group_b = (y_pred_B == y_test).astype(int)

n_a = len(group_a)
n_b = len(group_b)
successes_a = np.sum(group_a)
successes_b = np.sum(group_b)

from statsmodels.stats.proportion import proportions_ztest
stat, p_value2 = proportions_ztest([successes_a, successes_b], [n_a, n_b])

if p_value2 < alpha:
    print(f"Тест остановлен: различия обнаружены (p-value = {p_value2:.6f})")
else:
    print(f"Тест продолжается: различия не обнаружены (p-value = {p_value2:.6f})")
