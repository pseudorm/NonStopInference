from abc import ABC, abstractmethod
from sklearn.utils.validation import check_is_fitted
from nonstopinference.exception.base import ExceptionChain


class SklearnWrongModelTypeError(Exception):
    pass


class Block(ABC):
    def __init__(self, name, break_if_error=False):
        self.name = name
        self.break_if_error = break_if_error

    def fit(self):
        NotImplementedError

    @abstractmethod
    def imperfect_predict(self, X, exception_chain: ExceptionChain, y=None):
        """
        Inference under error, each block should have a desinated fallback
        method to either continue inferencing or break and return some default
        output.
        """
        NotImplementedError

    @abstractmethod
    def predict(self):
        """
        Method to unify both transforms and predicts
        """
        NotImplementedError


class SklearnBlock(Block):
    def __init__(self, name, model, break_if_error=False):
        super().__init__(name, break_if_error)
        self.model = model
        # if model has predict attribute, then it's a model
        # otherwise it's a transformation
        self._model_has_predict = self._check_model_has_predict()

    @property
    def model_has_predict(self):
        return self._model_has_predict

    def _check_model_has_predict(self):
        return hasattr(self.model, "predict")

    def _check_model_is_fitted(self):
        return check_is_fitted(self.model)

    def _infer(self, X):
        self._check_model_is_fitted()

        try:
            if self._model_has_predict:
                return self.model.predict(X)
            else:
                return self.model.transform(X)
        except SklearnWrongModelTypeError as e:
            raise e(
                f"Model needs to be either a predictor or a transform, got {self.model}"
            )

    def imperfect_predict(self, X, exception_chain: ExceptionChain, y=None):
        return None

    def predict(self, X):
        return self._infer(X)

