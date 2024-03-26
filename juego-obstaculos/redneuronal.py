import numpy as np
import tensorflow as tf

# Cargar datos desde el archivo de texto
def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            entry = list(map(int, line.strip().split(',')))
            data.append(entry)
    return np.array(data)

# Dividir datos en características (X) y etiquetas (y)
def preprocess_data(data):
    X = data[:, :2]  # Posición del jugador y del obstáculo
    y = data[:, 2]   # Altura del obstáculo
    return X, y

# Cargar los datos recolectados
data = load_data('obstacle_data.txt')

# Preprocesar los datos
X, y = preprocess_data(data)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test = X[:int(0.8*len(X))], X[int(0.8*len(X)):]
y_train, y_test = y[:int(0.8*len(y))], y[int(0.8*len(y)):]

# Construir el modelo de red neuronal
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
