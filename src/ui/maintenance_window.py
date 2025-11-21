import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.maintenance_logic import MaintenanceLogic
from src.logic.vehicle_logic import VehicleLogic # Para listar vehículos

class MaintenanceWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Bitácora de Mantenimiento")
        self.geometry("900x600")
        self.config(bg="#F4F6F9")
        
        # Estilos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#343a40", foreground="white", relief="flat")
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)

        self.vehicles_map = {}
        
        self.create_header()
        self.create_form()
        self.create_table()
        self.load_vehicles()
        self.load_data()

    def create_header(self):
        h = tk.Frame(self, bg="#F4F6F9")
        h.pack(fill="x", padx=20, pady=10)
        tk.Label(h, text="🛠️ Registro de Mantenimiento", font=("Segoe UI", 20, "bold"), bg="#F4F6F9", fg="#333").pack(side="left")

    def create_form(self):
        card = tk.Frame(self, bg="white", padx=20, pady=20)
        card.pack(fill="x", padx=20, pady=5)

        tk.Label(card, text="Vehículo:", font=("Segoe UI", 9, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        self.combo_veh = ttk.Combobox(card, state="readonly", width=30)
        self.combo_veh.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(card, text="Costo ($):", font=("Segoe UI", 9, "bold"), bg="white").grid(row=0, column=2, sticky="w")
        self.entry_cost = tk.Entry(card, width=15, bg="#f8f9fa", relief="flat", highlightthickness=1)
        self.entry_cost.grid(row=0, column=3, padx=10, ipady=3)

        tk.Label(card, text="Descripción:", font=("Segoe UI", 9, "bold"), bg="white").grid(row=1, column=0, sticky="nw", pady=10)
        self.entry_desc = tk.Entry(card, width=60, bg="#f8f9fa", relief="flat", highlightthickness=1)
        self.entry_desc.grid(row=1, column=1, columnspan=3, sticky="w", padx=10, ipady=3)

        tk.Button(card, text="REGISTRAR", bg="#28a745", fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", cursor="hand2", command=self.save).grid(row=2, column=3, sticky="e", pady=10)

    def create_table(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        cols = ("id", "placa", "modelo", "desc", "costo", "fecha")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        headers = ["ID", "Placa", "Modelo", "Descripción del Trabajo", "Costo", "Fecha"]
        widths = [40, 80, 150, 300, 80, 120]
        
        for c, h, w in zip(cols, headers, widths):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w)
            
        self.tree.pack(side="left", fill="both", expand=True)
        sc = ttk.Scrollbar(frame, command=self.tree.yview); self.tree.configure(yscroll=sc.set); sc.pack(side="right", fill="y")

    def load_vehicles(self):
        # Usamos la logica de vehiculos existente
        rows = VehicleLogic.read_all()
        self.vehicles_map = {f"{r['plate_number']} - {r['model']}": r['id'] for r in rows}
        self.combo_veh['values'] = list(self.vehicles_map.keys())

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        rows = MaintenanceLogic.read_all()
        for r in rows:
            self.tree.insert("", "end", values=(r['id'], r['plate_number'], r['model'], r['description'], f"${r['cost']}", r['log_date']))

    def save(self):
        v_txt = self.combo_veh.get()
        desc = self.entry_desc.get()
        cost = self.entry_cost.get()
        
        if not v_txt or not desc or not cost: return
        
        v_id = self.vehicles_map[v_txt]
        ok, msg = MaintenanceLogic.create_log(v_id, desc, cost)
        if ok:
            messagebox.showinfo("Listo", msg)
            self.load_data()
            self.entry_desc.delete(0, "end")
            self.entry_cost.delete(0, "end")
        else:
            messagebox.showerror("Error", msg)