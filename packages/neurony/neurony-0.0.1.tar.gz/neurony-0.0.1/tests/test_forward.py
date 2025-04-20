from src.Neurony.main import Layer
import numpy as np

def test_z_computing():
    # построение слоя
    l = Layer(3, activation="relu")
    l.build(5, 0.01)

    # создаем кастомные веса
    l.weights = np.array([[0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1]])
    # создаем входные данные
    x = np.array([[1, 1, 1, 1, 1]])

    ans = l.forward(x)

    assert ans.shape == (1, 3)

    assert (ans == np.array([[0.5, 0.5, 0.5]])).all()