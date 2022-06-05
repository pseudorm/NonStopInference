import numpy as np

from nonstopinference.block import SklearnBlock
from sklearn.linear_model import LinearRegression


def test_not_fit_excepted():
    linr = LinearRegression()
    block = SklearnBlock("linear_regression", linr)

    X = np.random.normal(size=(3, 3))
    y = np.random.normal(size=(3,))

    linr.fit(X, y)

    print(block.predict(X))


test_not_fit_excepted()
