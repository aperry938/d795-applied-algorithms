# Emergency Ambulance Dispatch Optimization

Graph-based ambulance dispatch system comparing Dijkstra's algorithm (single-source shortest path) against Floyd-Warshall (all-pairs precomputation) for emergency response routing.

## Overview

This project models a city's road network as a weighted directed graph and simulates an ambulance dispatch system that assigns the nearest available ambulance to each incoming emergency call. Two prototypes implement different shortest-path strategies:

**Prototype 1 (Dijkstra):** Computes the shortest path on demand for each ambulance-to-call pair. Each dispatch triggers multiple single-source queries, making it responsive but computationally repetitive across calls.

**Prototype 2 (Floyd-Warshall):** Precomputes all-pairs shortest paths in O(V^3) time, then answers each dispatch query with O(1) matrix lookup. The upfront cost pays off when processing many calls on the same network, reducing per-query latency by orders of magnitude.

Both prototypes process a priority queue of emergency calls (sorted by call type severity) and output identical dispatch logs, enabling direct performance comparison.

## Key Techniques

- Weighted directed graph with adjacency list representation
- Dijkstra's algorithm with min-heap priority queue (O((V+E) log V) per query)
- Floyd-Warshall all-pairs shortest paths (O(V^3) precomputation, O(1) lookup)
- Priority-based call dispatching with heapq
- Performance instrumentation with `time.perf_counter`

## Project Structure

```
d795-applied-algorithms/
├── dijkstra_dispatch.py               — Dijkstra-based dispatch (on-demand shortest paths)
├── floyd_warshall_dispatch.py               — Floyd-Warshall-based dispatch (precomputed matrix)
└── data/
    ├── location_network.csv    — Road network: start, end, travel time, traffic delay
    ├── calls.csv               — Emergency calls: ID, location, call type
    ├── call_priority.csv       — Call type → priority mapping
    └── ambulance.csv           — Ambulance IDs and staging locations
```

## Algorithm Comparison

| Aspect               | Dijkstra (Prototype 1)       | Floyd-Warshall (Prototype 2) |
|-----------------------|------------------------------|------------------------------|
| Precomputation        | None                         | O(V^3)                       |
| Per-query complexity  | O((V+E) log V)               | O(1) matrix lookup           |
| Space complexity      | O(V) per query               | O(V^2) distance matrix       |
| Best for              | Sparse queries, dynamic graphs | Many queries, static graphs |

For a static road network with many incoming calls, Floyd-Warshall's precomputation cost is amortized across all dispatches, making it the more efficient choice. Dijkstra is preferable when the graph changes frequently or only a few queries are needed.

## How to Run

### Prerequisites
Python 3 (standard library only — no external dependencies).

### Run Simulations
```bash
# Prototype 1: Dijkstra-based dispatch
python dijkstra_dispatch.py

# Prototype 2: Floyd-Warshall-based dispatch
python floyd_warshall_dispatch.py
```

Each prototype outputs a dispatch log CSV (`ambulance_call_log_dijkstra.csv` / `ambulance_call_log_floyd_warshall.csv`) and prints the total time spent in pathfinding.

## Dataset

Synthetic city road network with weighted edges (travel time + traffic delay), emergency call records, and ambulance staging locations. All data in CSV format under `data/`.

## Author

Anthony Perry — M.S. Computer Science, Western Governors University
