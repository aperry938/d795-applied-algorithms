import csv
import heapq # Priority queue library
import time
# --- Part 1: Graph Representation ---
# We represent the city map as a graph where locations are vertices
# and routes are weighted edges.

class Graph:
    def __init__(self):
        # Adjacency list format: {source_node: [(destination_node, weight), ...]}
        self.adjacency_list = {}
        # Set to store all unique locations (vertices)
        self.vertices = set()

    def add_edge(self, source, destination, weight):
        """Adds a directed edge to the graph."""
        # Ensure source node exists in the adjacency list
        if source not in self.adjacency_list:
            self.adjacency_list[source] = []
        
        self.adjacency_list[source].append((destination, weight))
        # Add both source and destination to the set of vertices
        self.vertices.add(source)
        self.vertices.add(destination)

# --- Part 2: Data Loading Functions ---

def load_network_data(filename):
    """Loads network data from CSV and populates a graph object."""
    graph = Graph()
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                source = row['Start']
                destination = row['End']
                # Calculate edge weight: Travel Time + Traffic Delay
                # Convert string values to float for calculation
                travel_time = float(row['Travel Time'])
                traffic_delay = float(row['Traffic Delay'])
                weight = travel_time + traffic_delay
                
                graph.add_edge(source, destination, weight)
            except ValueError:
                print(f"Warning: Skipping row with invalid data: {row}")
    return graph

def load_call_priorities(filename):
    """Loads call priority mapping from CSV into a dictionary."""
    priorities = {}
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            priorities[row['Call Type']] = int(row['Priority'])
    return priorities

def load_ambulance_data(filename):
    """Loads initial ambulance locations."""
    ambulances = {} # {ambulance_id: current_location}
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ambulances[row['Ambulance Number']] = row['Staging Location']
    return ambulances
# --- Part 3: Algorithm Implementation (Prototype 1: Dijkstra) ---

def dijkstra_shortest_path(graph, start_node, end_node):
    """Calculates the shortest path cost from start_node to end_node using Dijkstra's algorithm."""
    
    # Priority queue stores tuples: (current_cost, current_node)
    # We use a min-heap, so the node with the smallest cost is always processed first.
    priority_queue = [(0, start_node)]
    
    # Dictionary to store the minimum cost found so far to reach each node from start_node.
    # Initialize all distances to infinity.
    distances = {vertex: float('infinity') for vertex in graph.vertices}
    distances[start_node] = 0

    while priority_queue:
        # Get the node with the smallest distance from the source so far
        current_cost, current_node = heapq.heappop(priority_queue)

        # Optimization: If we find a cost that is already larger than one we've recorded, skip it.
        if current_cost > distances[current_node]:
            continue

        # If we've reached the destination, return its cost.
        if current_node == end_node:
            return distances[end_node]

        # Explore neighbors (relaxation step)
        if current_node in graph.adjacency_list:
            for neighbor, edge_weight in graph.adjacency_list[current_node]:
                new_cost = distances[current_node] + edge_weight
                
                # If we found a shorter path to the neighbor, update it.
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    heapq.heappush(priority_queue, (new_cost, neighbor))

    # If the end_node was never reached (e.g., disconnected graph)
    return float('infinity')

# --- Part 4: Main Simulation Logic ---

def run_simulation():
    # 1. Load all data sources
    print("Loading data...")
    graph = load_network_data('data/location_network.csv')
    call_priorities = load_call_priorities('data/call_priority.csv')
    initial_ambulances = load_ambulance_data('data/ambulance.csv')
    
    # 2. Prepare call queue
    call_queue = [] # This will become our priority queue
    with open('data/calls.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            call_id = int(row['Call ID'])
            location = row['Location']
            call_type = row['Call Type']
            priority = call_priorities.get(call_type, 99) # Default to low priority if type unknown
            heapq.heappush(call_queue, (priority, call_id, row))

    print(f"Loaded {len(call_queue)} calls and {len(graph.vertices)} locations.")

    # 3. Process calls
    dispatch_log = []
    available_ambulances = initial_ambulances.copy() # Active fleet
    
    # --- Performance Counter Initialization ---
    total_algorithm_time = 0.0 

    while call_queue:
        priority, call_id, call_details = heapq.heappop(call_queue)
        call_location = call_details['Location']

        best_ambulance = None
        fastest_time = float('infinity')

        # Find best ambulance for this call
        for ambulance_id, ambulance_location in available_ambulances.items():
            # --- Start Performance Timer ---
            start_time = time.perf_counter()
            
            time_to_call = dijkstra_shortest_path(graph, ambulance_location, call_location)
            
            # --- End Performance Timer ---
            end_time = time.perf_counter()
            total_algorithm_time += (end_time - start_time) # Accumulate time spent in algorithm
            
            if time_to_call < fastest_time:
                fastest_time = time_to_call
                best_ambulance = ambulance_id

        # Log dispatch result
        if best_ambulance:
            log_entry = {
                "Call ID": call_id,
                "Call Type": call_details['Call Type'],
                "Call Location": call_location,
                "Selected Ambulance": best_ambulance,
                "Time to Call Location": round(fastest_time, 2), # Round for cleaner output
            }
            dispatch_log.append(log_entry)
        else:
            print(f"Warning: No route found for call {call_id} at {call_location}.")

    # 4. Write log file
    log_file_path = 'ambulance_call_log_p1.csv' # Changed path for clarity
    with open(log_file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["Call ID", "Call Type", "Call Location", "Selected Ambulance", "Time to Call Location"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dispatch_log)

    print(f"\nSimulation complete. Dispatch log saved to {log_file_path}")
    print(f"--- Prototype 1 Performance (Dijkstra) ---")
    print(f"Total time spent in pathfinding algorithm: {total_algorithm_time:.8f} seconds")

# --- Entry Point ---
if __name__ == "__main__":
    run_simulation()