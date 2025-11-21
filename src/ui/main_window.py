import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import os

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
        
        # --- PALETA DE COLORES ---
        self.color_header = "#1a1a1a"
        self.color_bg = "#F4F6F9"
        self.color_card = "#FFFFFF"
        self.color_text = "#333333"
        self.color_accent = "#D60000" 
        self.color_btn_hover = "#333333"
        
        self.title(f"AutoPy System - {self.user_data['user_name']}")
        self.geometry("1200x800")
        self.state('zoomed') 
        self.configure(bg=self.color_bg)
        
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.create_header()
        self.create_dashboard_content()

    def quit_app(self):
        if messagebox.askokcancel("Salir", "¿Desea cerrar el sistema?"):
            self.master.destroy()

    def create_header(self):
       
        header = tk.Frame(self, bg=self.color_header, height=70)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        left_frame = tk.Frame(header, bg=self.color_header)
        left_frame.pack(side="left", padx=20)

        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            img_path = os.path.join(base_dir, "assets", "logo.jpg")
            pil_img = Image.open(img_path)
            pil_img = pil_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.logo_icon = ImageTk.PhotoImage(pil_img)
            tk.Label(left_frame, image=self.logo_icon, bg=self.color_header, bd=0).pack(side="left", padx=(0, 10))
        except:
            pass

        tk.Label(left_frame, text="AUTOPY", font=("Segoe UI", 16, "bold"), bg=self.color_header, fg="#FFFFFF").pack(side="left")

        nav_frame = tk.Frame(header, bg=self.color_header)
        nav_frame.pack(side="left", padx=50)

        self.create_nav_btn(nav_frame, "VEHÍCULOS", lambda: self.open_crud("Vehículos"))
        self.create_nav_btn(nav_frame, "CLIENTES", lambda: self.open_crud("Clientes"))
        self.create_nav_btn(nav_frame, "RENTAS", lambda: self.open_crud("Rentas"))
        self.create_nav_btn(nav_frame, "REPORTES", self.show_reports_menu) # Menú desplegable simulado

        right_frame = tk.Frame(header, bg=self.color_header)
        right_frame.pack(side="right", padx=20)

        if self.role == "Administrador":
             self.create_icon_btn(right_frame, "⚙️", self.show_admin_menu)

        self.create_icon_btn(right_frame, "❓", self.open_help)

       
        tk.Frame(right_frame, bg="#555", width=1, height=30).pack(side="left", padx=15)

    
        tk.Label(right_frame, text=self.user_data['user_name'].upper(), font=("Segoe UI", 10, "bold"), 
                 bg=self.color_header, fg="white").pack(side="left")
        
        tk.Button(right_frame, text="SALIR", font=("Segoe UI", 8, "bold"), bg=self.color_accent, fg="white", 
                  relief="flat", cursor="hand2", padx=10, command=self.quit_app).pack(side="left", padx=15)

    def create_nav_btn(self, parent, text, command):
        """Crea un botón de navegación estilo Web"""
        btn = tk.Button(parent, text=text, font=("Segoe UI", 10, "bold"), 
                        bg=self.color_header, fg="#cccccc", 
                        activebackground=self.color_btn_hover, activeforeground="white",
                        relief="flat", cursor="hand2", bd=0, padx=15, pady=10,
                        command=command)
        btn.pack(side="left")
        
        btn.bind("<Enter>", lambda e: btn.config(bg=self.color_btn_hover, fg="white"))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.color_header, fg="#cccccc"))

    def create_icon_btn(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 12), 
                        bg=self.color_header, fg="white", 
                        activebackground=self.color_btn_hover,
                        relief="flat", cursor="hand2", bd=0, padx=5,
                        command=command)
        btn.pack(side="left")

    def create_dashboard_content(self):
        container = tk.Frame(self, bg=self.color_bg)
        container.pack(fill="both", expand=True, padx=50, pady=40)

        tk.Label(container, text="Panel de Control", font=("Segoe UI", 20, "bold"), bg=self.color_bg, fg="#333").pack(anchor="w", pady=(0, 20))
        
        grid_frame = tk.Frame(container, bg=self.color_bg)
        grid_frame.pack(fill="x")

        self.create_card(grid_frame, 0, 0, "🚗", "Flota Vehicular", "Administrar autos", "#20c997", lambda: self.open_crud("Vehículos"))
        self.create_card(grid_frame, 0, 1, "👥", "Clientes", "Base de datos", "#17a2b8", lambda: self.open_crud("Clientes"))
        self.create_card(grid_frame, 0, 2, "🔑", "Nueva Renta", "Procesar alquiler", "#007bff", lambda: self.open_crud("Rentas"))
        
        status_frame = tk.Frame(self, bg="white", height=30)
        status_frame.pack(side="bottom", fill="x")
        tk.Label(status_frame, text=f"Sistema listo. Conectado como {self.role}", font=("Segoe UI", 9), bg="white", fg="#666").pack(side="right", padx=20)

    def create_card(self, parent, row, col, icon, title, subtitle, color, cmd):
        card = tk.Frame(parent, bg=self.color_card, padx=20, pady=20)
        card.grid(row=row, column=col, padx=15, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Frame(card, bg=color, height=4).pack(fill="x", side="top", pady=(0, 15))
        
        tk.Label(card, text=icon, font=("Segoe UI", 32), bg=self.color_card).pack()
        tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), bg=self.color_card, fg="#333").pack(pady=5)
        tk.Label(card, text=subtitle, font=("Segoe UI", 9), bg=self.color_card, fg="#888").pack(pady=(0, 15))
        
        tk.Button(card, text="Acceder", bg=color, fg="white", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=cmd).pack(fill="x")
    
    def show_reports_menu(self):
        # Crea un menú flotante 
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Inventario de Vehículos", command=ReportService.export_simple_vehicles)
        menu.add_command(label="Clientes y Rentas (Maestro)", command=ReportService.export_master_detail)
        menu.add_command(label="Rentas por Fechas", command=self.ask_date_report)
        
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def show_admin_menu(self):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Crear Respaldo BD", command=BackupService.create_backup)
        menu.add_command(label="Restaurar BD", command=BackupService.restore_backup)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def open_crud(self, module_name):
        if module_name == "Clientes": CustomersWindow(self)
        elif module_name == "Vehículos": VehiclesWindow(self)
        elif module_name == "Rentas": RentalsWindow(self)

    def ask_date_report(self):
        start = simpledialog.askstring("Reporte", "Fecha Inicio (YYYY-MM-DD):", parent=self)
        if start:
            end = simpledialog.askstring("Reporte", "Fecha Fin (YYYY-MM-DD):", parent=self)
            if end: ReportService.export_parameterized(start, end)

    def open_help(self):
        HelpWindow(self)