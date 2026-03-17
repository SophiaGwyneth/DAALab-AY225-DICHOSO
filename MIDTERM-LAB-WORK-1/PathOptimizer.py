import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv

class PathFinderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Path Optimizer — Dijkstra's Algorithm")
        self.root.geometry("1280x800")
        self.root.configure(bg='#141822')

        self.edges = []
        self.nodes = []

        # -- TOP BAR --
        top_frame = tk.Frame(self.root, bg='#1E2432', padx=10, pady=8)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        self.styled_label(top_frame, "Source Node:").pack(side=tk.LEFT, padx=5)
        self.source_combo = ttk.Combobox(top_frame, width=12, state="readonly")
        self.source_combo.pack(side=tk.LEFT, padx=5)

        self.styled_label(top_frame, "Criteria:").pack(side=tk.LEFT, padx=5)
        self.criteria_combo = ttk.Combobox(top_frame, values=["FUEL", "DISTANCE", "TIME", "ALL"], width=12, state="readonly")
        self.criteria_combo.set("FUEL")
        self.criteria_combo.pack(side=tk.LEFT, padx=5)

        self.styled_btn(top_frame, "📂 Upload CSV", '#326EBE', self.load_csv).pack(side=tk.LEFT, padx=5)
        self.styled_btn(top_frame, "⚡ Analyze", '#289646', self.analyze).pack(side=tk.LEFT, padx=5)
        self.styled_btn(top_frame, "🗑 Clear", '#822828', self.clear_all).pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(top_frame, text=" No dataset loaded", fg='#B4A050', bg='#1E2432', font=("Courier", 10))
        self.status_label.pack(side=tk.LEFT, padx=10)

        # -- MAIN CONTENT (PanedWindow) --
        pw = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg='#141822', bd=0, sashwidth=4)
        pw.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Left: Calculation Area
        self.calc_area = tk.Text(pw, bg='#FFFCEB', fg='#141E78', font=("Courier", 11), padx=15, pady=15)
        self.calc_area.insert("1.0", "Upload CSV then click Analyze to see calculations.")
        pw.add(self.calc_area, width=780)

        # Right: Summary Area
        self.summary_area = tk.Text(pw, bg='#0E121E', fg='#B4E6C3', font=("Courier", 11), padx=15, pady=15)
        self.summary_area.insert("1.0", "Summary will appear here.")
        pw.add(self.summary_area)

    # -- LOGIC --

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path: return
        
        try:
            with open(file_path, mode='r') as f:
                reader = csv.reader(f)
                next(reader) # skip header
                self.edges = []
                temp_nodes = set()
                for row in reader:
                    if not row or len(row) < 5: continue
                    edge = {
                        'from': row[0].strip(), 'to': row[1].strip(),
                        'dist': float(row[2]), 'time': float(row[3]), 'fuel': float(row[4])
                    }
                    self.edges.append(edge)
                    temp_nodes.update([edge['from'], edge['to']])
                
                self.nodes = sorted(list(temp_nodes), key=lambda x: int(x) if x.isdigit() else x)
                self.source_combo['values'] = self.nodes
                self.status_label.config(text=f" ✔ {len(self.edges)} edges | Nodes: {self.nodes}", fg='#50DC82')
        except Exception as e:
            messagebox.showerror("CSV Error", f"Could not read file:\n{e}")

    def analyze(self):
        if not self.edges:
            self.calc_area.delete("1.0", tk.END)
            self.calc_area.insert("1.0", "Upload a dataset first.")
            return

        src = self.source_combo.get()
        criteria = self.criteria_combo.get()
        if not src: return

        dests = [n for n in self.nodes if n != src]
        
        do_fuel = criteria in ["FUEL", "ALL"]
        do_dist = criteria in ["DISTANCE", "ALL"]
        do_time = criteria in ["TIME", "ALL"]

        calc_text = ""
        summ_text = ""

        modes = []
        if do_fuel: modes.append("FUEL")
        if do_dist: modes.append("DISTANCE")
        if do_time: modes.append("TIME")

        for m in modes:
            calc_text += self.build_calc_block(src, dests, m)
            summ_text += self.build_summary_block(src, dests, m)

        self.calc_area.delete("1.0", tk.END)
        self.calc_area.insert("1.0", calc_text)
        self.summary_area.delete("1.0", tk.END)
        self.summary_area.insert("1.0", summ_text)

    def build_calc_block(self, src, dests, mode):
        unit = {"FUEL": "L", "DISTANCE": "km", "TIME": "min"}[mode]
        sb = f" {'═'*70}\n  {mode} =\n {'─'*70}\n\n"
        grand_total = 0

        for dst in dests:
            paths = self.enumerate_all_paths(src, dst)
            if not paths:
                sb += f"  {src} → {dst} : (unreachable)\n\n"
                continue
            
            paths.sort(key=lambda p: p[mode])
            min_val = paths[0][mode]
            grand_total += min_val

            sb += f"  {src} → {dst}\n {'-'*60}\n"
            for p in paths:
                val = p[mode]
                is_best = (val == min_val)
                
                # Build segments string
                seg_parts = []
                run_parts = []
                for i in range(len(p['path'])-1):
                    u, v = p['path'][i], p['path'][i+1]
                    edge = self.find_edge(u, v)
                    ev = edge[mode.lower()[:4] if mode != "DISTANCE" else "dist"]
                    seg_parts.append(f"{u},{v}={self.fmt(ev)}")
                    run_parts.append(self.fmt(ev))

                seg_str = " + ".join(seg_parts)
                run_str = " + ".join(run_parts)
                best_tag = f"  ◄ {self.fmt(val)} {unit}" if is_best else ""

                if len(p['path']) == 2:
                    sb += f"  {seg_str} = {self.fmt(val)}{best_tag}\n"
                else:
                    sb += f"  {seg_str}\n       = {run_str} = {self.fmt(val)}{best_tag}\n"
            sb += "\n"
        
        sb += f" {'═'*70}\n  TOTAL CHEAPEST {mode:<10} = {grand_total:.2f} {unit}\n {'═'*70}\n\n"
        return sb

    def build_summary_block(self, src, dests, mode):
        unit = {"FUEL": "L", "DISTANCE": "km", "TIME": "min"}[mode]
        sb = f" {'═'*55}\n  {mode} — BEST PATHS FROM NODE {src}\n {'═'*55}\n"
        sb += f"  {'DEST':<6}  {'BEST PATH':<28}  VALUE\n {'-'*55}\n"
        
        total = 0
        for dst in dests:
            paths = self.enumerate_all_paths(src, dst)
            if not paths:
                sb += f"  {dst:<6}  {'(unreachable)':<28}  N/A\n"
                continue
            
            paths.sort(key=lambda p: p[mode])
            best = paths[0]
            val = best[mode]
            total += val
            path_str = " → ".join(best['path'])
            sb += f"  {src+'→'+dst:<6}  {path_str:<28}  {val:.2f} {unit}\n"
            
        sb += f" {'-'*55}\n  {'TOTAL':<6}  {'':<28}  {total:.2f} {unit}\n {'═'*55}\n\n"
        return sb

    def enumerate_all_paths(self, src, dst):
        results = []
        stack = [[src]]
        while stack:
            path = stack.pop()
            last = path[-1]
            if last == dst:
                d, t, f = 0, 0, 0
                for i in range(len(path)-1):
                    e = self.find_edge(path[i], path[i+1])
                    d += e['dist']; t += e['time']; f += e['fuel']
                results.append({'path': list(path), 'DISTANCE': d, 'TIME': t, 'FUEL': f})
                continue
            
            for e in self.edges:
                if e['from'] == last and e['to'] not in path:
                    new_path = list(path)
                    new_path.append(e['to'])
                    stack.append(new_path)
        return results

    # -- HELPERS --
    def find_edge(self, u, v):
        return next((e for e in self.edges if e['from'] == u and e['to'] == v), None)

    def fmt(self, v):
        return f"{int(v)}" if v == int(v) else f"{v:.1f}"

    def clear_all(self):
        self.calc_area.delete("1.0", tk.END)
        self.summary_area.delete("1.0", tk.END)

    def styled_label(self, parent, text):
        return tk.Label(parent, text=text, fg='#AACDFF', bg='#1E2432', font=("Arial", 9, "bold"))

    def styled_btn(self, parent, text, color, cmd):
        return tk.Button(parent, text=text, bg=color, fg='white', font=("Arial", 9, "bold"), 
                         relief="flat", padx=10, command=cmd, cursor="hand2")

if __name__ == "__main__":
    root = tk.Tk()
    app = PathFinderUI(root)
    root.mainloop()