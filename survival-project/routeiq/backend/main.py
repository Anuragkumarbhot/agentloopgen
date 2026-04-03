from fastapi import FastAPI
from itertools import permutations

app = FastAPI()

# Simple in-memory distance map
distance_map = {
    ("Mumbai", "Pune"): 150,
    ("Pune", "Nashik"): 210,
    ("Mumbai", "Nashik"): 170,
}


def get_distance(city1, city2):
    if (city1, city2) in distance_map:
        return distance_map[(city1, city2)]

    if (city2, city1) in distance_map:
        return distance_map[(city2, city1)]

    return 999999


@app.get("/")
def home():
    return {"message": "RouteIQ API running inside phone"}


@app.post("/optimize")
def optimize(cities: list[str]):

    shortest_distance = float("inf")
    shortest_route = None

    for route in permutations(cities):

        total = 0

        for i in range(len(route) - 1):

            total += get_distance(
                route[i],
                route[i + 1],
            )

        total += get_distance(
            route[-1],
            route[0],
        )

        if total < shortest_distance:

            shortest_distance = total
            shortest_route = route + (route[0],)

    return {
        "route": shortest_route,
        "distance": shortest_distance,
    }
