"""
pathfinder.py — Travelling Salesman / Shortest Path CLI Tool
Usage:
  python pathfinder.py --file data.csv --from IMUS --to SILANG --metric distance
  python pathfinder.py --file data.csv --all-pairs --metric time
  python pathfinder.py --sample   (generates a sample CSV)
"""

import csv
import sys
import argparse
import heapq
from collections import defaultdict


# ──────────────────────────────────────────────
# GRAPH CLASS
# ──────────────────────────────────────────────
class Graph:
    def __init__(self):
        # Node set: unique node IDs
        self.nodes: set = set()
        # Edge list: preserve all edges for display and summary
        self.edges: list = []
        # Adjacency list for graph traversal (Dijkstra)
        self.adj: dict = defaultdict(list)

    def add_edge(self, from_node: str, to_node: str,
                 distance: float, time: float, fuel: float):
        """Add a bidirectional weighted edge."""
        # Normalize or validate values upstream if needed.
        self.nodes.add(from_node)
        self.nodes.add(to_node)
        self.edges.append({
            "from": from_node, "to": to_node,
            "distance": distance, "time": time, "fuel": fuel
        })

        # Undirected graph: add both directions for traversal.
        self.adj[from_node].append({"node": to_node, "distance": distance,
                                    "time": time, "fuel": fuel})
        self.adj[to_node].append({"node": from_node, "distance": distance,
                                  "time": time, "fuel": fuel})

    def dijkstra(self, start: str, end: str, metric: str = "distance"):
        """
        Dijkstra's algorithm.
        metric: "distance" | "time" | "fuel"
        Returns dict with keys: path, total_distance, total_time, total_fuel
        or None if no path exists.
        """
        INF = float("inf")
        dist = {n: INF for n in self.nodes}
        prev = {}
        dist[start] = 0

        # Priority queue: (cost, node)
        # We use heapq for efficiency, not a naive sorted list.
        pq = [(0, start)]

        while pq:
            cost, u = heapq.heappop(pq)
            if cost > dist[u]:
                continue
            if u == end:
                break
            for edge in self.adj.get(u, []):
                v = edge["node"]
                w = edge[metric]
                new_cost = dist[u] + w
                if new_cost < dist[v]:
                    dist[v] = new_cost
                    prev[v] = u
                    heapq.heappush(pq, (new_cost, v))

        if dist[end] == INF:
            # No path found between start and end in current graph
            return None

        # Reconstruct path from end back to start using prev[] map.
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = prev.get(cur)
        path.reverse()

        # Compute all totals
        total_dist = total_time = total_fuel = 0.0
        edge_lookup = {}
        for e in self.edges:
            key_ab = (e["from"], e["to"])
            key_ba = (e["to"], e["from"])
            edge_lookup[key_ab] = e
            edge_lookup[key_ba] = e

        for i in range(len(path) - 1):
            e = edge_lookup.get((path[i], path[i + 1]))
            if e:
                total_dist += e["distance"]
                total_time += e["time"]
                total_fuel += e["fuel"]

        return {
            "path": path,
            "total_distance": round(total_dist, 2),
            "total_time": round(total_time, 2),
            "total_fuel": round(total_fuel, 3),
        }


# ──────────────────────────────────────────────
# CSV LOADER
# ──────────────────────────────────────────────
def load_csv(filepath: str) -> Graph:
    """Load a CSV file into a Graph. Flexible column detection."""
    g = Graph()
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = [h.strip().lower() for h in reader.fieldnames or []]

        # Find the first header matching any of the label variants.
        def find_col(keys):
            for h in reader.fieldnames or []:
                if any(k in h.lower() for k in keys):
                    return h
            return None

        from_col  = find_col(["from"])
        to_col    = find_col(["to"])
        dist_col  = find_col(["dist", "km"])
        time_col  = find_col(["time", "min"])
        fuel_col  = find_col(["fuel", "liter"])

        if not from_col or not to_col:
            raise ValueError("CSV must contain 'From Node' and 'To Node' columns.")

        for row in reader:
            from_n = row[from_col].strip().upper()
            to_n   = row[to_col].strip().upper()
            dist   = float(row[dist_col].strip()) if dist_col else 0.0
            time   = float(row[time_col].strip()) if time_col else 0.0
            fuel   = float(row[fuel_col].strip()) if fuel_col else 0.0
            if from_n and to_n:
                g.add_edge(from_n, to_n, dist, time, fuel)
    return g


# ──────────────────────────────────────────────
# DISPLAY HELPERS
# ──────────────────────────────────────────────
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
RESET  = "\033[0m"
DIM    = "\033[2m"

def print_result(result: dict, start: str, end: str, metric: str):
    if result is None:
        print(f"{RED}✗ No path found from {start} to {end}.{RESET}")
        return

    arrow = f" {DIM}→{RESET} "
    path_str = arrow.join(f"{CYAN}{n}{RESET}" for n in result["path"])
    metric_labels = {"distance": "Distance", "time": "Time", "fuel": "Fuel"}

    print(f"\n{BOLD}{'─'*50}{RESET}")
    print(f"{BOLD}  Shortest Path  ({metric_labels[metric]} optimized){RESET}")
    print(f"{'─'*50}")
    print(f"  Route  : {path_str}")
    print(f"  Steps  : {len(result['path']) - 1} hop(s)")
    print(f"{'─'*50}")
    print(f"  {GREEN}Distance{RESET} : {result['total_distance']:>8.1f} km")
    print(f"  {YELLOW}Time    {RESET} : {result['total_time']:>8.1f} mins")
    print(f"  {CYAN}Fuel    {RESET} : {result['total_fuel']:>8.3f} liters")
    print(f"{'─'*50}\n")


def print_graph_summary(g: Graph):
    print(f"\n{BOLD}Graph Summary{RESET}")
    print(f"  Nodes : {len(g.nodes)}")
    print(f"  Edges : {len(g.edges)}")
    print(f"  Nodes : {', '.join(sorted(g.nodes))}\n")


# ──────────────────────────────────────────────
# SAMPLE CSV GENERATOR
# ──────────────────────────────────────────────
SAMPLE_DATA = [
    ("IMUS",     "BACOOR",  10, 15, 1.2),
    ("BACOOR",   "DASMA",   12, 25, 1.5),
    ("DASMA",    "KAWIT",   12, 25, 1.5),
    ("KAWIT",    "INDANG",  12, 25, 1.2),
    ("INDANG",   "SILANG",  14, 25, 1.5),
    ("SILANG",   "GENTRI",  10, 25, 1.3),
    ("GENTRI",   "NOVELETA",10, 25, 1.5),
    ("NOVELETA", "IMUS",    10, 15, 1.2),
    ("BACOOR",   "SILANG",  10, 25, 1.3),
    ("DASMA",    "SILANG",  12, 25, 1.5),
    ("SILANG",   "BACOOR",  10, 25, 1.3),
    ("NOVELETA", "BACOOR",  10, 15, 1.2),
    ("SILANG",   "KAWIT",   14, 25, 1.2),
    ("IMUS",     "NOVELETA",10, 15, 1.2),
]

def generate_sample_csv(path: str = "sample_nodes.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["From Node", "To Node", "Distance (km)", "Time (mins)", "Fuel (liters)"])
        for row in SAMPLE_DATA:
            writer.writerow(row)
    print(f"{GREEN}✓ Sample CSV written to: {path}{RESET}")


# ──────────────────────────────────────────────
# CLI ENTRY POINT
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="PathFinder — Shortest path via Dijkstra's Algorithm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pathfinder.py --sample
  python pathfinder.py --file sample_nodes.csv --from IMUS --to SILANG
  python pathfinder.py --file sample_nodes.csv --from IMUS --to GENTRI --metric fuel
  python pathfinder.py --file sample_nodes.csv --all-pairs --metric time
        """
    )
    parser.add_argument("--file",       help="Path to CSV file")
    parser.add_argument("--from",       dest="from_node", help="Start node")
    parser.add_argument("--to",         dest="to_node",   help="End node")
    parser.add_argument("--metric",     choices=["distance", "time", "fuel"],
                        default="distance", help="Optimization metric (default: distance)")
    parser.add_argument("--all-pairs",  action="store_true",
                        help="Find shortest paths between all node pairs")
    parser.add_argument("--sample",     action="store_true",
                        help="Generate a sample CSV file and exit")

    args = parser.parse_args()

    # Sample generation
    if args.sample:
        generate_sample_csv()
        return

    if not args.file:
        parser.print_help()
        sys.exit(1)

    # Load graph file and handle errors cleanly.
    try:
        g = load_csv(args.file)
    except FileNotFoundError:
        print(f"{RED}✗ File not found: {args.file}{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}✗ Error loading file: {e}{RESET}")
        sys.exit(1)

    print_graph_summary(g)

    # All-pairs mode
    if args.all_pairs:
        nodes = sorted(g.nodes)
        print(f"{BOLD}All-Pairs Shortest Paths (metric: {args.metric}){RESET}")
        print(f"{'─'*60}")
        for i, a in enumerate(nodes):
            for b in nodes[i+1:]:
                r = g.dijkstra(a, b, args.metric)
                if r:
                    path_str = " → ".join(r["path"])
                    print(f"  {a:10s} → {b:10s} | {path_str}")
                    print(f"  {'':>23} Dist:{r['total_distance']:6.1f}km  "
                          f"Time:{r['total_time']:6.0f}min  "
                          f"Fuel:{r['total_fuel']:5.2f}L")
                    print(f"  {'─'*57}")
        return

    # Single path
    if not args.from_node or not args.to_node:
        print(f"{RED}✗ Provide --from and --to nodes (or use --all-pairs).{RESET}")
        parser.print_help()
        sys.exit(1)

    start = args.from_node.strip().upper()
    end   = args.to_node.strip().upper()

    if start not in g.nodes:
        print(f"{RED}✗ Node '{start}' not found. Available: {', '.join(sorted(g.nodes))}{RESET}")
        sys.exit(1)
    if end not in g.nodes:
        print(f"{RED}✗ Node '{end}' not found. Available: {', '.join(sorted(g.nodes))}{RESET}")
        sys.exit(1)

    result = g.dijkstra(start, end, args.metric)
    print_result(result, start, end, args.metric)


if __name__ == "__main__":
    main()