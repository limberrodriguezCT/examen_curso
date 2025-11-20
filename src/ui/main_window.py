from src.ui.customers_window import CustomersWindow

def open_crud(self, module_name):
    if module_name == "Clientes":
        CustomersWindow(self) # Abre la ventana nueva
    elif module_name == "Vehículos":
        messagebox.showinfo("Pendiente", "Formulario de Vehículos en construcción")
    elif module_name == "Rentas":
        messagebox.showinfo("Pendiente", "Formulario de Rentas en construcción")
        
        