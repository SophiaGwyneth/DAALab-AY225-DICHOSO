import csv
import time
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

# Increase recursion depth for Merge Sort on massive datasets
sys.setrecursionlimit(200000)

class SmoothSortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AlgoMetric Pro - Performance Suite")
        self.root.geometry("800x950")
        self.root.configure(bg="#121212") 
        
        self.file_path = ""
        self.sorted_results = []
        self.headers = []
        self.is_running = False
        
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define theme colors
        bg_color = "#121212"
        accent_cyan = "#00FFCC"
        
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground="#E0E0E0", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground=accent_cyan)
        
        style.configure("BigProgress.Horizontal.TProgressbar", 
                        troughcolor="#333333", 
                        background=accent_cyan, 
                        thickness=25)

        header = ttk.Label(self.root, text="ALGO-METRIC BENCHMARK PRO", style="Header.TLabel")
        header.pack(pady=20)

        # 1. Data Source Section
        file_frame = tk.LabelFrame(self.root, text=" 1. Data Source ", bg=bg_color, fg=accent_cyan, padx=15, pady=15)
        file_frame.pack(fill="x", padx=40, pady=10)
        
        self.btn_browse = tk.Button(file_frame, text="SELECT CSV FILE", command=self.load_file, bg="#333", fg="white", relief="flat", padx=10)
        self.btn_browse.pack(side="left")
        
        self.lbl_file = ttk.Label(file_frame, text="Waiting for input...", font=("Segoe UI", 9, "italic"))
        self.lbl_file.pack(side="left", padx=20)

        # 2. Parameters Section
        config_frame = tk.LabelFrame(self.root, text=" 2. Parameters ", bg=bg_color, fg=accent_cyan, padx=15, pady=15)
        config_frame.pack(fill="x", padx=40, pady=10)

        ttk.Label(config_frame, text="Rows to Process (N):").grid(row=0, column=0, sticky="w")
        self.ent_n = tk.Entry(config_frame, bg="#222", fg=accent_cyan, insertbackground="white", borderwidth=0, font=("Consolas", 11))
        self.ent_n.insert(0, "10000")
        self.ent_n.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(config_frame, text="Sort Algorithm:").grid(row=1, column=0, sticky="w")
        self.var_alg = tk.StringVar(value="Merge Sort")
        alg_menu = ttk.OptionMenu(config_frame, self.var_alg, "Merge Sort", "Merge Sort", "Bubble Sort", "Insertion Sort")
        alg_menu.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        config_frame.columnconfigure(1, weight=1)

        # 3. Action Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=40, pady=10)

        self.btn_run = tk.Button(btn_frame, text="START BENCHMARK", bg=accent_cyan, fg="#121212", font=("Segoe UI", 10, "bold"), command=self.run_benchmark_threaded)
        self.btn_run.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_stop = tk.Button(btn_frame, text="STOP", bg="#FF3366", fg="white", state="disabled", command=self.stop, width=10)
        self.btn_stop.pack(side="left", padx=5)

        self.btn_export = tk.Button(btn_frame, text="EXPORT CSV", bg="#28A745", fg="white", state="disabled", command=self.export_csv, width=15)
        self.btn_export.pack(side="left", padx=5)

        # 4. Progress Visualization
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100, style="BigProgress.Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=40, pady=(20, 5))

        self.lbl_progress = tk.Label(self.root, text="SYSTEM IDLE", font=("Segoe UI", 11, "bold"), bg=bg_color, fg="#FFFFFF")
        self.lbl_progress.pack(pady=5)

        # 5. Result Preview Terminal
        tk.Label(self.root, text="LOG OUTPUT & PREVIEW", bg=bg_color, fg="#555", font=("Segoe UI", 8, "bold")).pack(padx=40, anchor="w")
        self.txt_output = tk.Text(self.root, bg="#000", fg=accent_cyan, font=("Consolas", 10), height=15, borderwidth=0, padx=15, pady=15)
        self.txt_output.pack(padx=40, pady=(0, 20), fill="both", expand=True)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            self.file_path = path
            self.lbl_file.config(text=os.path.basename(path), foreground="#00FFCC")

    def stop(self):
        self.is_running = False
        self.lbl_progress.config(text="ABORTING PROCESS...", fg="#FF3366")

    def run_benchmark_threaded(self):
        if not self.file_path:
            return messagebox.showerror("Error", "No CSV file selected.")
        
        try:
            n = int(self.ent_n.get())
        except ValueError:
            return messagebox.showerror("Error", "Rows (N) must be a valid number.")

        alg = self.var_alg.get()
        
        if n > 15000 and alg in ["Bubble Sort", "Insertion Sort"]:
            warn_msg = f"WARNING: {alg} is $O(n^2)$. Sorting {n} rows will be very slow.\n\nProceed anyway?"
            if not messagebox.askyesno("Performance Warning", warn_msg):
                return

        self.is_running = True
        self.btn_run.config(state="disabled", text="RUNNING...")
        self.btn_stop.config(state="normal")
        self.btn_export.config(state="disabled")
        self.txt_output.delete("1.0", tk.END)
        self.progress_var.set(0)
        
        threading.Thread(target=self.logic, daemon=True).start()

    def get_val(self, row, col):
        """Helper to safely compare numeric or string values."""
        v = row.get(col, "")
        try:
            return float(v)
        except (ValueError, TypeError):
            return str(v).lower()

    def logic(self):
        try:
            n = int(self.ent_n.get())
            alg = self.var_alg.get()
            col = "ID" # Change this if your CSV uses a different primary key

            # MEASURE LOAD TIME
            self.update_status("Reading CSV File...")
            t_start_load = time.perf_counter()
            data = []
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.headers = reader.fieldnames
                if col not in self.headers:
                    # Fallback if "ID" column doesn't exist
                    col = self.headers[0]
                
                for i, row in enumerate(reader):
                    if not self.is_running: break
                    if i >= n: break
                    data.append(row)
            
            t_end_load = time.perf_counter()
            load_time = t_end_load - t_start_load

            if not self.is_running:
                return

            # MEASURE SORT TIME
            self.update_status(f"Sorting with {alg}...")
            t_start_sort = time.perf_counter()
            
            if alg == "Merge Sort":
                sorted_data = self.merge_sort(data, col)
            elif alg == "Bubble Sort":
                sorted_data = self.bubble_sort(data, col)
            else:
                sorted_data = self.insertion_sort(data, col)
            
            t_end_sort = time.perf_counter()
            sort_time = t_end_sort - t_start_sort

            if self.is_running:
                self.sorted_results = sorted_data
                self.root.after(0, lambda: self.finalize(load_time, sort_time, alg))
            else:
                self.update_status("Benchmark Aborted.")

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("System Error", str(e)))
        finally:
            self.root.after(0, self.reset_ui)

    def bubble_sort(self, data, col):
        n = len(data)
        for i in range(n):
            if not self.is_running: return []
            if i % 100 == 0:
                percent = (i / n) * 100
                self.root.after(0, lambda p=percent, r=i: self.update_progress(p, f"BUBBLE SORT: {r} / {n} ROWS"))
            
            for j in range(0, n - i - 1):
                if self.get_val(data[j], col) > self.get_val(data[j+1], col):
                    data[j], data[j+1] = data[j+1], data[j]
        return data

    def insertion_sort(self, data, col):
        n = len(data)
        for i in range(1, n):
            if not self.is_running: return []
            if i % 100 == 0:
                percent = (i / n) * 100
                self.root.after(0, lambda p=percent, r=i: self.update_progress(p, f"INSERTION SORT: {r} / {n} ROWS"))
            
            key = data[i]
            v_key = self.get_val(key, col)
            j = i - 1
            while j >= 0 and self.get_val(data[j], col) > v_key:
                data[j+1] = data[j]
                j -= 1
            data[j+1] = key
        return data

    def merge_sort(self, data, col):
        if not self.is_running or len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.merge_sort(data[:mid], col)
        right = self.merge_sort(data[mid:], col)
        return self.merge(left, right, col)

    def merge(self, left, right, col):
        res = []
        i = j = 0
        while i < len(left) and j < len(right):
            if self.get_val(left[i], col) <= self.get_val(right[j], col):
                res.append(left[i]); i += 1
            else:
                res.append(right[j]); j += 1
        res.extend(left[i:]); res.extend(right[j:])
        return res

    def update_status(self, msg):
        self.root.after(0, lambda: self.lbl_progress.config(text=msg.upper(), fg="#00FFCC"))

    def update_progress(self, val, msg):
        self.progress_var.set(val)
        self.lbl_progress.config(text=msg.upper(), fg="#00FFCC")

    def finalize(self, t_load, t_sort, algo_name):
        self.update_progress(100, "BENCHMARK COMPLETE")
        self.btn_export.config(state="normal")
        
        row_count = len(self.sorted_results)
        throughput = row_count / t_sort if t_sort > 0 else 0
        
        out = f"--- BENCHMARK RESULTS ({algo_name}) ---\n"
        out += f"File I/O Time  : {t_load:.4f} seconds\n"
        out += f"Sorting Time   : {t_sort:.4f} seconds\n"
        out += f"Total Time     : {t_load + t_sort:.4f} seconds\n"
        out += f"Throughput     : {throughput:.2f} rows/sec\n"
        out += f"Dataset Size   : {row_count} rows\n"
        out += f"{'-'*40}\n"
        out += f"PREVIEW (TOP 10 RECORDS):\n"
        
        # Display first 3 columns for preview
        preview_cols = self.headers[:3]
        head_str = " | ".join(preview_cols)
        out += f"{head_str}\n"
        out += f"{'-'*len(head_str)*2}\n"
        
        for row in self.sorted_results[:10]:
            vals = [str(row.get(h, "")) for h in preview_cols]
            out += " | ".join(vals) + "\n"
            
        self.txt_output.insert(tk.END, out)

    def export_csv(self):
        if not self.sorted_results: return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.headers)
                    writer.writeheader()
                    writer.writerows(self.sorted_results)
                messagebox.showinfo("Success", "Data exported successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def reset_ui(self):
        self.is_running = False
        self.btn_run.config(state="normal", text="START BENCHMARK")
        self.btn_stop.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmoothSortingApp(root)
    root.mainloop()