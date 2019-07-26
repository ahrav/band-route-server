import random, operator
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .tasks import City, Fitness


class TasksTests(TestCase):
    """Tests for all tasks related to genetic algorithm"""

    city1 = City(x=1, y=2)
    city2 = City(x=3, y=4)
    city3 = City(x=4, y=5)
    city_list = [city1, city2, city3]

    def test_create_route(self):
        """Test given list of cities should return randomized 
        sample of cities equal to the length of city_list"""

        route = random.sample(self.city_list, len(self.city_list))

        self.assertEqual(len(route), len(self.city_list))
        self.assertIsInstance(route[0], City)

    def test_create_initial_population(self):
        """Test being able to return list of cities randomized"""

        population = []

        for i in range(0, 3):
            population.append(self.city_list)

        self.assertEqual(len(population), 3)
        self.assertIsInstance(population[0][0], City)

    def test_rank_routes(self):
        """Test to return ordered list from highest to lowest fitness score"""

        fitness_results = {}
        population = [
            [(1, 2), (4, 5), (3, 4)],
            [(3, 4), (4, 5), (1, 2)],
            [(4, 5), (1, 2), (3, 4)],
        ]

        for i in range(0, len(population)):
            fitness_result[i] = Fitness(population[i]).route_fitness()
        result = sorted(
            fitness_results.items(), key=operator.itemgetter(1), reversed=True
        )
        self.assertEqual(len(result), len(population))
