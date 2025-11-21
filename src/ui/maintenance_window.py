import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.maintenance_logic import MaintenanceLogic
from src.logic.vehicle_logic import VehicleLogic 

class MaintenanceWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Bitácora de Mantenimiento")
        self.geometry("1000x650")
        self.config(bg="#F4F6F9")
        
        # --- ESTILOS VISUALES ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#343a40", foreground="white", relief="flat")
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, background="white", foreground="black", fieldbackground="white")
        self.style.map("Treeview", background=[('selected', '#007bff')], foreground=[('selected', 'white')])

        self.vehicles_map = {}
        self.reverse_veh_map = {} 
        
      
        self.create_header()
        self.create_form_area()
        self.create_table_area()
        
        try:
            self.load_vehicles()
            self.load_data()
        except Exception as e:
            print(f"Error cargando ventana: {e}")

    def create_header(self):
        h = tk.Frame(self, bg="#F4F6F9")
        h.pack(fill="x", padx=20, pady=15)
        tk.Label(h, text="🛠️ Registro de Taller", font=("Segoe UI", 22, "bold"), bg="#F4F6F9", fg="#333").pack(side="left")

    def create_form_area(self):
        card = tk.Frame(self, bg="white", padx=20, pady=20)
        card.pack(fill="x", padx=20, pady=5)

        self.var_id = tk.StringVar() 

        inputs = tk.Frame(card, bg="white")
        inputs.pack(fill="x", pady=(0, 15))

        
        tk.Label(inputs, text="Vehículo:", font=("Segoe UI", 9, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        self.combo_veh = ttk.Combobox(inputs, state="readonly", width=40)
        self.combo_veh.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(inputs, text="Costo ($):", font=("Segoe UI", 9, "bold"), bg="white").grid(row=0, column=2, sticky="w")
        self.entry_cost = tk.Entry(inputs, width=15, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#ddd", fg="black")
        self.entry_cost.grid(row=0, column=3, padx=10, ipady=3)

       
        tk.Label(inputs, text="Descripción:", font=("Segoe UI", 9, "bold"), bg="white").grid(row=1, column=0, sticky="nw", pady=10)
        self.entry_desc = tk.Entry(inputs, width=65, bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#ddd", fg="black")
        self.entry_desc.grid(row=1, column=1, columnspan=3, sticky="w", padx=10, ipady=3)

        
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill="x", pady=5)

        self.create_btn(btn_frame, "Guardar", "#28a745", self.save)
        self.create_btn(btn_frame, "Actualizar", "#17a2b8", self.update)
        self.create_btn(btn_frame, "Eliminar", "#dc3545", self.delete)
        self.create_btn(btn_frame, "Limpiar", "#6c757d", self.clear)

    def create_btn(self, parent, text, color, cmd):
        tk.Button(parent, text=text, bg=color, fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", cursor="hand2", padx=20, pady=8, command=cmd).pack(side="left", padx=(0, 10))

    def create_table_area(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Historial de Mantenimientos", font=("Segoe UI", 11, "bold"), bg="white", fg="#555").pack(anchor="w", pady=(0, 10))
        
        cols = ("id", "placa", "modelo", "desc", "costo", "fecha", "vid")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        headers = ["ID", "Placa", "Modelo", "Descripción del Trabajo", "Costo", "Fecha"]
        widths = [40, 100, 150, 300, 80, 120]
        
        for c, h, w in zip(cols[:-1], headers, widths):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w)
            
        self.tree.column("vid", width=0, stretch=False) 

        self.tree.pack(side="left", fill="both", expand=True)
        sc = ttk.Scrollbar(frame, command=self.tree.yview); self.tree.configure(yscroll=sc.set); sc.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

    def load_vehicles(self):
        rows = VehicleLogic.read_all()
        self.vehicles_map = {}
        self.reverse_veh_map = {}
        values = []
        for r in rows:
            display = f"{r['plate_number']} - {r['model']}"
            values.append(display)
            self.vehicles_map[display] = r['id']
            self.reverse_veh_map[r['id']] = display
        self.combo_veh['values'] = values

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        rows = MaintenanceLogic.read_all()
        
        print(f"[DEBUG UI MANTENIMIENTO] Cargando {len(rows)} filas.") # Chivato
        
        for r in rows:
      
            self.tree.insert("", "end", values=(
                r[0], # ID
                r[1], # Placa
                r[2], # Modelo
                r[3], # Desc
                f"${r[4]}", # Costo
                r[5], # Fecha
                r[6]  # VID
            ))

    def select_item(self, event):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            vals = item['values']
            self.var_id.set(vals[0])
            
            vid = vals[6]
            if vid in self.reverse_veh_map:
                self.combo_veh.set(self.reverse_veh_map[vid])
            
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, vals[3])
            
            cost_clean = str(vals[4]).replace("$", "")
            self.entry_cost.delete(0, tk.END)
            self.entry_cost.insert(0, cost_clean)

    def save(self):
        v_txt = self.combo_veh.get()
        desc = self.entry_desc.get()
        cost = self.entry_cost.get()
        
        if not v_txt or not desc or not cost: 
            messagebox.showwarning("Atención", "Llene todos los campos")
            return
        
        v_id = self.vehicles_map[v_txt]
        ok, msg = MaintenanceLogic.create_log(v_id, desc, cost)
        if ok:
            messagebox.showinfo("Listo", msg)
            self.load_data()
            self.clear()
        else:
            messagebox.showerror("Error", msg)

    def update(self):
        if not self.var_id.get(): 
            messagebox.showwarning("Atención", "Seleccione un registro para editar")
            return
        
        ok, msg = MaintenanceLogic.update(self.var_id.get(), self.entry_desc.get(), self.entry_cost.get())
        if ok:
            messagebox.showinfo("Actualizado", msg)
            self.load_data()
            self.clear()
        else:
            messagebox.showerror("Error", msg)

    def delete(self):
        if not self.var_id.get(): return
        if messagebox.askyesno("Confirmar", "¿Borrar este registro?"):
            ok, msg = MaintenanceLogic.delete(self.var_id.get())
            if ok:
                self.load_data()
                self.clear()
            else:
                messagebox.showerror("Error", msg)

    def clear(self):
        self.var_id.set("")
        self.combo_veh.set("")
        self.entry_desc.delete(0, tk.END)
        self.entry_cost.delete(0, tk.END)