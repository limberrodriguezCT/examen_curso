import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.rental_logic import RentalLogic

class RentalsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Rentas")
        self.geometry("1000x600")
        
        self.customers_map = {} # Para guardar ID del cliente seleccionado
        self.vehicles_map = {}  # Para guardar ID del vehículo seleccionado
        
        self.create_form()
        self.create_table()
        self.load_combos()
        self.load_data()

    def create_form(self):
        frame = tk.LabelFrame(self, text="Nueva Renta", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        # Cliente
        tk.Label(frame, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.combo_customers = ttk.Combobox(frame, width=30, state="readonly")
        self.combo_customers.grid(row=0, column=1, padx=5)

        # Vehículo
        tk.Label(frame, text="Vehículo Disponible:").grid(row=0, column=2, sticky="w")
        self.combo_vehicles = ttk.Combobox(frame, width=30, state="readonly")
        self.combo_vehicles.grid(row=0, column=3, padx=5)

        # Días
        tk.Label(frame, text="Días de renta:").grid(row=1, column=0, sticky="w")
        self.entry_days = tk.Entry(frame, width=10)
        self.entry_days.grid(row=1, column=1, sticky="w", padx=5)

        # Botón Rentar
        tk.Button(frame, text="REGISTRAR RENTA", bg="#007bff", fg="white", command=self.save_rental).grid(row=1, column=3, pady=10, sticky="e")

    def create_table(self):
        # Tabla de Rentas Activas
        frame = tk.LabelFrame(self, text="Rentas Activas (Vehículos en calle)")
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        cols = ("id", "cliente", "vehiculo", "placa", "fecha", "total", "vid")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("vehiculo", text="Vehículo")
        self.tree.heading("placa", text="Placa")
        self.tree.heading("fecha", text="Fecha Salida")
        self.tree.heading("total", text="Total ($)")
        
        self.tree.column("id", width=30)
        self.tree.column("vid", width=0, stretch=False) # Ocultar ID vehiculo
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Botón para Finalizar Renta
        btn_frame = tk.Frame(frame)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Button(btn_frame, text="FINALIZAR\nRENTA\n(Devolución)", bg="#dc3545", fg="white", command=self.end_rental).pack(pady=20, padx=5)

    def load_combos(self):
        # Cargar Clientes
        customers = RentalLogic.get_customers()
        c_values = []
        self.customers_map = {}
        for c in customers:
            display = f"{c['full_name']} ({c['document_number']})"
            c_values.append(display)
            self.customers_map[display] = c['id']
        self.combo_customers['values'] = c_values

        # Cargar Vehículos Disponibles
        vehicles = RentalLogic.get_available_vehicles()
        v_values = []
        self.vehicles_map = {}
        for v in vehicles:
            display = f"{v['model']} - {v['plate_number']} (${v['daily_rate']}/día)"
            v_values.append(display)
            self.vehicles_map[display] = v['id']
        self.combo_vehicles['values'] = v_values

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = RentalLogic.read_all_active()
        for r in rows:
            self.tree.insert("", tk.END, values=(r['id'], r['full_name'], r['model'], r['plate_number'], r['rental_date'], r['total_amount'], r['vehicle_id']))

    def save_rental(self):
        c_text = self.combo_customers.get()
        v_text = self.combo_vehicles.get()
        days = self.entry_days.get()

        if not c_text or not v_text or not days:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        
        if not days.isdigit():
            messagebox.showerror("Error", "Los días deben ser un número entero")
            return

        c_id = self.customers_map[c_text]
        v_id = self.vehicles_map[v_text]

        ok, msg = RentalLogic.create_rental(c_id, v_id, days)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.load_combos() # Recargar combos (el carro ya no debe salir)
            self.load_data()
            self.entry_days.delete(0, tk.END)
            self.combo_vehicles.set('')
        else:
            messagebox.showerror("Error", msg)

    def end_rental(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una renta activa para finalizarla")
            return
        
        item = self.tree.item(sel[0])
        rental_id = item['values'][0]
        vehicle_id = item['values'][6] # Columna oculta
        
        if messagebox.askyesno("Confirmar", "¿El vehículo ha sido devuelto?"):
            ok, msg = RentalLogic.finalize_rental(rental_id, vehicle_id)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.load_data()
                self.load_combos() # El vehículo vuelve a estar disponible
            else:
                messagebox.showerror("Error", msg)