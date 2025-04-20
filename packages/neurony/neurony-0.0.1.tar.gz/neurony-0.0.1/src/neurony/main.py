import numpy as np

# Активации и их производные
def relu(x):
    return np.maximum(0, x)


def relu_derivative(x):
    return (x > 0).astype(float)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)


def tanh(x):
    return np.tanh(x)


def tanh_derivative(x):
    return 1 - np.tanh(x) ** 2


# Функция потерь и её производная
def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)


def mean_squared_error_gradient(y_true, y_pred):
    return 2 * (y_pred - y_true) / y_true.shape[0]


def cross_entropy_error(predictions, targets):
    """
    predictions: предсказания модели, значения от 0 до 1 (после sigmoid)
    targets: целевые значения (0 или 1)

    Возвращает среднюю кросс-энтропию по батчу.
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


# Слой ввода
class InputLayer:
    def __init__(self, output_size):
        self.learning_rate = 0
        self.output_size = output_size
        self.z = None

    def build(self, input_size, learning_rate):
        pass

    def forward(self, x):
        self.z = x
        return x

    def backward(self, delta):
        return delta


# Обычный слой
class Layer:
    def __init__(self, output_size, activation="tanh"):
        self.output_size = output_size
        self.activation_name = activation
        self.activation = None
        self.activation_derivative = None
        self.weights = None
        self.biases = None
        self.learning_rate = 0.1
        self.z = None

    def build(self, input_size, learning_rate):
        self.input_size = input_size
        self.learning_rate = learning_rate
        self.weights = np.random.randn(self.output_size, input_size) * np.sqrt(2 / input_size)
        self.biases = np.zeros((1, self.output_size))

        if self.activation_name == 'relu':
            self.activation = relu
            self.activation_derivative = relu_derivative
        elif self.activation_name == "sigmoid":
            self.activation = sigmoid
            self.activation_derivative = sigmoid_derivative
        elif self.activation_name == "tanh":
            self.activation = tanh
            self.activation_derivative = tanh_derivative
        else:
            raise ValueError("Unsupported activation function")

    def forward(self, x):
        self.input = x
        self.z = np.dot(x, self.weights.T) + self.biases
        return self.activation(self.z)

    def backward(self, delta, prev_activation):
        dz = delta * self.activation_derivative(self.z)
        dw = np.dot(dz.T, prev_activation) / dz.shape[0]
        db = np.mean(dz, axis=0, keepdims=True)
        self.weights -= self.learning_rate * dw
        self.biases -= self.learning_rate * db
        return np.dot(dz, self.weights)


# MLP
class MLP:
    def __init__(self, architecture, learning_rate=0.1):
        self.layers = []
        self._build(architecture, learning_rate)

    def _build(self, architecture, learning_rate):
        for i, layer in enumerate(architecture):
            input_size = architecture[i - 1].output_size if i > 0 else None
            layer.build(input_size, learning_rate)
            self.layers.append(layer)

    def batch_generator(self, x, y, batch_size=32, shuffle=True):
        """
        Бесконечный генератор для создания батчей данных.

        :param x: Признаки (матрица, где строки — примеры, а столбцы — признаки)
        :param y: Целевые значения (вектор или матрица меток)
        :param batch_size: Размер одного батча
        :param shuffle: Перемешивать ли данные перед каждым проходом
        :return: Батчи данных (x_batch, y_batch)
        """
        assert len(x) == len(y), "x и y должны быть одинаковой длины"
        num_samples = len(x)
        indices = np.arange(num_samples)

        while True:  # бесконечный цикл
            if shuffle:
                np.random.shuffle(indices)  # перемешиваем индексы

            for start_idx in range(0, num_samples, batch_size):
                end_idx = min(start_idx + batch_size, num_samples)
                batch_indices = indices[start_idx:end_idx]

                x_batch = np.array(x[batch_indices])
                y_batch = np.array(y[batch_indices])

                yield x_batch, y_batch

    def _forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def _backward(self, error):
        for i in reversed(range(1, len(self.layers))):
            error = self.layers[i].backward(error, self.layers[i - 1].z)

    def fit(self, x, y, epochs=10000, loss_function="cross_entropy", batch_size=32, learning_rate=0.1):
        for layer in self.layers:
            layer.learning_rate = learning_rate

        batches = self.batch_generator(x, y, batch_size)

        if loss_function == "cross_entropy":
            compute_loss = cross_entropy_error
            compute_gradient = cross_entropy_error_gradient
        elif loss_function == "mean_squared_error":
            compute_loss = mean_squared_error
            compute_gradient = mean_squared_error_gradient

        for epoch in range(epochs):
            batch_X, batch_y = next(batches)
            predictions = self._forward(batch_X)

            loss = compute_loss(batch_y, predictions)
            error = compute_gradient(batch_y, predictions)
            self._backward(error)
            if epoch % 1000 == 0:
                for layer in self.layers:
                    layer.learning_rate *= 0.99
                print(f"Epoch {epoch}, Loss: {loss:.6f}")

    def predict(self, x):
        return self._forward(x)
