from src.Neurony.main import MLP, InputLayer, Layer
import numpy as np

def test_and():
    print("\n=== Тест: AND ===")
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    y = np.array([[0], [0], [0], [1]])

    model = MLP([
        InputLayer(2),
        Layer(2, activation='tanh'),
        Layer(1, activation='sigmoid')
    ], learning_rate=0.1)

    model.fit(X, y, epochs=5000)
    preds = model.predict(X)
    print("Predictions:", np.round(preds, 2))
    print("Rounded:", np.round(preds))

def test_xor_relu():
    print("\n=== Тест: XOR (ReLU) ===")
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    y = np.array([[0], [1], [1], [0]])

    model = MLP([
        InputLayer(2),
        Layer(4, activation='relu'),
        Layer(1, activation='sigmoid')
    ], learning_rate=0.1)

    model.fit(X, y, epochs=10000)
    preds = model.predict(X)
    print("Predictions:", np.round(preds, 2))
    print("Rounded:", np.round(preds))
