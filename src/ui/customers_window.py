import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.customer_logic import CustomerLogic

class CustomersWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Clientes")
        self.geometry("900x600")
        self.config(bg="#f4f4f4")
        
        self.create_toolbar()
        self.create_form()
        self.create_table()
        self.load_data()

    def create_toolbar(self):
        # Cumple con el punto "Barra de Herramientas" de la Rúbrica
        toolbar = tk.Frame(self, bg="#ddd", height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        btn_help = tk.Button(toolbar, text="Ayuda (?)", command=self.show_help, bg="#ddd", relief=tk.FLAT)
        btn_help.pack(side=tk.RIGHT, padx=10)

    def create_form(self):
        frame_form = tk.LabelFrame(self, text="Datos del Cliente", bg="white", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        # Variables
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_doc = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_address = tk.StringVar()
        self.var_gender = tk.StringVar(value="M")

        # Inputs
        tk.Label(frame_form, text="Nombre Completo:", bg="white").grid(row=0, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_name, width=30).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="No. Documento:", bg="white").grid(row=0, column=2, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_doc, width=20).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Teléfono:", bg="white").grid(row=1, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_phone, width=20).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Género:", bg="white").grid(row=1, column=2, sticky="w")
        tk.OptionMenu(frame_form, self.var_gender, "M", "F").grid(row=1, column=3, sticky="w")

        tk.Label(frame_form, text="Dirección:", bg="white").grid(row=2, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_address, width=50).grid(row=2, column=1, columnspan=3, sticky="w", padx=5)

        # Botones de Acción (CRUD)
        frame_buttons = tk.Frame(frame_form, bg="white")
        frame_buttons.grid(row=3, column=0, columnspan=4, pady=10)

        tk.Button(frame_buttons, text="Guardar", bg="#28a745", fg="white", width=12, command=self.save).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Actualizar", bg="#ffc107", width=12, command=self.update).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Eliminar", bg="#dc3545", fg="white", width=12, command=self.delete).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Limpiar", bg="#6c757d", fg="white", width=12, command=self.clear_form).pack(side=tk.LEFT, padx=5)

    def create_table(self):
        frame_table = tk.Frame(self)
        frame_table.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "nombre", "doc", "genero", "telefono", "direccion")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")
        
        # Encabezados
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre Completo")
        self.tree.heading("doc", text="Documento")
        self.tree.heading("genero", text="Sexo")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("direccion", text="Dirección")

        # Anchos
        self.tree.column("id", width=30)
        self.tree.column("nombre", width=200)
        self.tree.column("doc", width=100)
        self.tree.column("genero", width=50)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

    def load_data(self):
        # Limpiar tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Traer datos de la BD
        rows = CustomerLogic.read_all()
        for row in rows:
            # Convertir row (sqlite3.Row) a tupla
            self.tree.insert("", tk.END, values=(row['id'], row['full_name'], row['document_number'], row['gender'], row['number_telephone'], row['address']))

    def select_item(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            vals = item['values']
            # Llenar formulario
            self.var_id.set(vals[0])
            self.var_name.set(vals[1])
            self.var_doc.set(vals[2])
            self.var_gender.set(vals[3])
            self.var_phone.set(vals[4])
            self.var_address.set(vals[5])

    def save(self):
        if not self.var_name.get() or not self.var_doc.get():
            messagebox.showwarning("Error", "Nombre y Documento son obligatorios")
            return

        ok, msg = CustomerLogic.create(
            self.var_name.get(), self.var_doc.get(), self.var_gender.get(), 
            self.var_phone.get(), self.var_address.get()
        )
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", msg)

    def update(self):
        if not self.var_id.get():
            messagebox.showwarning("Error", "Seleccione un cliente para actualizar")
            return
        
        ok, msg = CustomerLogic.update(
            self.var_id.get(), self.var_name.get(), self.var_doc.get(), 
            self.var_gender.get(), self.var_phone.get(), self.var_address.get()
        )
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", msg)

    def delete(self):
        if not self.var_id.get():
            messagebox.showwarning("Error", "Seleccione un cliente para eliminar")
            return
        
        confirm = messagebox.askyesno("Confirmar", "¿Realmente desea eliminar este cliente?")
        if confirm:
            ok, msg = CustomerLogic.delete(self.var_id.get())
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", msg)

    def clear_form(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_doc.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_gender.set("M")

    def show_help(self):
        messagebox.showinfo("Ayuda", "Llene los campos y presione Guardar.\nPara editar, seleccione de la tabla.")

if __name__ == "__main__":
    # Prueba unitaria visual
    root = tk.Tk()
    app = CustomersWindow(root)
    root.mainloop()