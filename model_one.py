import  matplotlib.pyplot  as  plt
import  pandas  as  pd  #Для работы с данными
import  numpy  as  np  #Для операций с массивами
import  tensorflow  as  tf  #Для работы с нейронными сетями
from  sklearn.preprocessing  import  StandardScaler  #Для стандартизации данных
from  sklearn.model_selection  import  train_test_split  #Для разделения данных на обучающую и тестовую  выборки
import matplotlib.pyplot as plt
import requests
import apimoex
from datetime import *

# Получение данных с 6 ноября 2024 года
def GetDataFromSpecificDate():
    specific_date = '2024-11-06'  # Задаем определенную дату
    today = datetime.now().isoformat()[:10]  # Берем текущую дату в формате 'YYYY-MM-DD'

    print(f'Начальная дата: {specific_date}')
    print(f'Конечная дата: {today}')

    with requests.Session() as session:
        data = apimoex.get_board_candles(session, 'SBER', start=specific_date, end=today)
        df = pd.DataFrame(data)  # Преобразование словаря data в датафрейм
        print(df.head(), '\n')  # Вывод начальных нескольких строк
        print(df.tail(), '\n')  # Вывод последних нескольких строк
        df.to_csv('./model/sber_from_specific_date.csv', index=False)

GetDataFromSpecificDate()


# Загрузка модели
loaded_model = tf.keras.models.load_model("./model/my_lstm_model.h5")

# Загрузка нового датасета
new_data = pd.read_csv('./model/sber_from_specific_date.csv')

new_data = new_data.drop(columns=["begin"]) #Удаляем солбец даты

#Убираем дробнуя часть значений в столбцах
new_data['open'] = new_data['open'].astype(int)
new_data['close'] = new_data['close'].astype(int)
new_data['high'] = new_data['high'].astype(int)
new_data['low'] = new_data['low'].astype(int)
new_data['value'] = new_data['value'].astype(int)
new_data['volume'] = new_data['volume'].astype(int)

# Предобработка данных (нормализация)
scaler = StandardScaler()
new_data_scaled = scaler.fit_transform(new_data)

# Преобразование данных в последовательности
time_steps = 5  #Длина временного ряда

def prepare_data_for_prediction(data, time_steps):
    data = data.values
    X = []
    for i in range(len(data) - time_steps + 1):
        X.append(data[i:i + time_steps])
    return np.array(X)

X_new = prepare_data_for_prediction(pd.DataFrame(new_data_scaled, columns=new_data.columns), time_steps)

# Прогнозирование
predictions = loaded_model.predict(X_new)

# Обратное преобразование
predictions_inverse = scaler.inverse_transform(np.concatenate((predictions, np.zeros((predictions.shape[0], new_data.shape[1]-1))), axis=1))[:,0]

pred_l = []
# Вывод результатов
for i, prediction in enumerate(predictions_inverse):
    print(f"Предсказанная цена открытия {i+1} дня: {prediction}")
    pred_l.append(prediction)

print(pred_l)
pred_l = list(reversed(pred_l))

tomorrow = str(pred_l[0])[:6]
week = str(pred_l[6])[:6]
month = str(pred_l[22])[:6]
quarter = str(pred_l[-1])[:6]
