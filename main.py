from Algorithms.Population import Population
from Algorithms.AntSystem import AntSystem
import math


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

n = len(cities)
cities_matrix = [[0 for _ in range(n)] for _ in range(n)]

# Вычисляем расстояния между городами и заполняем матрицу
for i in range(n):
    for j in range(n):
        if i != j:
            x1, y1 = cities[i]
            x2, y2 = cities[j]
            # Вычисляем евклидово расстояние между координатами городов
            distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            cities_matrix[i][j] = distance

# Создайте данные для точек
if __name__ == "__main__":
    AntSystem(100, 500, cities_matrix, cities, 0.2, 5).start()
    # 223
    # 6238.76003872322
    #Population(2500, 1000, 0.5, 0.1, cities).start()
