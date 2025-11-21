import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.customer_logic import CustomerLogic

class CustomersWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Clientes")
        self.geometry("1100x700")
        self.config(bg="#F4F6F9") 
        
        # --- ESTILOS ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), 
                             background="#343a40", foreground="white", relief="flat")
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        self.style.map("Treeview", background=[('selected', '#007bff')])

        # Construimos la interfaz paso a paso
        self.create_header()
        self.create_form()
        self.create_table()
        
        # Cargamos datos al final, protegidos por try/except para que no explote
        try:
            self.load_data()
        except Exception as e:
            print(f"Error cargando datos: {e}")

    def create_header(self):
        header_frame = tk.Frame(self, bg="#F4F6F9")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(header_frame, text="👥 Directorio de Clientes", font=("Segoe UI", 20, "bold"), 
                 bg="#F4F6F9", fg="#333").pack(side="left")

    def create_form(self):
        # Tarjeta blanca contenedora
        card = tk.Frame(self, bg="white", padx=20, pady=20)
        card.pack(fill="x", padx=20, pady=5)
        
        # Variables
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_doc = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_address = tk.StringVar()
        self.var_gender = tk.StringVar(value="M")

        # --- FILA 1 ---
        # Nombre
        tk.Label(card, text="Nombre Completo:", font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(card, textvariable=self.var_name, width=40, font=("Segoe UI", 10), bg="#f8f9fa").grid(row=0, column=1, sticky="w", padx=5, ipady=3)

        # Documento
        tk.Label(card, text="No. Documento:", font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=0, column=2, sticky="w", pady=5, padx=(20, 0))
        tk.Entry(card, textvariable=self.var_doc, width=20, font=("Segoe UI", 10), bg="#f8f9fa").grid(row=0, column=3, sticky="w", padx=5, ipady=3)

        # --- FILA 2 ---
        # Teléfono
        tk.Label(card, text="Teléfono:", font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(card, textvariable=self.var_phone, width=20, font=("Segoe UI", 10), bg="#f8f9fa").grid(row=1, column=1, sticky="w", padx=5, ipady=3)

        # Género
        tk.Label(card, text="Género:", font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=1, column=2, sticky="w", pady=5, padx=(20, 0))
        ttk.Combobox(card, textvariable=self.var_gender, values=["M", "F"], state="readonly", width=18).grid(row=1, column=3, sticky="w", padx=5)

        # --- FILA 3 ---
        # Dirección
        tk.Label(card, text="Dirección:", font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(card, textvariable=self.var_address, font=("Segoe UI", 10), bg="#f8f9fa").grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, ipady=3)

        # --- BOTONES ---
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=(20, 0), sticky="e")

        # Botón Guardar (Verde)
        tk.Button(btn_frame, text="Guardar", bg="#28a745", fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", padx=15, pady=5, cursor="hand2", command=self.save).pack(side="left", padx=5)

        # Botón Actualizar (Azul)
        tk.Button(btn_frame, text="Actualizar", bg="#17a2b8", fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", padx=15, pady=5, cursor="hand2", command=self.update).pack(side="left", padx=5)

        # Botón Eliminar (Rojo)
        tk.Button(btn_frame, text="Eliminar", bg="#dc3545", fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", padx=15, pady=5, cursor="hand2", command=self.delete).pack(side="left", padx=5)

        # Botón Limpiar (Gris)
        tk.Button(btn_frame, text="Limpiar", bg="#6c757d", fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", padx=15, pady=5, cursor="hand2", command=self.clear_form).pack(side="left", padx=5)

    def create_table(self):
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("id", "nombre", "doc", "genero", "telefono", "direccion")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")
        
        # Configuración de columnas
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50)
        
        self.tree.heading("nombre", text="Nombre Completo")
        self.tree.column("nombre", width=250)
        
        self.tree.heading("doc", text="Documento")
        self.tree.column("doc", width=120)
        
        self.tree.heading("genero", text="Género")
        self.tree.column("genero", width=80)
        
        self.tree.heading("telefono", text="Teléfono")
        self.tree.column("telefono", width=120)
        
        self.tree.heading("direccion", text="Dirección")
        self.tree.column("direccion", width=300)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.select_item)

    def load_data(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Traer datos
        rows = CustomerLogic.read_all()
        for row in rows:
            self.tree.insert("", tk.END, values=(
                row['id'], row['full_name'], row['document_number'], 
                row['gender'], row['number_telephone'], row['address']
            ))

    def select_item(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            vals = item['values']
            # Llenar campos
            self.var_id.set(vals[0])
            self.var_name.set(vals[1])
            self.var_doc.set(vals[2])
            self.var_gender.set(vals[3])
            self.var_phone.set(vals[4])
            self.var_address.set(vals[5])

    def save(self):
        if not self.var_name.get(): 
            messagebox.showwarning("Error", "El nombre es obligatorio")
            return
        ok, msg = CustomerLogic.create(
            self.var_name.get(), self.var_doc.get(), self.var_gender.get(), 
            self.var_phone.get(), self.var_address.get()
        )
        if ok: 
            messagebox.showinfo("Éxito", msg)
            self.load_data()
            self.clear_form()
        else: 
            messagebox.showerror("Error", msg)

    def update(self):
        if not self.var_id.get(): return
        ok, msg = CustomerLogic.update(
            self.var_id.get(), self.var_name.get(), self.var_doc.get(), 
            self.var_gender.get(), self.var_phone.get(), self.var_address.get()
        )
        if ok: 
            messagebox.showinfo("Éxito", msg)
            self.load_data()
            self.clear_form()
        else:
            messagebox.showerror("Error", msg)

    def delete(self):
        if not self.var_id.get(): return
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            ok, msg = CustomerLogic.delete(self.var_id.get())
            if ok: 
                self.load_data()
                self.clear_form()
            else: 
                messagebox.showerror("Error", msg)

    def clear_form(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_doc.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_gender.set("M")