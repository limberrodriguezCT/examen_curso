import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.payment_logic import PaymentLogic
from src.logic.rental_logic import RentalLogic

class PaymentWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Caja y Pagos")
        self.geometry("1000x700")
        self.config(bg="#F4F6F9")
        
        # --- ESTILOS VISUALES ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        # Forzamos colores de alto contraste
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#343a40", foreground="white", relief="flat")
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, background="white", foreground="black", fieldbackground="white")
        self.style.map("Treeview", background=[('selected', '#007bff')], foreground=[('selected', 'white')])

        self.rentals_map = {}
        
        # Construcción de interfaz vertical (Pack es más seguro que Grid aquí)
        self.create_header()
        self.create_form_area()
        self.create_table_area()
        
        # Carga de datos
        try:
            self.load_rentals()
            self.load_data()
        except Exception as e:
            print(f"Error inicializando ventana: {e}")

    def create_header(self):
        h = tk.Frame(self, bg="#F4F6F9")
        h.pack(fill="x", padx=20, pady=15)
        tk.Label(h, text="💰 Registro de Pagos", font=("Segoe UI", 22, "bold"), bg="#F4F6F9", fg="#333").pack(side="left")

    def create_form_area(self):
        # Tarjeta Blanca
        card = tk.Frame(self, bg="white", padx=20, pady=20)
        card.pack(fill="x", padx=20, pady=5)

        self.var_id = tk.StringVar() # ID oculto para editar

        # --- SECCIÓN DE INPUTS ---
        inputs_frame = tk.Frame(card, bg="white")
        inputs_frame.pack(fill="x", pady=(0, 15))

        # Combo Renta
        tk.Label(inputs_frame, text="Seleccionar Renta Pendiente:", font=("Segoe UI", 9, "bold"), bg="white").pack(anchor="w")
        self.combo_rent = ttk.Combobox(inputs_frame, state="readonly", width=50, font=("Segoe UI", 10))
        self.combo_rent.pack(anchor="w", pady=(5, 15), ipady=3)

        # Input Monto
        tk.Label(inputs_frame, text="Monto a Pagar ($):", font=("Segoe UI", 9, "bold"), bg="white").pack(anchor="w")
        self.entry_amount = tk.Entry(inputs_frame, width=20, font=("Segoe UI", 11), bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        self.entry_amount.pack(anchor="w", pady=(5, 5), ipady=3)

        # --- SECCIÓN DE BOTONES (CRUD) ---
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill="x", pady=10)

        # Botones grandes y claros
        self.create_btn(btn_frame, "✅ REGISTRAR PAGO", "#28a745", self.save)
        self.create_btn(btn_frame, "🔄 ACTUALIZAR", "#17a2b8", self.update)
        self.create_btn(btn_frame, "🗑 ELIMINAR", "#dc3545", self.delete)
        self.create_btn(btn_frame, "🧹 LIMPIAR", "#6c757d", self.clear)

    def create_btn(self, parent, text, color, cmd):
        tk.Button(parent, text=text, bg=color, fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", cursor="hand2", padx=20, pady=8, command=cmd).pack(side="left", padx=(0, 10))

    def create_table_area(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Historial de Pagos Recibidos", font=("Segoe UI", 11, "bold"), bg="white", fg="#555").pack(anchor="w", pady=(0, 10))

        # Tabla
        cols = ("id", "fecha", "monto", "moneda", "cliente", "placa", "rid")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        headers = ["ID", "Fecha Pago", "Monto", "Moneda", "Cliente", "Vehículo"]
        widths = [50, 150, 100, 80, 200, 100]
        
        for c, h, w in zip(cols[:-1], headers, widths):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w)
            
        self.tree.column("rid", width=0, stretch=False) # Ocultar ID Renta

        self.tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        sc = ttk.Scrollbar(frame, command=self.tree.yview)
        self.tree.configure(yscroll=sc.set)
        sc.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

    def load_rentals(self):
        rows = RentalLogic.read_all_active()
        self.rentals_map = {}
        self.combo_rent['values'] = []
        values = []
        for r in rows:
            # r[0]=rental_id, r[1]=cliente, r[3]=placa (Según índices del SQL)
            display = f"Renta #{r[0]} - {r[1]} ({r[3]})"
            values.append(display)
            self.rentals_map[display] = r[0]
        self.combo_rent['values'] = values

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        rows = PaymentLogic.read_all()
        
        # Debug en consola
        print(f"[DEBUG UI] Cargando {len(rows)} filas en la tabla de pagos.")
        
        for r in rows:
            # Usamos índices numéricos r[0], r[1] para máxima seguridad
            self.tree.insert("", "end", values=(
                r[0], # ID
                r[1], # Fecha
                f"${r[2]}", # Monto
                r[3], # Moneda
                r[4], # Cliente
                r[5], # Placa
                r[6]  # Rental ID
            ))

    def select_item(self, event):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            vals = item['values']
            self.var_id.set(vals[0])
            
            # Recuperar monto limpio (sin $)
            amt = str(vals[2]).replace("$", "")
            self.entry_amount.delete(0, tk.END)
            self.entry_amount.insert(0, amt)
            # Nota: No seleccionamos el combo automáticamente porque la renta podría no estar activa ya

    def save(self):
        r_txt = self.combo_rent.get()
        amt = self.entry_amount.get()
        
        if not r_txt:
            messagebox.showwarning("Atención", "Debe seleccionar una Renta activa.")
            return
        if not amt:
            messagebox.showwarning("Atención", "Ingrese el monto.")
            return
        
        r_id = self.rentals_map[r_txt]
        ok, msg = PaymentLogic.create_payment(r_id, amt)
        if ok:
            messagebox.showinfo("Exito", msg)
            self.load_data()
            self.entry_amount.delete(0, "end")
        else:
            messagebox.showerror("Error", msg)

    def update(self):
        if not self.var_id.get(): 
            messagebox.showwarning("Atención", "Seleccione un pago de la tabla para editar.")
            return
        
        ok, msg = PaymentLogic.update(self.var_id.get(), self.entry_amount.get())
        if ok:
            messagebox.showinfo("Actualizado", msg)
            self.load_data()
            self.clear()

    def delete(self):
        if not self.var_id.get(): return
        if messagebox.askyesno("Confirmar", "¿Eliminar este registro de pago?"):
            ok, msg = PaymentLogic.delete(self.var_id.get())
            if ok: self.load_data(); self.clear()

    def clear(self):
        self.var_id.set("")
        self.combo_rent.set("")
        self.entry_amount.delete(0, tk.END)