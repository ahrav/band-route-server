import numpy as np, operator, random, pandas as pd


# Create necessary classes and methods for genetic algorithm


class City:
    """Class to create city objects with given x and y coordinates
        represents gene in genetic algorithm"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        """Find distance for given city"""

        x_dist = abs(self.x - city.x)
        y_dist = abs(self.y - city.y)
        distance = np.sqrt((x_dist ** 2) + (y_dist ** 2))

        return distance

    def __repr__(self):
        return f"({str(self.x)}, {str(self.y)})"


class Fitness:
    """Class for the fitness function needed for genetic algorithm
        how fast the route is"""

    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def route_distance(self):
        """Find the route distance"""

        if self.distance == 0:
            path_distance = 0
            for i in range(0, len(self.route)):
                from_city = self.route[i]
                to_city = None
                if i + 1 < len(self.route):
                    to_city = self.route[i + 1]
                else:
                    to_city = self.route[0]
                path_distance += from_city.distance(to_city)
            self.distance = path_distance

        return self.distance

    def route_fitness(self):
        """Determine fitness of given route
            inverse of distance"""

        if self.fitness == 0:
            self.fitness = 1 / float(self.route_distance())

        return self.fitness


# Create initial population


def create_route(city_list):
    """Create route given list of cities
        creating a single individual"""

    route = random.sample(city_list, len(city_list))
    return route


def create_routes(city_list, num_routes):
    """Create first list of routes (population)
        createing entire population of individuals"""

    population = []

    for i in range(0, num_routes):
        population.append(create_route(city_list))
    return population


# Create genetic algorithm.


def rank_routes(routes):
    """Rank routes by fitness and get most fit route(best)
        survival of the fittest"""

    fitness_results = {}

    for i in range(0, len(routes)):
        fitness_results[i] = Fitness(routes[i]).route_fitness()

    return sorted(
        fitness_results.items(), key=operator.itemgetter(1), reverse=True
    )


def selection_func(routes_ranked, elite_size):
    """Select most appropriate routes to 
        use and persist routes with best fitness(distance)"""

    selection_results = []
    df = pd.DataFrame(np.array(routes_ranked), columns=["Index", "Fitness"])
    df["cum_sum"] = df.Fitness.cumsum()
    df["cum_perc"] = 100 * df.cum_sum / df.Fitness.sum()

    # keep best routes, Elitism.
    for i in range(0, elite_size):
        selection_results.append(routes_ranked[i][0])

    # random selection of routes
    for i in range(0, len(routes_ranked) - elite_size):
        pick = 100 * random.random()
        for i in range(0, len(routes_ranked)):
            if pick <= df.iat[i, 3]:
                selection_results.append(routes_ranked[i][0])
                break

    return selection_results


def select_routes(routes, selection_results):
    """Extract a subset of routes via selection function
        considered the mating pool"""

    selected_routes = []

    for i in range(0, len(selection_results)):
        index = selection_results[i]
        selected_routes.append(routes[index])

    return selected_routes


def combine_route(route1, route2):
    """Combine routes together to create an extended route
        breeding with mating pool (ordered crossover)
        create single offspring"""

    child_route = []
    parent_route1 = []
    parent_route2 = []

    partial_route1 = int(random.random()) * len(route1)
    partial_route2 = int(random.random()) * len(route2)

    start_route = min(partial_route1, partial_route2)
    end_route = max(partial_route1, partial_route2)

    for i in range(start_route, end_route):
        parent_route1.append(route1[i])

    parent_route2 = [item for item in route2 if item not in parent_route1]
    child_route = parent_route1 + parent_route2

    return child_route


def combine_routes(routes, elite_size):
    """Keep best routes then use combine routes
       function to create different route combos
       create population of offspring"""

    new_routes = []
    length = len(routes) - elite_size
    pool = random.sample(routes, len(routes))

    # Keep best routes from list of routes, elitism.
    for i in range(0, elite_size):
        new_routes.append(routes[i])

    for i in range(0, length):
        new_route = combine_route(pool[i], pool[len(routes) - i - 1])
        new_routes.append(new_route)

    return new_routes


def swap_route(route, swap_rate):
    """Swap cities with each other to be able to change route combinations
        mutations in the population (due to restrictions of including all
        cities, no dropping of cities) swap_rate = mutation rate"""

    for swapped in range(len(route)):
        if random.random() < swap_rate:
            swap_with = int(random.random() * len(route))

            city1, city2 = route[swapped], route[swap_with]

            route[swapped], route[swap_with] = city2, city1

    return route


def swap_routes(routes, swap_rate):
    """Apply swap route function across all routes
        apply mutation throughout entire population"""

    swapped_routes = []

    for idx in range(0, len(routes)):
        swapped_route = swap_route(routes[idx], swap_rate)
        swapped_routes.append(swapped_route)

    return swapped_routes


def new_route(curr_route, elite_size, swap_rate):
    """Use earlier functions in order to
       create a new route to visit all points
       create a new generation"""

    # Find fit individuals
    ranked_routes = rank_routes(curr_route)
    # Potential parents
    selection_results = selection_func(ranked_routes, elite_size)
    # Create mating pool
    selected_routes = select_routes(curr_route, selection_results)
    # Breed to create new generation
    routes = combine_routes(selected_routes, elite_size)
    # Apply mutations
    new_routes = swap_routes(routes, swap_rate)

    return new_routes


def fastest_route(routes, num_routes, elite_size, swap_rate, generations):
    """Function to find fastest route to visit all cities only once"""

    route = create_routes(routes, num_routes)

    # Set generation to 50 feel free to change for more route possibilities
    for i in range(0, generations):
        route = new_route(route, elite_size, swap_rate)

    best_route_index = rank_routes(route)[0][0]
    best_route = route[best_route_index]

    return best_route
