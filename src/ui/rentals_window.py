import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.rental_logic import RentalLogic

class RentalsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Procesar Rentas")
        self.geometry("1100x750")
        self.config(bg="#F4F6F9")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Encabezados oscuros
        self.style.configure("Treeview.Heading", 
                             font=("Segoe UI", 10, "bold"), 
                             background="#343a40", 
                             foreground="white", 
                             relief="flat")
        
        # Filas blancas con letra negra
        self.style.configure("Treeview", 
                             font=("Segoe UI", 10), 
                             rowheight=35, 
                             background="white", 
                             foreground="black",
                             fieldbackground="white")
        
        # Selección azul
        self.style.map("Treeview", 
                       background=[('selected', '#007bff')], 
                       foreground=[('selected', 'white')])

        self.customers_map = {}
        self.vehicles_map = {}
        
        self.create_header()
        self.create_form()
        self.create_table()
        
        try:
            self.load_combos()
            self.load_data()
        except Exception as e:
            print(f"Error inicializando datos: {e}")

    def create_header(self):
        h = tk.Frame(self, bg="#F4F6F9")
        h.pack(fill="x", padx=20, pady=(20,10))
        tk.Label(h, text=" Mostrador de Rentas", font=("Segoe UI", 20, "bold"), bg="#F4F6F9", fg="#333").pack(side="left")

    def create_form(self):
        card = tk.Frame(self, bg="white", padx=25, pady=25)
        card.pack(fill="x", padx=20, pady=5)
        
        tk.Label(card, text="Nueva Solicitud de Alquiler", font=("Segoe UI", 12, "bold"), bg="white", fg="#007bff").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        tk.Label(card, text="Seleccionar Cliente:", font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=1, column=0, sticky="w")
        self.combo_customers = ttk.Combobox(card, width=35, state="readonly", font=("Segoe UI", 10))
        self.combo_customers.grid(row=1, column=1, sticky="w", padx=10, ipady=3)

        tk.Label(card, text="Vehículo Disponible:", font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=1, column=2, sticky="w")
        self.combo_vehicles = ttk.Combobox(card, width=35, state="readonly", font=("Segoe UI", 10))
        self.combo_vehicles.grid(row=1, column=3, sticky="w", padx=10, ipady=3)

        tk.Label(card, text="Días a Rentar:", font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=2, column=0, sticky="w", pady=20)
        self.entry_days = tk.Entry(card, width=10, font=("Segoe UI", 12), bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#ccc", fg="black")
        self.entry_days.grid(row=2, column=1, sticky="w", padx=10, ipady=5)

        tk.Button(card, text="Confirmar y Registrar", bg="#007bff", fg="white", font=("Segoe UI", 11, "bold"), 
                  relief="flat", cursor="hand2", padx=20, pady=10, command=self.save_rental).grid(row=2, column=2, columnspan=2, sticky="e")

    def create_table(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        top_bar = tk.Frame(frame, bg="white")
        top_bar.pack(fill="x", pady=(0, 10))
        tk.Label(top_bar, text="Vehículos actualmente en calle (Activos)", font=("Segoe UI", 11, "bold"), bg="white", fg="#555").pack(side="left")
        
        tk.Button(top_bar, text="FINALIZAR RENTA SELECCIONADA", bg="#dc3545", fg="white", 
                  font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", padx=10, pady=5, 
                  command=self.end_rental).pack(side="right")

        # Definición de columnas
        cols = ("id", "cliente", "vehiculo", "placa", "fecha", "total", "vid")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        headers = ["ID", "Cliente", "Vehículo", "Placa", "Fecha Salida", "Total ($)"]
        widths = [50, 200, 150, 100, 150, 100]
        
        for c, h, w in zip(cols[:-1], headers, widths):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w)
        
        self.tree.column("vid", width=0, stretch=False)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        sc = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=sc.set)
        sc.pack(side=tk.RIGHT, fill=tk.Y)

    def load_combos(self):
        customers = RentalLogic.get_customers()
        self.customers_map = {f"{c['full_name']}": c['id'] for c in customers}
        self.combo_customers['values'] = list(self.customers_map.keys())

        vehicles = RentalLogic.get_available_vehicles()
        self.vehicles_map = {f"{v['model']} - {v['plate_number']} (${v['daily_rate']})": v['id'] for v in vehicles}
        self.combo_vehicles['values'] = list(self.vehicles_map.keys())

    def load_data(self):
        # 1. Limpiar
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 2. Traer datos
        rows = RentalLogic.read_all_active()
        
       
        for r in rows:
            try:
                self.tree.insert("", tk.END, values=(
                    r[0], # Rental ID
                    r[1], # Cliente Nombre
                    r[2], # Vehiculo Modelo
                    r[3], # Placa
                    r[4], # Fecha
                    f"${r[5]}", # Total
                    r[6]  # Vehicle ID (Oculto)
                ))
            except Exception as e:
                print(f"Error visual al insertar fila: {e}")

    def save_rental(self):
        c_txt = self.combo_customers.get()
        v_txt = self.combo_vehicles.get()
        days = self.entry_days.get()
        
        if not c_txt or not v_txt or not days: 
            messagebox.showwarning("Atención", "Llene todos los campos")
            return
        
        c_id = self.customers_map[c_txt]
        v_id = self.vehicles_map[v_txt]
        
        ok, msg = RentalLogic.create_rental(c_id, v_id, days)
        if ok:
            messagebox.showinfo("Renta Procesada", msg)
            self.load_combos() 
            self.load_data()   
            self.entry_days.delete(0, tk.END)
            self.combo_customers.set('')
            self.combo_vehicles.set('')
        else:
            messagebox.showerror("Error", msg)

    def end_rental(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Alerta", "Seleccione una renta para finalizar.")
            return
        
        item = self.tree.item(sel[0])
        if messagebox.askyesno("Devolución", f"¿Confirmar devolución del vehículo {item['values'][3]}?"):
            RentalLogic.finalize_rental(item['values'][0], item['values'][6])
            self.load_data()
            self.load_combos()