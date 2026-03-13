# 🔷 PathFinder — Node Network Visualizer

A shortest-path visualization and CLI tool built around **Dijkstra's Algorithm**, capable of finding optimal routes between nodes in a weighted graph — optimized by **distance**, **time**, or **fuel consumption**.

---

## 📁 Project Files

| File | Description |
|---|---|
| `index.html` | Interactive browser-based graph visualizer |
| `pathfinder.py` | Python CLI tool for shortest-path computation |
| `sample_nodes.csv` | Sample CSV dataset (auto-generated via `--sample`) |

---

## 🚀 Getting Started

### Web Interface (index.html)

Simply open `index.html` in any modern browser — no server or installation required.

1. Upload a CSV file using the drag-and-drop area
2. Select a **From Node** and **To Node**
3. Choose your optimization metric: **Distance**, **Time**, or **Fuel**
4. Click **▶ Find Shortest Path** to visualize the result

### Python CLI (pathfinder.py)

**Requirements:** Python 3.7+, no external libraries needed.

```bash
# Generate a sample CSV
python pathfinder.py --sample

# Find shortest path by distance (default)
python pathfinder.py --file sample_nodes.csv --from IMUS --to SILANG

# Optimize by time
python pathfinder.py --file sample_nodes.csv --from IMUS --to GENTRI --metric time

# Optimize by fuel
python pathfinder.py --file sample_nodes.csv --from IMUS --to GENTRI --metric fuel

# Compute all-pairs shortest paths
python pathfinder.py --file sample_nodes.csv --all-pairs --metric distance
```

---

## 📄 CSV Format

The CSV file must include at minimum a **From** and **To** column. Distance, Time, and Fuel columns are optional but recommended.

```csv
From Node,To Node,Distance (km),Time (mins),Fuel (liters)
IMUS,BACOOR,10,15,1.2
BACOOR,DASMA,12,25,1.5
...
```

**Column detection is flexible** — the parser recognizes variations like `from`, `From Node`, `FROM`, `dist`, `Distance (km)`, `time`, `Time (mins)`, `fuel`, etc. Both comma (`,`), semicolon (`;`), and tab-delimited files are supported.

> ⚠️ All edges are treated as **bidirectional** (undirected graph).

---

## ⚙️ Algorithm Used — Dijkstra's Algorithm

Both the web and Python implementations use **Dijkstra's Algorithm** to find the shortest (minimum-cost) path between two nodes in a weighted, undirected graph.

### How it works:

1. **Initialize** all node distances to infinity, except the start node (cost = 0)
2. **Push** the start node into a priority queue (min-heap)
3. **Pop** the lowest-cost node from the queue
4. **Relax** all neighboring edges — if a cheaper path to a neighbor is found, update and re-enqueue it
5. **Repeat** until the destination node is reached or the queue is exhausted
6. **Reconstruct** the path by backtracking through a `prev` map from end to start

### Complexity:
- **Time:** O((V + E) log V) with a binary heap
- **Space:** O(V + E)

### Metric flexibility:
The weight used during edge relaxation is swappable at runtime:
- `distance` → minimize total kilometers
- `time` → minimize total travel minutes
- `fuel` → minimize total fuel liters consumed

---

## 🖥️ Web Visualizer Features

- **Interactive canvas** — pan (drag) and zoom (scroll wheel or buttons)
- **Node hover tooltips** — shows connection count per node
- **Path highlighting** — shortest path edges rendered in green, start/end nodes distinctly colored
- **Edge table** — lists all edges with path-edge highlighting
- **Result stats** — displays total distance, time, and fuel for the found path
- **Flexible CSV parser** — handles quoted fields, BOM characters, CRLF line endings, and multiple delimiter types

---

## 🐍 Python CLI Features

- **Colorized terminal output** using ANSI escape codes
- **All-pairs mode** (`--all-pairs`) — computes shortest paths between every pair of nodes
- **Sample generator** (`--sample`) — writes a ready-to-use `sample_nodes.csv`
- **Graceful error handling** — missing files, invalid nodes, disconnected graphs

---

## 📊 Sample Dataset

The built-in sample dataset models a road network of municipalities in **Cavite, Philippines**:

```
IMUS ↔ BACOOR ↔ DASMA ↔ KAWIT ↔ INDANG ↔ SILANG ↔ GENTRI ↔ NOVELETA ↔ IMUS
(plus several cross-connections)
```

Generate it with:
```bash
python pathfinder.py --sample
```

---

## 🧩 Challenges Faced

### 1. Robust CSV Parsing (Web)
Real-world CSV files vary widely — different delimiters, quoted fields, byte-order marks (BOM), Windows line endings (`\r\n`), and inconsistent header naming. A custom quoted-field-aware parser was written from scratch in JavaScript to handle all of these cases without any external library, using a character-by-character scan with quote-tracking state.

### 2. Flexible Column Detection
Headers like `"Distance (km)"`, `"dist"`, `"KM"`, and `"distance"` should all resolve to the same column. A multi-strategy resolver was implemented: it tries exact match → `startsWith` → `includes`, using normalized (lowercased, punctuation-stripped) header strings. Extra care was taken so that `"from"` and `"to"` don't collide with each other due to substring matching (longer keys are tried first).

### 3. Graph Rendering & Layout
Placing nodes visually without coordinate data required an automatic circular layout algorithm. Nodes are evenly distributed around a circle scaled to the canvas size. The renderer supports real-time pan/zoom using an affine transform (translate + scale), with mouse-to-world coordinate projection for accurate hover detection even after transformation.

### 4. Priority Queue in JavaScript
JavaScript has no built-in heap/priority queue. The web implementation uses an array sorted each iteration (`pq.sort()`), which is O(E log E) per sort. For the scale of typical route datasets this is acceptable, but for very large graphs the Python version's `heapq` module provides a true O(log n) min-heap.

### 5. Undirected vs. Directed Edges
The CSV format specifies edges as pairs (A → B), but roads are typically bidirectional. Both implementations explicitly add edges in both directions when loading, ensuring Dijkstra can traverse the graph freely regardless of the order rows appear in the CSV.

---

## 👤 Author Notes

This project was designed to be self-contained and dependency-free:
- The **web version** runs entirely in-browser with zero npm packages
- The **Python version** uses only the standard library (`csv`, `heapq`, `argparse`, `collections`)

This makes deployment trivial — share the HTML file or the Python script and it works out of the box.

The Issue: (Brief Explanation)
I was challenged when the CSV file is not uploading. The upload button did nothing when a CSV was selected, also the browser are blocking the external files like HTML, CSS, and JS. Separated files are breaking the website so I put them inline with HTML to prevent it from doing so. 