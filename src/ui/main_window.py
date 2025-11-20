import tkinter as tk
from tkinter import messagebox
# Asegúrate de que este archivo (customers_window.py) exista también
from src.ui.customers_window import CustomersWindow

class MainWindow(tk.Toplevel):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.user_data = user_data
        self.role = user_data['role_name']
        
        # Configuración de la ventana
        self.title(f"AutoPy System - Usuario: {self.user_data['user_name']}")
        self.geometry("1024x768")
        
        # Maximizar ventana (compatible con Windows)
        self.state('zoomed') 
        
        # Protocolo de cierre: Si cierran esta ventana, se apaga todo el sistema
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        # Construcción de la interfaz
        self.create_menu()
        self.create_dashboard()

    def quit_app(self):
        if messagebox.askokcancel("Salir", "¿Desea salir del sistema?"):
            self.master.destroy() # Cierra la raíz oculta y termina el programa

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        # --- MENU ARCHIVO ---
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Salir", command=self.quit_app)

        # --- MENU GESTIÓN ---
        crud_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Gestión", menu=crud_menu)
        
        # Botones para abrir los formularios
        crud_menu.add_command(label="Clientes", command=lambda: self.open_crud("Clientes"))
        crud_menu.add_command(label="Vehículos", command=lambda: self.open_crud("Vehículos"))
        crud_menu.add_command(label="Rentas", command=lambda: self.open_crud("Rentas"))
        
        # --- MENU AYUDA ---
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=lambda: messagebox.showinfo("AutoPy", "Sistema de Rentas v1.0"))

    def create_dashboard(self):
        frame = tk.Frame(self, bg="#f0f0f0")
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text=f"Bienvenido al Sistema AutoPy", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
        tk.Label(frame, text=f"Panel de Control - Rol: {self.role}", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)

    def open_crud(self, module_name):
        if module_name == "Clientes":
            # Abre la ventana de Clientes pasando 'self' como padre
            CustomersWindow(self)
        else:
            messagebox.showinfo("En construcción", f"El módulo de {module_name} aún no está listo.")