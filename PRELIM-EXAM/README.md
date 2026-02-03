# AlgoMetric Benchmark Pro

A desktop performance-benchmarking tool for classic sorting algorithms. Load any CSV, choose an algorithm and a column, and watch a live progress bar while precise timing metrics stream into the log terminal. Export the sorted result with one click.

---

## Features

- **Live progress updates** — Bubble Sort and Insertion Sort report every pass/row in real time; the UI is throttled to 200 ms so it stays responsive even on large datasets.
- **Graceful abort** — Hit STOP at any point; every algorithm checks a shared flag on each iteration and exits cleanly.
- **Intelligent comparison** — The `id` column is cast to a numeric type automatically; all other columns fall back to case-insensitive string comparison.
- **Dynamic column picker** — The "Sort By" dropdown populates itself the moment you load a CSV; no configuration file needed.
- **One-click CSV export** — The fully sorted dataset can be saved directly from the app.

---

## Requirements

- **Python 3.7+**
- No third-party packages — the application uses only the standard library (`csv`, `tkinter`, `threading`, `time`).

---

## How to Run

```bash
python sorting_app.py
```

On macOS you may need to run from a framework build of Python (`/Library/Frameworks/Python.framework/…`) because `tkinter` is not bundled with the Homebrew or system interpreter by default.

---

## Usage

1. Click **SELECT CSV FILE** and choose any `.csv` on disk.
2. Set the desired row count in the **Rows (N)** field (default 100 000).
3. Pick an algorithm from the **Algorithm** dropdown.
4. Choose which column to sort by from the **Sort By** dropdown.
5. Press **START BENCHMARK**. Timing and a 10-row preview appear in the log pane when the sort finishes.
6. Optionally click **EXPORT CSV** to save the sorted data.

> **Performance note:** The app warns you before running Bubble Sort or Insertion Sort on more than 25 000 rows because their O(n²) complexity makes large runs impractical.

---

## Benchmark Table

The table below was produced by running each algorithm on randomly generated CSV data, sorting on a numeric `id` column. Bubble Sort and Insertion Sort were not run at 100 000 rows because their quadratic scaling would push runtimes into the range of several hours on typical hardware.

| Algorithm      |   1,000 rows |  10,000 rows | 100,000 rows |
|----------------|-------------:|-------------:|-------------:|
| Merge Sort     |     0.0059 s |     0.0480 s |     0.6535 s |
| Bubble Sort    |     0.1319 s |    14.0130 s |         N/A* |
| Insertion Sort |     0.0408 s |     4.1750 s |         N/A* |

\* O(n²) — estimated runtime at 100 000 rows exceeds several hours; benchmark omitted.

### What the numbers show

**Merge Sort** is the clear winner at every scale. It is the only O(n log n) algorithm in the suite, and its time grows almost exactly as theory predicts: roughly 8× from 1 k → 10 k, and roughly 14× from 10 k → 100 k.

**Insertion Sort** is faster than Bubble Sort at every size, which is expected: it moves each element into its correct position in a single pass rather than repeatedly swapping adjacent pairs. Its early-termination behaviour (the inner `while` loop stops as soon as the correct slot is found) gives it a practical edge over Bubble Sort, especially when the data is partially ordered.

**Bubble Sort** is the slowest algorithm tested. Its optimized variant (the `swapped` flag lets it exit early on already-sorted data) helps on best-case inputs, but on random data it still performs the full O(n²) work.

---

## Algorithm Details

### Merge Sort — O(n log n)

A recursive divide-and-conquer sort. The list is split in half repeatedly until each sublist has one element, then the halves are merged back together in sorted order. Because the recursion depth is O(log n), the app sets `sys.setrecursionlimit(200 000)` to handle very large datasets without hitting Python's default stack limit.

### Bubble Sort — O(n²)

Iterates through the list, swapping adjacent elements that are out of order. A `swapped` flag is checked after each full pass; if no swaps occurred the list is already sorted and the algorithm terminates early. This optimisation makes best-case performance O(n), but average and worst-case remain O(n²).

### Insertion Sort — O(n²)

Builds the sorted portion of the list one element at a time. For each new element it walks backward through the already-sorted section, shifting elements right until it finds the correct insertion point. Like Bubble Sort it is O(n²) in the worst case, but it tends to be faster in practice because it does fewer total comparisons on partially ordered data.

---

## Project Structure

```
sorting_app.py      Main application — GUI, sorting logic, benchmarking
README.md           This file
```

---

