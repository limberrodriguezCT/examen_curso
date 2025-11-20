import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.customer_logic import CustomerLogic

class CustomersWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Clientes")
        self.geometry("1100x700")
        self.config(bg="#F4F6F9") # Fondo suave del Dashboard
        
        # --- ESTILOS DE LA TABLA (Treeview) ---
        self.style = ttk.Style()
        self.style.theme_use("clam") # 'clam' permite personalizar colores mejor que 'vista'
        
        # Encabezados de tabla
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), 
                             background="#343a40", foreground="white", relief="flat")
        self.style.map("Treeview.Heading", background=[('active', '#23272b')])
        
        # Cuerpo de tabla
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, 
                             background="white", fieldbackground="white")
        self.style.map("Treeview", background=[('selected', '#007bff')]) # Azul al seleccionar

        self.create_header()
        self.create_form()
        self.create_table()
        self.load_data()

    def create_header(self):
        # Título superior
        header_frame = tk.Frame(self, bg="#F4F6F9")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(header_frame, text="👥 Directorio de Clientes", font=("Segoe UI", 20, "bold"), 
                 bg="#F4F6F9", fg="#333").pack(side="left")

    def create_form(self):
        # Tarjeta blanca para el formulario
        card = tk.Frame(self, bg="white", padx=20, pady=20)
        card.pack(fill="x", padx=20, pady=5)
        
        # Variables
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_doc = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_address = tk.StringVar()
        self.var_gender = tk.StringVar(value="M")

        # Grid Layout
        # Fila 1
        self.create_label_entry(card, "Nombre Completo:", self.var_name, 0, 0, width=40)
        self.create_label_entry(card, "No. Documento:", self.var_doc, 0, 2)
        
        # Fila 2
        self.create_label_entry(card, "Teléfono:", self.var_phone, 1, 0)
        
        tk.Label(card, text="Género:", font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=1, column=2, sticky="w", pady=5)
        ttk.Combobox(card, textvariable=self.var_gender, values=["M", "F"], state="readonly", width=18).grid(row=1, column=3, sticky="w", padx=5)

        # Fila 3 (Dirección ocupa más espacio)
        tk.Label(card, text="Dirección:", font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(card, textvariable=self.var_address, font=("Segoe UI", 10), bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#ddd").grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, ipady=5)

        # Botones de Acción
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=(20, 0), sticky="e")

        self.create_button(btn_frame, "Guardar", "#28a745", self.save)
        self.create_button(btn_frame, "Actualizar", "#17a2b8", self.update)
        self.create_button(btn_frame, "Eliminar", "#dc3545", self.delete)
        self.create_button(btn_frame, "Limpiar", "#6c757d", self.clear_form)

    def create_label_entry(self, parent, text, variable, row, col, width=20):
        tk.Label(parent, text=text, font=("Segoe UI", 9, "bold"), bg="white", fg="#555").grid(row=row, column=col, sticky="w", pady=5)
        e = tk.Entry(parent, textvariable=variable, width=width, font=("Segoe UI", 10), 
                     bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#ddd")
        e.grid(row=row, column=col+1, sticky="w", padx=5, pady=5, ipady=5)

    def create_button(self, parent, text, color, command):
        tk.Button(parent, text=text, bg=color, fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", cursor="hand2", padx=15, pady=5, command=command).pack(side="left", padx=5)

    def create_table(self):
        frame_table = tk.Frame(self, bg="white")