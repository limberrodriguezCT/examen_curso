import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os

# Importaciones de módulos
from src.ui.customers_window import CustomersWindow
from src.ui.vehicles_window import VehiclesWindow
from src.ui.rentals_window import RentalsWindow
from src.logic.reports import ReportService
from src.logic.backup import BackupService
from src.ui.help_window import HelpWindow

class MainWindow(tk.Toplevel):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.user_data = user_data
        self.role = user_data['role_name']
        
        # --- PALETA DE COLORES PROFESIONAL (Enterprise Theme) ---
        self.color_header = "#1a1a1a"   # Gris casi negro (Elegante, funde el logo)
        self.color_bg = "#F4F6F9"       # Gris azulado muy suave (Estándar en Dashboards modernos)
        self.color_card = "#FFFFFF"     # Blanco puro para las tarjetas
        self.color_text = "#333333"     # Gris oscuro (mejor lectura que negro)
        self.color_primary = "#007bff"  # Azul corporativo (Acciones)
        
        self.title(f"AutoPy System - {self.user_data['user_name']}")
        self.geometry("1024x768")
        self.state('zoomed') 
        self.configure(bg=self.color_bg)
        
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.create_menu()
        self.create_header()
        self.create_dashboard_content()

    def quit_app(self):
        if messagebox.askokcancel("Salir", "¿Desea salir del sistema?"):
            self.master.destroy()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        
        if self.role == "Administrador":
            file_menu.add_command(label="Crear Respaldo (Backup)", command=BackupService.create_backup)
            file_menu.add_command(label="Restaurar Base de Datos", command=BackupService.restore_backup)
            file_menu.add_separator()
            
        file_menu.add_command(label="Cerrar Sesión", command=self.quit_app)

        crud_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Gestión", menu=crud_menu)
        crud_menu.add_command(label="Clientes", command=lambda: self.open_crud("Clientes"))
        crud_menu.add_command(label="Vehículos", command=lambda: self.open_crud("Vehículos"))
        crud_menu.add_command(label="Rentas", command=lambda: self.open_crud("Rentas"))

        report_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Reportes", menu=report_menu)
        report_menu.add_command(label="Inventario Vehículos", command=ReportService.export_simple_vehicles)
        report_menu.add_command(label="Clientes y Rentas", command=ReportService.export_master_detail)
        report_menu.add_command(label="Rentas por Fecha", command=self.ask_date_report)
        
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Manual de Usuario", command=self.open_help)
        help_menu.add_command(label="Acerca de", command=lambda: messagebox.showinfo("AutoPy", "Sistema de Rentas v1.0\nExamen Final"))

    def create_header(self):
        # Header oscuro para mantener identidad con el logo
        header = tk.Frame(self, bg=self.color_header, height=70)
        header.pack(side="top", fill="x")
        header.pack_propagate(False) 

        # Logo
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            img_path = os.path.join(base_dir, "assets", "logo.jpg")
            pil_img = Image.open(img_path)
            pil_img = pil_img.resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_icon = ImageTk.PhotoImage(pil_img)
            
            lbl_logo = tk.Label(header, image=self.logo_icon, bg=self.color_header, bd=0)
            lbl_logo.pack(side="left", padx=(20, 10))
        except:
            pass

        # Título
        tk.Label(header, text="AutoPy Rental", font=("Segoe UI", 16, "bold"), 
                 bg=self.color_header, fg="#FFFFFF").pack(side="left")

        # Info Usuario (Derecha)
        user_frame = tk.Frame(header, bg=self.color_header)
        user_frame.pack(side="right", padx=20)

        tk.Label(user_frame, text=self.user_data['user_name'].title(), font=("Segoe UI", 11, "bold"), 
                 bg=self.color_header, fg="#FFFFFF").pack(anchor="e")
        
        # Etiqueta de Rol (Pequeña)
        role_bg = "#28a745" if self.role == "Administrador" else "#ffc107"
        role_fg = "#ffffff" if self.role == "Administrador" else "#000000"
        
        lbl_role = tk.Label(user_frame, text=f" {self.role} ", font=("Segoe UI", 8), 
                 bg=role_bg, fg=role_fg)
        lbl_role.pack(anchor="e")

    def create_dashboard_content(self):
        container = tk.Frame(self, bg=self.color_bg)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        # Saludo
        tk.Label(container, text=f"Hola, {self.user_data['user_name'].title()}", 
                 font=("Segoe UI", 22, "bold"), bg=self.color_bg, fg=self.color_text).pack(anchor="w")
        
        tk.Label(container, text="¿Qué deseas hacer hoy?", 
                 font=("Segoe UI", 11), bg=self.color_bg, fg="#666666").pack(anchor="w", pady=(0, 20))

        # --- GRID DE TARJETAS ---
        grid_frame = tk.Frame(container, bg=self.color_bg)
        grid_frame.pack(fill="x", pady=10)

        # 1. Vehículos (Verde Esmeralda)
        self.create_card(grid_frame, 0, 0, "🚗", "Vehículos", "Gestionar flota", 
                         "#20c997", lambda: self.open_crud("Vehículos"))
        
        # 2. Clientes (Azul Info)
        self.create_card(grid_frame, 0, 1, "👥", "Clientes", "Base de datos", 
                         "#17a2b8", lambda: self.open_crud("Clientes"))
        
        # 3. Rentas (Azul Primary - Acción principal)
        self.create_card(grid_frame, 0, 2, "🔑", "Nueva Renta", "Registrar alquiler", 
                         "#007bff", lambda: self.open_crud("Rentas"))
        
        # 4. Reportes (Naranja - Administrativo)
        self.create_card(grid_frame, 0, 3, "📈", "Reportes", "Ver estadísticas", 
                         "#fd7e14", self.ask_date_report)

    def create_card(self, parent, row, col, icon, title, subtitle, color_accent, command):
        """
        Crea una 'Tarjeta' visualmente atractiva con borde de color superior.
        """
        card = tk.Frame(parent, bg=self.color_card, padx=20, pady=20)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Línea de acento superior
        tk.Frame(card, bg=color_accent, height=3).pack(fill="x", side="top", pady=(0, 15))

        # Icono
        tk.Label(card, text=icon, font=("Segoe UI", 30), bg=self.color_card, fg=self.color_text).pack()
        
        # Título
        tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), bg=self.color_card, fg=self.color_text).pack(pady=(10, 0))
        
        # Subtítulo
        tk.Label(card, text=subtitle, font=("Segoe UI", 9), bg=self.color_card, fg="#999999").pack(pady=(0, 15))
        
        # Botón
        tk.Button(card, text="Acceder", bg=color_accent, fg="white", relief="flat", 
                  font=("Segoe UI", 9, "bold"), cursor="hand2", command=command).pack(fill="x")

        # Configurar peso del grid para que se estiren
        parent.grid_columnconfigure(col, weight=1)

    def open_crud(self, module_name):
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

    def open_help(self):
        HelpWindow(self)