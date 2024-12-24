import  matplotlib.pyplot  as  plt
import  pandas  as  pd  #Для работы с данными
import  numpy  as  np  #Для операций с массивами
import  tensorflow  as  tf  #Для работы с нейронными сетями
from  sklearn.preprocessing  import  StandardScaler  #Для стандартизации данных
from  sklearn.model_selection  import  train_test_split  #Для разделения данных на обучающую и тестовую  выборки

df = pd.read_csv("sber.csv", parse_dates=["begin"])

df = df.drop(columns=["begin"]) #Удаляем солбец даты

#Убираем дробнуя часть значений в столбцах
df['open'] = df['open'].astype(int)
df['close'] = df['close'].astype(int)
df['high'] = df['high'].astype(int)
df['low'] = df['low'].astype(int)
df['value'] = df['value'].astype(int)
df['volume'] = df['volume'].astype(int)

#Стандартизация данных
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)

scaled_df = pd.DataFrame(scaled_features, columns=df.columns)

#Разделение датасета на тестовую и валидационную части
train_df, val_df = train_test_split(scaled_df, test_size=0.2, random_state=42, shuffle=False)

#Функция для создания последовательностей
def make_dataset(df, time_steps: int, batch_size: int):
    data = df.values
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i + time_steps])
        y.append(data[i + time_steps, 0])
    X = np.array(X)
    y = np.array(y)
    return tf.data.Dataset.from_tensor_slices((X, y)).batch(batch_size).shuffle(1000)

#Задаём значения "time_steps" и "batch_size" созданём обучающий и валидационный наборы данных
time_steps = 5
batch_size = 32
train_ds = make_dataset(train_df, time_steps, batch_size)
val_ds = make_dataset(val_df, time_steps, batch_size)

#Создаём LSTM модель
lstm_model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(time_steps, train_df.shape[1])),
    tf.keras.layers.LSTM(256, activation='tanh', return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(128, activation='tanh', return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(64, activation='tanh'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)
])

lstm_model.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=tf.optimizers.Adam(learning_rate=0.0001), metrics=['mse'])

#Обучение модели
history = lstm_model.fit(train_ds, validation_data=val_ds, epochs=150)

lstm_model.evaluate(train_ds)

lstm_model.evaluate(val_ds)

# Построение графиков точности и потерь
acc = history.history['loss']
val_acc = history.history['val_loss']
loss = history.history['mse']
val_loss = history.history['val_mse']

epochs = range(len(acc))

plt.plot(epochs, acc, 'b', label='Точность на обучении')
plt.plot(epochs, val_acc, 'r', label='Точность на тестах')
plt.title('Точность обучения и тестов')
plt.legend()

lstm_model.save("my_lstm_model.h5")