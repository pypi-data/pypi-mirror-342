# ml_exam_codes/codes.py
"""
Module containing ML code snippets for exam preparation.
Call show_code(index) to display a code snippet by index (1 to 10).
"""

ML_CODES = {
    1: """
# Linear Regression Example
import numpy as np
from sklearn.linear_model import LinearRegression
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])
model = LinearRegression()
model.fit(X, y)
print(f'Slope: {model.coef_}, Intercept: {model.intercept_}')
""",
    2: """
# Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
iris = load_iris()
X, y = iris.data, iris.target
clf = DecisionTreeClassifier(max_depth=3)
clf.fit(X, y)
print(f'Accuracy: {clf.score(X, y)}')
""",
    3: """
# K-Means Clustering
from sklearn.cluster import KMeans
import numpy as np
X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
kmeans = KMeans(n_clusters=2, random_state=0)
kmeans.fit(X)
print(f'Cluster centers: {kmeans.cluster_centers_}')
""",
    # Placeholder for codes 4 to 10 (replace with your actual code)
    4: "# SVM Example\n# Replace with your SVM code",
    5: "# Random Forest Example\n# Replace with your Random Forest code",
    6: "# Logistic Regression Example\n# Replace with your Logistic Regression code",
    7: "# KNN Example\n# Replace with your KNN code",
    8: "# Naive Bayes Example\n# Replace with your Naive Bayes code",
    9: "# Gradient Boosting Example\n# Replace with your Gradient Boosting code",
    10: "# Neural Network Example\n# Replace with your Neural Network code"
}

def show_code(index):
    """
    Display the ML code snippet for the given index (1 to 10).
    
    Args:
        index (int): Index of the code snippet (1 to 10).
    
    Returns:
        str: The code snippet as a string, or an error message if index is invalid.
    """
    if index not in ML_CODES:
        return f"Error: Invalid index {index}. Please choose between 1 and 10."
    code = ML_CODES[index].strip()
    print(code)  # Display the code
    return code
