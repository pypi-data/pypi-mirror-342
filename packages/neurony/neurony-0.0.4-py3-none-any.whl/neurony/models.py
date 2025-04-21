import numpy as np
from neurony.metrics import (
    mean_squared_error,
    mean_squared_error_gradient,
    cross_entropy_error,
    cross_entropy_error_gradient
)


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

            loss = compute_loss(predictions, batch_y)
            error = compute_gradient(predictions, batch_y)
            self._backward(error)
            if epoch % 1000 == 0:
                for layer in self.layers:
                    layer.learning_rate *= 0.99
                print(f"Epoch {epoch}, Loss: {loss:.6f}")

    def predict(self, x):
        return self._forward(x)