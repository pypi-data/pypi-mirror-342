import numpy as np

def mean_squared_error(predictions, targets):
    return np.mean((targets - predictions) ** 2)


def mean_squared_error_gradient(predictions, targets):
    return 2 * (predictions - targets)


def cross_entropy_error(predictions, targets):
    """
    :param predictions: предсказания модели, значения от 0 до 1 (после sigmoid)
    :param targets: целевые значения (0 или 1)

    :returns: среднюю кросс-энтропию по батчу.
    """
    epsilon = 1e-12  # чтобы избежать log(0)
    predictions = np.clip(predictions, epsilon, 1 - epsilon)
    loss = -np.mean(targets * np.log(predictions) + (1 - targets) * np.log(1 - predictions))
    return loss


def cross_entropy_error_gradient(predictions, targets):
    """
    Предполагается, что выходная активация — sigmoid.
    Градиент dL/dz для последнего слоя с sigmoid и cross-entropy:
    просто (pred - target), что упрощается из-за формулы.
    """
    return predictions - targets