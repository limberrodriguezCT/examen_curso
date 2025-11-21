import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.vehicle_logic import VehicleLogic

class VehiclesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Vehículos")
        self.geometry("1000x650")
        self.config(bg="#F4F6F9")
        
        # Estilos compartidos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#343a40", foreground="white", relief="flat")
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        self.style.map("Treeview", background=[('selected', '#007bff')])

        self.create_header()
        self.create_form()
        self.create_table()
        self.load_data()

    def create_header(self):
        header = tk.Frame(self, bg="#F4F6F9")
        header.pack(fill="x", padx=20, pady=(20, 10))
        tk.Label(header, text="🚗 Flota Vehicular", font=("Segoe UI", 20, "bold"), bg="#F4F6F9", fg="#333").pack(side="left")

    def create_form(self):
        card = tk.Frame(self, bg="white", padx=20, pady=20)
        card.pack(fill="x", padx=20, pady=5)

        self.var_id = tk.StringVar()
        self.var_model = tk.StringVar()
        self.var_plate = tk.StringVar()
        self.var_chassis = tk.StringVar()
        self.var_rate = tk.DoubleVar(value=0.0)
        self.var_status = tk.IntVar(value=1)

        # Inputs
        self.create_input(card, "Modelo / Marca:", self.var_model, 0, 0, width=30)
        self.create_input(card, "Placa:", self.var_plate, 0, 2)
        self.create_input(card, "No. Chasis:", self.var_chassis, 1, 0, width=30)
        self.create_input(card, "Tarifa Diaria ($):", self.var_rate, 1, 2)
        
        # Checkbox
        tk.Checkbutton(card, text="Vehículo Disponible para Renta", variable=self.var_status, 
                       bg="white", activebackground="white", font=("Segoe UI", 10)).grid(row=2, column=0, columnspan=2, sticky="w", pady=10)

        # Botones
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=4, sticky="e", pady=10)
        self.create_btn(btn_frame, "Guardar", "#28a745", self.save)
        self.create_btn(btn_frame, "Actualizar", "#17a2b8", self.update)
        self.create_btn(btn_frame, "Eliminar", "#dc3545", self.delete)
        self.create_btn(btn_frame, "Limpiar", "#6c757d", self.clear)

    def create_input(self, parent, label, var, r, c, width=20):
        tk.Label(parent, text=label, font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=r, column=c, sticky="w", pady=5)
        tk.Entry(parent, textvariable=var, width=width, font=("Segoe UI", 10), bg="#f8f9fa", relief="flat", highlightthickness=1).grid(row=r, column=c+1, sticky="w", padx=10, ipady=5)

    def create_btn(self, parent, text, color, cmd):
        tk.Button(parent, text=text, bg=color, fg="white", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", padx=15, pady=5, command=cmd).pack(side="left", padx=5)

    def create_table(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        cols = ("id", "modelo", "placa", "chasis", "tarifa", "estado")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        headers = ["ID", "Modelo", "Placa", "Chasis", "Tarifa", "Estado"]
        for c, h in zip(cols, headers):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=100)
        
        self.tree.tag_configure("ocupado", foreground="red")
        self.tree.tag_configure("disponible", foreground="green")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = VehicleLogic.read_all()
        for r in rows:
            estado_txt = "Disponible" if r['is_available'] == 1 else "Rentado"
            tag = "disponible" if r['is_available'] == 1 else "ocupado"
            self.tree.insert("", tk.END, values=(r['id'], r['model'], r['plate_number'], r['chassis_number'], f"${r['daily_rate']}", estado_txt), tags=(tag,))

    def select_item(self, event):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            vals = item['values']
            self.var_id.set(vals[0])
            self.var_model.set(vals[1])
            self.var_plate.set(vals[2])
            self.var_chassis.set(vals[3])
          
            rate_clean = str(vals[4]).replace("$", "")
            self.var_rate.set(float(rate_clean))
            self.var_status.set(1 if vals[5] == "Disponible" else 0)

    def save(self):
        if not self.var_model.get(): return
        ok, msg = VehicleLogic.create(self.var_model.get(), self.var_plate.get(), self.var_chassis.get(), self.var_rate.get())
        if ok: self.load_data(); self.clear(); messagebox.showinfo("Ok", msg)
        else: messagebox.showerror("Error", msg)

    def update(self):
        if not self.var_id.get(): return
        ok, msg = VehicleLogic.update(self.var_id.get(), self.var_model.get(), self.var_plate.get(), self.var_chassis.get(), self.var_rate.get(), self.var_status.get())
        if ok: self.load_data(); self.clear(); messagebox.showinfo("Ok", msg)

    def delete(self):
        if not self.var_id.get(): return
        if messagebox.askyesno("Confirmar", "¿Borrar?"):
            ok, msg = VehicleLogic.delete(self.var_id.get())
            if ok: self.load_data(); self.clear()
            else: messagebox.showerror("Error", msg)

    def clear(self):
        self.var_id.set(""); self.var_model.set(""); self.var_plate.set(""); self.var_chassis.set(""); self.var_rate.set(0.0); self.var_status.set(1)
        