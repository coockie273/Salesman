import random
import math
import matplotlib.pyplot as plt
import multiprocessing
import time


def dist(x1, y1, x0, y0):
    return math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


class Population:

    def __init__(self, power, iterations, p_kross, p_mut, cities):
        self.power = power
        self.iterations = iterations
        self.cities = cities
        self.population = []
        self.N = len(cities)
        self.p_kross = p_kross
        self.p_mut = p_mut

        for i in range(power):
            route = [0]
            for j in range(1, self.N):
                route.append(random.randint(0, self.N - j - 1))
            self.population.append(route)

    def decode_route(self, route):
        numbers = []
        for i in range(len(self.cities)):
            numbers.append(i)
        new_route = []
        for i in range(0, self.N):
            new_route.append(numbers[route[i]])
            numbers.remove(numbers[route[i]])
        return new_route

    def encode_route(self, route):

        numbers = []
        for i in range(len(self.cities)):
            numbers.append(i)

        new_route = []

        for i in range(len(route)):
            number = numbers.index(route[i])
            new_route.append(number)
            numbers.remove(route[i])

        return new_route

    def dist_route(self, route):
        numbers = []
        for i in range(89):
            numbers.append(i)
        sum = 0
        current_city = self.cities[numbers[route[0]]]
        numbers.remove(numbers[route[0]])
        for i in range(1, self.N):
            city = self.cities[numbers[route[i]]]
            sum += dist(city[0], city[1], current_city[0], current_city[1])
            current_city = city
            numbers.remove(numbers[route[i]])
        return sum

    def dist_route_without_recover(self, route):
        sum = 0
        current_city = self.cities[route[0]]
        for i in range(1, len(route) - 1):
            city = self.cities[route[i]]
            sum += dist(city[0], city[1], current_city[0], current_city[1])
            current_city = city
        return sum

    def reproduction(self):
        sum = 0

        for individual in self.population:
            sum += 1 / self.dist_route(individual)

        probabilities = []

        for individual in self.population:
            probabilities.append((1 / self.dist_route(individual)) / sum)

        new_population = random.choices(self.population, probabilities, k=self.power)

        self.population = new_population

    def crossover(self):
        #start_time = time.time()
        pairs = []

        for i in range(0, len(self.population) - 1, 2):
            random_number = random.random()
            if random_number < self.p_kross:
                pairs.append((i, self.population[i], self.population[i + 1]))
        pool = multiprocessing.Pool(processes=8)

        results = pool.map(self.crossover_worker, [pair for pair in pairs])
        pool.close()
        pool.join()
        for res in results:
            self.population[res[0]] = res[1]
            self.population[res[0]] = res[2]
        #print("cross time:", time.time() - start_time)

    def crossover_worker(self, pair):
        index, individual1, individual2 = pair

        k = random.randint(0, len(individual1) - 1)
        for i in range(k, len(individual1)):
            c = individual1[i]
            individual1[i] = individual2[i]
            individual2[i] = c
        route1 = self.optimization_2opt(self.decode_route(individual1))
        route2 = self.optimization_2opt(self.decode_route(individual2))

        individual1 = self.encode_route(route1)
        individual2 = self.encode_route(route2)

        return index, individual1, individual2,

    def optimization_2opt(self, route):
        best_route = route.copy()
        best_distance = self.dist_route_without_recover(best_route)
        improvement = True
        while improvement:
            improvement = False
            for i in range(1, self.N - 1):
                for j in range(i + 1, self.N):
                    if j - i == 1:
                        continue  # Пропустить соседние вершины
                    new_tour = route[:i] + route[i:j][::-1] + route[j:]
                    new_distance = self.dist_route_without_recover(new_tour)

                    if new_distance < best_distance:
                        best_route = new_tour.copy()
                        best_distance = new_distance
                        improvement = True

        return best_route

    def mutation(self, p):
        start_time = time.time()
        pool = multiprocessing.Pool(processes=8)

        individuals = []

        for i in range(len(self.population)):
            random_number = random.random()
            if random_number < self.p_mut:
                individuals.append((i, self.population[i]))
        results = pool.map(self.mutation_worker, [inv for inv in individuals])

        pool.close()
        pool.join()
        for res in results:
            self.population[res[0]] = res[1]
        print("mutation time:", time.time() - start_time)

    def mutation_worker(self, individual):
        index, inv = individual
        k = random.randint(1, self.N - 1)
        n = random.randint(0, self.N - 1 - k)
        for i in range(k, k + n):
            inv[i] = random.randint(0, self.N - i - 1)

        route1 = self.optimization_2opt(self.decode_route(inv))
        return index, self.encode_route(route1)
    def start(self):
        for i in range(0, self.iterations):
            start_time = time.time()
            print(i)
            values = []
            for i in self.population:
                values.append(self.dist_route(i))
            min_value = min(values)
            print(min_value)
            self.reproduction()
            self.crossover()
            self.mutation(self.p_mut)
            end_time = time.time()
            print(end_time - start_time)
        values = []
        for i in self.population:
            values.append(self.dist_route(i))
        min_value = min(values)
        return min_value, self.population[values.index(min_value)]

    def draw(self):
        values = []
        for i in self.population:
            values.append(self.dist_route(i))
        min_value = min(values)
        route = self.population[values.index(min_value)]
        numbers = []
        for i in range(len(self.cities)):
            numbers.append(i)
        x = []
        y = []
        for i in range(0, len(route)):
            x.append(self.cities[numbers[route[i]]][0])
            y.append(self.cities[numbers[route[i]]][1])
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

