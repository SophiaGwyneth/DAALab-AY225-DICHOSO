# DAALab-AY225
The DAA-Lab Repo

# Descending Order Sorting Suite

A Python-based utility that implements various sorting algorithms to arrange numerical datasets in descending order. This program is a **Console-based (CLI)** application.

## 🖥️ Interface Type

* **Interface:** Command Line Interface (CLI) / Console-based.
* **Interaction:** Text-based menu navigation and terminal output.

---

## 🚀 Features

* **Three Sorting Algorithms:**
* **Bubble Sort:** Optimized with a swap-check flag.
* **Insertion Sort:** Efficient for small datasets.
* **Merge Sort:** High-performance  recursive algorithm.


* **Performance Tracking:** Measures and displays the exact time taken (in seconds) to sort the data.
* **Automated Verification:** Checks the final list to ensure the sorting logic was successful.
* **Flexible Data Loading:** Reads numbers from a text file, supporting spaces, commas, or new lines.

---

## 📂 Project Structure

* `main.py`: The core script containing the algorithms and menu logic.
* `dataset.txt`: The input file containing the numbers to be sorted.

---

## 🛠️ Requirements

* **Python 3.x**
* No external libraries required (uses standard `time` and `sys` modules).

---

## 📖 Usage

### 1. Prepare your data

Create a file named `dataset.txt` in the same directory as the script. Add your numbers separated by spaces, commas, or new lines.

### 2. Run the program

Open your terminal or command prompt and execute:

```bash
python main.py

```

### 3. Navigate the Menu

Once the program starts, follow the on-screen prompts:

1. Select an algorithm (1-3) to sort the data.
2. View the sorted output and performance metrics.
3. Select option **4** to exit.

---

## 📊 Comparison of Algorithms Included

| Algorithm | Best Case | Average Case | Worst Case | Type |
| --- | --- | --- | --- | --- |
| **Bubble Sort** |  |  |  | Comparison |
| **Insertion Sort** |  |  |  | Comparison |
| **Merge Sort** |  |  |  | Divide & Conquer |

---

## ⚠️ Troubleshooting

* **File Not Found:** Ensure `dataset.txt` is in the same folder as the script.
* **Invalid Input:** The program expects numerical values in the text file. Non-numeric strings will be skipped.
