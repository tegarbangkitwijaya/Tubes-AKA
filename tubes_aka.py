import heapq
import time
import matplotlib.pyplot as plt

class Graph:
    def _init(self):  # Perbaikan dari _init ke _init_
        self.adjacency_list = {}

    def add_edge(self, u, v, weight):
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        self.adjacency_list[u].append((v, weight))
        self.adjacency_list[v].append((u, weight))  # Assuming undirected graph

# Iterative Dijkstra with route tracking
def dijkstra_iterative_with_routes(graph, start):
    distances = {vertex: float('infinity') for vertex in graph.adjacency_list}
    distances[start] = 0
    priority_queue = [(0, start)]  # (distance, vertex)
    routes = {vertex: [] for vertex in graph.adjacency_list}  # Track routes
    routes[start] = [start]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph.adjacency_list[current_vertex]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
                routes[neighbor] = routes[current_vertex] + [neighbor]

    return distances, routes

# Recursive Dijkstra with route tracking
def dijkstra_recursive_with_routes(graph, start):
    distances = {vertex: float('infinity') for vertex in graph.adjacency_list}
    distances[start] = 0
    priority_queue = [(0, start)]  # (distance, vertex)
    routes = {vertex: [] for vertex in graph.adjacency_list}  # Track routes
    routes[start] = [start]

    def visit():
        if not priority_queue:
            return
        current_distance, current_vertex = heapq.heappop(priority_queue)

        for neighbor, weight in graph.adjacency_list[current_vertex]:
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor))
                routes[neighbor] = routes[current_vertex] + [neighbor]

        visit()

    visit()
    return distances, routes

# Measure execution time
def measure_time_with_routes(graph, start, algorithm):
    start_time = time.perf_counter()
    distances, routes = algorithm(graph, start)
    end_time = time.perf_counter()
    return end_time - start_time, distances, routes

# Main Program
if _name_ == "_main_":
    graph = Graph()

    # Graph with travel times
    graf_waktu = {
        'Warung Sate Shinta': [('Karanglewas', 15), ('Purwokerto Timur', 10), ('Banyumas', 20)],
        'Bebek Goreng H. Slamet': [('Karanglewas', 20), ('Purwokerto Barat', 15), ('Ajibarang', 25)],
        'Ayam Geprek Bensu': [('Purwokerto Timur', 15), ('Purwokerto Barat', 20), ('c', 10)],
        'Karanglewas': [('Warung Sate Shinta', 15), ('Bebek Goreng H. Slamet', 20)],
        'Purwokerto Timur': [('Warung Sate Shinta', 10), ('Ayam Geprek Bensu', 15)],
        'Purwokerto Barat': [('Bebek Goreng H. Slamet', 15), ('Ayam Geprek Bensu', 20)],
        'Banyumas': [('Warung Sate Shinta', 20), ('Sokaraja', 25)],
        'Ajibarang': [('Bebek Goreng H. Slamet', 25), ('Banyumas', 30)],
        'Sokaraja': [('Ayam Geprek Bensu', 10), ('Banyumas', 25)],
    }

    # Add edges to the graph
    for u, neighbors in graf_waktu.items():
        for v, weight in neighbors:
            graph.add_edge(u, v, weight)

    # Input locations for multiple routes
    routes_input = []
    print("Masukkan pasangan lokasi awal dan tujuan:")
    print("Format: Lokasi awal, Lokasi tujuan")
    print("Contoh: 'Warung Sate Shinta, Banyumas'")

    while True:
        user_input = input("Masukkan pasangan (atau ketik 'selesai' untuk berhenti): ").strip()
        if user_input.lower() == 'selesai':
            break
        else:
            start, end = user_input.split(",")
            routes_input.append((start.strip(), end.strip()))

    # Store execution times for plotting
    iterative_times = []
    recursive_times = []
    route_pairs = []

    for start_location, end_location in routes_input:
        if start_location not in graph.adjacency_list or end_location not in graph.adjacency_list:
            print(f"Lokasi '{start_location}' atau '{end_location}' tidak ditemukan di graf.")
            continue

        # Iterative Dijkstra
        time_iterative, distances_iter, routes_iter = measure_time_with_routes(
            graph, start_location, dijkstra_iterative_with_routes
        )
        route_iter = " -> ".join(routes_iter[end_location])
        print(f"[Iterative] Dari {start_location} ke {end_location}: {distances_iter[end_location]} menit melalui rute {route_iter} (Waktu: {time_iterative:.6f} detik)")

        # Recursive Dijkstra
        time_recursive, distances_recur, routes_recur = measure_time_with_routes(
            graph, start_location, dijkstra_recursive_with_routes
        )
        route_recur = " -> ".join(routes_recur[end_location])
        print(f"[Recursive] Dari {start_location} ke {end_location}: {distances_recur[end_location]} menit melalui rute {route_recur} (Waktu: {time_recursive:.6f} detik)")

        # Collect execution times for plotting
        iterative_times.append(time_iterative)
        recursive_times.append(time_recursive)
        route_pairs.append(f"{start_location} -> {end_location}")

    # Create line plot for execution times
    x = range(len(route_pairs))  # Indices for each route pair

    plt.plot(x, iterative_times, marker='o', label='Iteratif', color='blue', linestyle='-')
    plt.plot(x, recursive_times, marker='s', label='Rekursif', color='green', linestyle='-')

    plt.xlabel('Pasangan Lokasi')
    plt.ylabel('Waktu Eksekusi (detik)')
    plt.title('Perbandingan Waktu Eksekusi Dijkstra')
    plt.xticks(x, route_pairs, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()
