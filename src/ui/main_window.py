import tkinter as tk
from tkinter import messagebox, simpledialog
from src.ui.rentals_window import RentalsWindow
from src.ui.customers_window import CustomersWindow
from src.ui.vehicles_window import VehiclesWindow  # <--- ESTA ERA LA QUE FALTABA
from src.logic.reports import ReportService

class MainWindow(tk.Toplevel):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.user_data = user_data
        self.role = user_data['role_name']
        
        self.title(f"AutoPy System - Usuario: {self.user_data['user_name']}")
        self.geometry("1024x768")
        self.state('zoomed') 
        
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.create_menu()
        self.create_dashboard()

    def quit_app(self):
        if messagebox.askokcancel("Salir", "¿Desea salir del sistema?"):
            self.master.destroy()

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
        crud_menu.add_command(label="Clientes", command=lambda: self.open_crud("Clientes"))
        crud_menu.add_command(label="Vehículos", command=lambda: self.open_crud("Vehículos"))
        crud_menu.add_command(label="Rentas", command=lambda: self.open_crud("Rentas"))

        # --- MENU REPORTES ---
        report_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Reportes", menu=report_menu)
        
        report_menu.add_command(label="Inventario Vehículos (Sencillo)", 
                                command=ReportService.export_simple_vehicles)
        
        report_menu.add_command(label="Clientes y Rentas (Maestro-Detalle)", 
                                command=ReportService.export_master_detail)
        
        report_menu.add_command(label="Rentas por Fecha (Parametrizado)", 
                                command=self.ask_date_report)
        
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
        # Aquí estaba el error visual. Al pegar esto completo se arregla la indentación.
        if module_name == "Clientes":
            CustomersWindow(self)
        elif module_name == "Vehículos":
            VehiclesWindow(self)
        elif module_name == "Rentas":
            RentalsWindow(self)
            

    def ask_date_report(self):
        start_date = simpledialog.askstring("Reporte", "Fecha Inicio (YYYY-MM-DD):", parent=self)
        if not start_date: return
        
        end_date = simpledialog.askstring("Reporte", "Fecha Fin (YYYY-MM-DD):", parent=self)
        if not end_date: return
        
        ReportService.export_parameterized(start_date, end_date)