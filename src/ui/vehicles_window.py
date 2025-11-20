import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.vehicle_logic import VehicleLogic

class VehiclesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Vehículos")
        self.geometry("900x600")
        self.config(bg="#f4f4f4")
        
        self.create_toolbar()
        self.create_form()
        self.create_table()
        self.load_data()

    def create_toolbar(self):
        toolbar = tk.Frame(self, bg="#ddd", height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        tk.Button(toolbar, text="Ayuda (?)", command=lambda: messagebox.showinfo("Ayuda", "Gestione la flota vehicular aquí."), bg="#ddd", relief=tk.FLAT).pack(side=tk.RIGHT, padx=10)

    def create_form(self):
        frame = tk.LabelFrame(self, text="Datos del Vehículo", bg="white", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        # Variables
        self.var_id = tk.StringVar()
        self.var_model = tk.StringVar()
        self.var_plate = tk.StringVar()
        self.var_chassis = tk.StringVar()
        self.var_rate = tk.DoubleVar(value=0.0)
        self.var_status = tk.IntVar(value=1) # 1=Disponible, 0=Rentado

        # Inputs
        tk.Label(frame, text="Modelo/Marca:", bg="white").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.var_model, width=30).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Placa:", bg="white").grid(row=0, column=2, sticky="w")
        tk.Entry(frame, textvariable=self.var_plate, width=20).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame, text="Chasis:", bg="white").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.var_chassis, width=30).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Tarifa Diaria ($):", bg="white").grid(row=1, column=2, sticky="w")
        tk.Entry(frame, textvariable=self.var_rate, width=15).grid(row=1, column=3, padx=5, pady=5)
        
        tk.Checkbutton(frame, text="Disponible", variable=self.var_status, bg="white").grid(row=2, column=0)

        # Botones
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_frame, text="Guardar", bg="#28a745", fg="white", width=10, command=self.save).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Actualizar", bg="#ffc107", width=10, command=self.update).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar", bg="#dc3545", fg="white", width=10, command=self.delete).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar", bg="#6c757d", fg="white", width=10, command=self.clear).pack(side=tk.LEFT, padx=5)

    def create_table(self):
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        cols = ("id", "modelo", "placa", "chasis", "tarifa", "estado")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("modelo", text="Modelo")
        self.tree.heading("placa", text="Placa")
        self.tree.heading("chasis", text="Chasis")
        self.tree.heading("tarifa", text="Tarifa")
        self.tree.heading("estado", text="Estado")
        
        self.tree.column("id", width=30)
        self.tree.column("estado", width=80)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = VehicleLogic.read_all()
        for r in rows:
            estado = "Disponible" if r['is_available'] == 1 else "Ocupado"
            self.tree.insert("", tk.END, values=(r['id'], r['model'], r['plate_number'], r['chassis_number'], r['daily_rate'], estado))

    def select_item(self, event):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            vals = item['values']
            self.var_id.set(vals[0])
            self.var_model.set(vals[1])
            self.var_plate.set(vals[2])
            self.var_chassis.set(vals[3])
            self.var_rate.set(vals[4])
            self.var_status.set(1 if vals[5] == "Disponible" else 0)

    def save(self):
        if not self.var_model.get() or not self.var_plate.get():
            messagebox.showwarning("Error", "Modelo y Placa requeridos")
            return
        ok, msg = VehicleLogic.create(self.var_model.get(), self.var_plate.get(), self.var_chassis.get(), self.var_rate.get())
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.load_data()
            self.clear()
        else:
            messagebox.showerror("Error", msg)

    def update(self):
        if not self.var_id.get(): return
        ok, msg = VehicleLogic.update(self.var_id.get(), self.var_model.get(), self.var_plate.get(), self.var_chassis.get(), self.var_rate.get(), self.var_status.get())
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.load_data()
            self.clear()

    def delete(self):
        if not self.var_id.get(): return
        if messagebox.askyesno("Confirmar", "¿Borrar vehículo?"):
            ok, msg = VehicleLogic.delete(self.var_id.get())
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.load_data()
                self.clear()
            else:
                messagebox.showerror("Error", msg)

    def clear(self):
        self.var_id.set("")
        self.var_model.set("")
        self.var_plate.set("")
        self.var_chassis.set("")
        self.var_rate.set(0.0)
        self.var_status.set(1)
        