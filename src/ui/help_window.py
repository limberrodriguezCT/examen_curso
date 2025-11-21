import tkinter as tk
from tkinter import ttk

class HelpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Centro de Ayuda")
        self.geometry("800x600")
        self.config(bg="#F4F6F9")
        self.resizable(False, False)
        
        # Estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TNotebook', background='#F4F6F9', borderwidth=0)
        self.style.configure('TNotebook.Tab', 
                             font=('Segoe UI', 10, 'bold'), 
                             padding=[15, 5], 
                             background='#e9ecef', 
                             foreground='#555')
        
        self.style.map('TNotebook.Tab', 
                       background=[('selected', '#007bff')], 
                       foreground=[('selected', 'white')],
                       expand=[('selected', [1, 1, 1, 0])])

        self.create_header()
        self.create_tabs()
        self.create_footer()

    def create_header(self):
        header = tk.Frame(self, bg="#1a1a1a", height=60)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="Manual de Usuario & Documentación", 
                 font=("Segoe UI", 14, "bold"), bg="#1a1a1a", fg="white").pack(side="left", padx=20)

    def create_tabs(self):
        container = tk.Frame(self, bg="#F4F6F9")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)

        # Pestañas (Sin emojis en los títulos para evitar errores)
        tab1 = tk.Frame(notebook, bg="white")
        notebook.add(tab1, text="  Inicio  ")
        self.build_home_tab(tab1)

        tab2 = tk.Frame(notebook, bg="white")
        notebook.add(tab2, text="  Gestión  ")
        self.build_gestion_tab(tab2)

        tab3 = tk.Frame(notebook, bg="white")
        notebook.add(tab3, text="  Rentas  ")
        self.build_rentas_tab(tab3)

        tab4 = tk.Frame(notebook, bg="white")
        notebook.add(tab4, text="  Admin  ")
        self.build_admin_tab(tab4)

    def build_home_tab(self, parent):
        tk.Label(parent, text="Bienvenido al Sistema AutoPy", 
                 font=("Segoe UI", 18, "bold"), bg="white", fg="#007bff").pack(pady=(40, 10))
        
        desc = ("Este sistema permite gestionar una agencia de renta de autos.\n"
                "Use el menú superior para navegar entre las opciones.")
        tk.Label(parent, text=desc, font=("Segoe UI", 11), bg="white", fg="#555").pack()

        info_frame = tk.Frame(parent, bg="#f8f9fa", padx=20, pady=20)
        info_frame.pack(pady=30, fill="x", padx=40)
        
        # Reemplazado el emoji de foco por texto
        tk.Label(info_frame, text="CONSEJOS RÁPIDOS:", font=("Segoe UI", 10, "bold"), bg="#f8f9fa").pack(anchor="w")
        tips = [
            "• Use el menú superior para navegar entre módulos.",
            "• Los campos obligatorios son validados automáticamente.",
            "• Puede generar reportes Excel en cualquier momento."
        ]
        for tip in tips:
            tk.Label(info_frame, text=tip, font=("Segoe UI", 10), bg="#f8f9fa", fg="#333").pack(anchor="w", pady=2)

    def build_gestion_tab(self, parent):
        tk.Label(parent, text="Módulos de Gestión", font=("Segoe UI", 14, "bold"), bg="white", fg="#333").pack(pady=20)
        
        items = [
            ("CLIENTES", "Registre la información personal y documentos de identidad.\nEs necesario registrar un cliente antes de rentar."),
            ("VEHÍCULOS", "Administre la flota. Puede cambiar tarifas y ver el estado\n(Disponible/Ocupado) de cada auto.")
        ]
        
        for title, text in items:
            frame = tk.Frame(parent, bg="white", pady=10)
            frame.pack(fill="x", padx=40)
            tk.Label(frame, text=f"> {title}", font=("Segoe UI", 12, "bold"), bg="white", fg="#17a2b8").pack(anchor="w")
            tk.Label(frame, text=text, font=("Segoe UI", 10), bg="white", justify="left", fg="#555").pack(anchor="w")
            ttk.Separator(parent, orient='horizontal').pack(fill='x', padx=40)

    def build_rentas_tab(self, parent):
        tk.Label(parent, text="Flujo de Renta", font=("Segoe UI", 14, "bold"), bg="white", fg="#333").pack(pady=20)
        
        # Reemplazados los emojis de números por texto simple
        steps = [
            "1. Ir a Gestión > Rentas en el menú principal.",
            "2. Seleccionar un Cliente existente del menú desplegable.",
            "3. Seleccionar un Vehículo Disponible (los ocupados no aparecen).",
            "4. Ingresar la cantidad de días y presionar 'CONFIRMAR'.",
            "5. Para devolver: Seleccione la renta en la tabla inferior y click en 'FINALIZAR'."
        ]
        
        for step in steps:
            tk.Label(parent, text=step, font=("Segoe UI", 11), bg="white", fg="#333", pady=5).pack(anchor="w", padx=40)

    def build_admin_tab(self, parent):
        tk.Label(parent, text="Funciones de Administrador", font=("Segoe UI", 14, "bold"), bg="white", fg="#dc3545").pack(pady=20)
        
        warning = tk.Label(parent, text="ATENCIÓN: Zona Restringida (Solo Admin)", 
                           font=("Segoe UI", 10, "bold"), bg="#fff3cd", fg="#856404", padx=10, pady=5)
        warning.pack(pady=10)

        info = ("• Respaldos: Vaya a Archivo > Crear Respaldo para guardar una copia segura (.db).\n"
                "• Restauración: Permite recuperar datos desde un archivo previo.\n"
                "• Reportes Financieros: Acceso total a historiales de venta.")
        
        tk.Label(parent, text=info, font=("Segoe UI", 10), bg="white", justify="left", padx=40).pack(anchor="w", pady=10)

    def create_footer(self):
        footer = tk.Frame(self, bg="#F4F6F9")
        footer.pack(side="bottom", fill="x", pady=10)
        
        tk.Button(footer, text="Cerrar Ventana", command=self.destroy, 
                  bg="#6c757d", fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", cursor="hand2", padx=20, pady=5).pack()