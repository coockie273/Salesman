import matplotlib.pyplot as plt
import multiprocessing

from Population import Population

# Откройте файл для чтения
with open('cities.txt', 'r') as file:
    lines = file.readlines()

# Инициализируйте массив для хранения кортежей
cities = []
x = []
y = []
# Обработайте каждую строку в файле
for line in lines:
    # Разделите строку на части, используя пробел в качестве разделителя
    parts = line.split()

    # Преобразуйте строки в числа с плавающей точкой и создайте кортеж
    x = float(parts[1])
    y = float(parts[2])
    point = (x, y)

    # Добавьте кортеж в массив
    cities.append(point)
# Создайте данные для точек
if __name__ == "__main__":
    route = Population(2500, 1000, 0.5, 0.1, cities).start()
    print(route[0])
    print(route[1])
    route = route[1]
    numbers = []
    for i in range(len(cities)):
        numbers.append(i)

    x = []
    y = []
    for i in range(0, len(route)):
        x.append(cities[numbers[route[i]]][0])
        y.append(cities[numbers[route[i]]][1])
        numbers.remove(numbers[route[i]])

    x.append(x[0])
    y.append(y[0])

    # Используйте plt.scatter() для постановки точек на графике
    plt.scatter(x, y, label='Точки')

    # Используйте plt.plot() для соединения точек линией
    plt.plot(x, y, linestyle='-', color='blue', label='Линия')

    # Настройте метки осей и заголовок
    plt.xlabel('Ось X')
    plt.ylabel('Ось Y')
    plt.title('График с точками и линией')

    # Добавьте легенду
    plt.legend()

    # Отобразите график
    plt.show()