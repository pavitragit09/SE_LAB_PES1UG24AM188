"""Campus shuttle fleet management and passenger-load analysis."""
import json
import random
from datetime import datetime

# Global state
routes = {
    "R1": {"name": "Main Gate - Library", "trips": []},
    "R2": {"name": "Hostel - Sports Complex", "trips": []},
    "R3": {"name": "Admin Block - Metro", "trips": []},
}
MIN_CAPACITY = 10


def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip and return its log entries."""
    if route_id not in routes:
        raise ValueError(f"Unknown route: {route_id}")

    if not isinstance(passenger_count, int) or isinstance(
        passenger_count, bool
    ):
        raise ValueError("Passenger count must be an integer.")

    if passenger_count < 0:
        raise ValueError("Passenger count cannot be negative.")

    if logs is None:
        logs = []

    routes[route_id]["trips"].append(passenger_count)
    logs.append(
        f"{datetime.now()}: {route_id} carried {passenger_count}"
    )
    return logs


def remove_route(route_id):
    """Remove a route if it exists."""
    if route_id not in routes:
        raise ValueError(f"Unknown route: {route_id}")
    del routes[route_id]


def average_load(route_id):
    """Calculate the average passenger count for a route."""
    if route_id not in routes:
        raise ValueError(f"Unknown route: {route_id}")

    trips = routes[route_id]["trips"]
    if not trips:
        return 0.0

    return sum(trips) / len(trips)


def underused_routes():
    """Return routes with average passenger counts below capacity."""
    flagged = []
    for route_id in routes:
        if average_load(route_id) < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged


def assign_driver(route_id):
    """Assign a driver to a valid route."""
    if route_id not in routes:
        raise ValueError(f"Unknown route: {route_id}")

    drivers = ["Prakash", "Leela", "Imran", "Tom"]
    return drivers[0]


def sync_fleet_data(file="fleet.json"):
    """Save fleet data and reload it into the existing routes dictionary."""
    with open(file, "w", encoding="utf-8") as fleet_file:
        json.dump(routes, fleet_file, indent=2)

    with open(file, "r", encoding="utf-8") as fleet_file:
        loaded_routes = json.load(fleet_file)

    routes.clear()
    routes.update(loaded_routes)

def main():
    """Run the campus shuttle demonstration."""
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)

    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))

    sync_fleet_data()
    remove_route("R3")

    choice = input("Route to look up (Enter for R2): ").strip() or "R2"

    if choice not in routes:
        print(f"Route {choice} does not exist.")
        return

    print("Trips on", choice, ":", routes[choice]["trips"])


if __name__ == "__main__":
    main()
