import heapq
import time
import matplotlib.pyplot as plt
import random

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, u, v, weight):
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        self.adjacency_list[u].append((v, weight))
        self.adjacency_list[v].append((u, weight))  # Assuming undirected graph

# Iterative Dijkstra
def dijkstra_iterative(graph, start):
    distances = {vertex: float('infinity') for vertex in graph.adjacency_list}
    distances[start] = 0
    priority_queue = [(0, start)]  # (distance, vertex)

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph.adjacency_list[current_vertex]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# Recursive Dijkstra
def dijkstra_recursive_fixed(graph, start):
    distances = {vertex: float('infinity') for vertex in graph.adjacency_list}
    distances[start] = 0
    priority_queue = [(0, start)]  # (distance, vertex)

    def visit():
        if not priority_queue:
            return
        current_distance, current_vertex = heapq.heappop(priority_queue)
        for neighbor, weight in graph.adjacency_list[current_vertex]:
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor))
        visit()

    visit()
    return distances

# Menghubungkan dataset dengan edge
def connect_datasets(graph, nodes):
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            weight = random.randint(1, 50)  # Bobot acak antara node
            graph.add_edge(nodes[i], nodes[j], weight)

# Membuat dataset khusus
def create_custom_dataset():
    graph = Graph()
    nodes = [
        "Sate Martawi (Cilacap)",
        "BOSTEAK (Cilacap)",
        "RM Sidoroso (Cilacap)",
        "Sambel Layah (Cilacap)",
        "Lesehan Ikan Bakar 70 (Cilacap)",
        "Table Nine Kitchen (Purwokerto)",
        "Gubug Makan Mang Engking (Purwokerto)",
        "Level Up (Purwokerto)",
        "Eco 21 (Purwokerto)",
        "Soto Sutrisno (Purwokerto)"
    ]
    connect_datasets(graph, nodes)
    return graph

# Menampilkan graph
def print_graph_details(graph):
    print("Detail graph (asal, tujuan, jarak):")
    for u, neighbors in graph.adjacency_list.items():
        for v, weight in neighbors:
            print(f"{u} -> {v}, Jarak: {weight}")

# Main program
if __name__ == "__main__":
    datasets = {}
    for i in range(1, 11):  # Membuat 10 dataset acak
        datasets[i] = Graph()
        num_nodes = random.randint(5, 10)
        nodes = [f"Node_{j}" for j in range(1, num_nodes + 1)]
        connect_datasets(datasets[i], nodes)

    # Menambahkan dataset khusus
    datasets[11] = create_custom_dataset()

    while True:
        print("\n=== Pilih Dataset untuk Dijalankan ===")
        print("Dataset yang tersedia:")
        for i in range(1, 12):
            print(f"{i}: {'Custom Dataset' if i == 11 else f'Dataset {i}'}")
        print("Ketik 0 untuk keluar.")

        choice = int(input("Masukkan pilihan dataset: "))
        if choice == 0:
            print("Program berhenti. Terima kasih telah menggunakan aplikasi ini!")
            break
        if choice not in datasets:
            print("Pilihan tidak valid. Silakan coba lagi.")
            continue

        graph = datasets[choice]
        print(f"\nMenampilkan dataset {choice}...\n")
        print_graph_details(graph)

        results = []
        nodes = list(graph.adjacency_list.keys())
        for _ in range(5):  # Melakukan 5 pencarian secara acak
            start_location, end_location = random.sample(nodes, 2)

            time_iterative = measure_time(graph, start_location, dijkstra_iterative)
            time_recursive = measure_time(graph, start_location, dijkstra_recursive_fixed)

            results.append((start_location, end_location, time_iterative, time_recursive))

        print("\nHasil Pencarian:")
        for start_location, end_location, time_iterative, time_recursive in results:
            print(f"Iteratif: Lokasi ditemukan: {{'awal': '{start_location}', 'akhir': '{end_location}'}} Waktu: {time_iterative:.6f} detik")
            print(f"Rekursif: Lokasi ditemukan: {{'awal': '{start_location}', 'akhir': '{end_location}'}} Waktu: {time_recursive:.6f} detik\n")
