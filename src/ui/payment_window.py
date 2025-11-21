import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.payment_logic import PaymentLogic
from src.logic.rental_logic import RentalLogic # Para listar rentas activas

class PaymentWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Caja - Registro de Pagos")
        self.geometry("900x600")
        self.config(bg="#F4F6F9")
        
        # Estilos (Mismos que antes)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#343a40", foreground="white", relief="flat")
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)

        self.rentals_map = {}
        
        self.create_header()
        self.create_form()
        self.create_table()
        self.load_rentals()
        self.load_data()

    def create_header(self):
        h = tk.Frame(self, bg="#F4F6F9")
        h.pack(fill="x", padx=20, pady=10)
        tk.Label(h, text="💰 Registro de Pagos", font=("Segoe UI", 20, "bold"), bg="#F4F6F9", fg="#333").pack(side="left")

    def create_form(self):
        card = tk.Frame(self, bg="white", padx=20, pady=20)
        card.pack(fill="x", padx=20, pady=5)

        tk.Label(card, text="Renta / Cliente:", font=("Segoe UI", 9, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        self.combo_rent = ttk.Combobox(card, state="readonly", width=40)
        self.combo_rent.grid(row=0, column=1, padx=10)

        tk.Label(card, text="Monto a Pagar:", font=("Segoe UI", 9, "bold"), bg="white").grid(row=0, column=2, sticky="w")
        self.entry_amount = tk.Entry(card, width=15, bg="#f8f9fa", relief="flat", highlightthickness=1)
        self.entry_amount.grid(row=0, column=3, padx=10, ipady=3)

        tk.Button(card, text="REGISTRAR PAGO", bg="#007bff", fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", cursor="hand2", command=self.save).grid(row=0, column=4, padx=20)

    def create_table(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        cols = ("id", "fecha", "monto", "moneda", "cliente", "placa")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        headers = ["ID Pago", "Fecha", "Monto", "Moneda", "Cliente", "Vehículo"]
        for c, h in zip(cols, headers):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=100)
            
        self.tree.pack(side="left", fill="both", expand=True)
        sc = ttk.Scrollbar(frame, command=self.tree.yview); self.tree.configure(yscroll=sc.set); sc.pack(side="right", fill="y")

    def load_rentals(self):
        # Listamos las rentas activas para cobrar
        rows = RentalLogic.read_all_active()
        self.rentals_map = {}
        self.combo_rent['values'] = []
        values = []
        for r in rows:
            # r[0] = id, r[1] = cliente, r[3] = placa (segun tu rental_logic)
            display = f"Renta #{r['rental_id']} - {r['cliente_nombre']} ({r['placa']})"
            values.append(display)
            self.rentals_map[display] = r['rental_id']
        self.combo_rent['values'] = values

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        rows = PaymentLogic.read_all()
        for r in rows:
            self.tree.insert("", "end", values=(r['id'], r['payment_date'], f"{r['amount']}", r['currency'], r['full_name'], r['plate_number']))

    def save(self):
        r_txt = self.combo_rent.get()
        amt = self.entry_amount.get()
        if not r_txt or not amt: return
        
        r_id = self.rentals_map[r_txt]
        ok, msg = PaymentLogic.create_payment(r_id, amt)
        if ok:
            messagebox.showinfo("Exito", msg)
            self.load_data()
            self.entry_amount.delete(0, "end")
        else:
            messagebox.showerror("Error", msg)