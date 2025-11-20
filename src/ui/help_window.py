import tkinter as tk
from tkinter import ttk

class HelpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manual de Usuario / Ayuda")
        self.geometry("600x500")
        self.resizable(False, False)
        
        self.create_content()
        
        # Botón cerrar
        tk.Button(self, text="Cerrar", command=self.destroy, bg="#6c757d", fg="white").pack(pady=10)

    def create_content(self):
        # Usamos un Notebook (Pestañas) para organizar la ayuda
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Pestaña 1: Inicio
        f1 = tk.Frame(notebook, bg="white")
        notebook.add(f1, text="Inicio")
        lbl = tk.Label(f1, text="Bienvenido al Sistema AutoPy", font=("Arial", 14, "bold"), bg="white")
        lbl.pack(pady=10)
        txt = ("Este sistema permite gestionar una agencia de renta de autos.\n"
               "Use el menú superior para navegar entre las opciones.")
        tk.Label(f1, text=txt, bg="white", justify="left").pack(pady=10)

        # Pestaña 2: Gestión (CRUDs)
        f2 = tk.Frame(notebook, bg="white")
        notebook.add(f2, text="Gestión")
        info_gestion = (
            "• CLIENTES: Registre, edite o elimine clientes.\n"
            "• VEHÍCULOS: Administre la flota. Puede cambiar el estado y tarifa.\n"
            "• RENTAS: Módulo principal para registrar alquileres."
        )
        tk.Label(f2, text=info_gestion, bg="white", justify="left", padx=20, pady=20).pack(anchor="w")

        # Pestaña 3: Rentas
        f3 = tk.Frame(notebook, bg="white")
        notebook.add(f3, text="Cómo Rentar")
        info_rentas = (
            "PASO 1: Vaya a Gestión > Rentas.\n"
            "PASO 2: Seleccione un Cliente de la lista.\n"
            "PASO 3: Seleccione un Vehículo (solo aparecen los disponibles).\n"
            "PASO 4: Ingrese los días y presione 'Registrar Renta'.\n\n"
            "Para devolver un auto, seleccione la renta en la tabla y presione 'FINALIZAR'."
        )
        tk.Label(f3, text=info_rentas, bg="white", justify="left", padx=20, pady=20).pack(anchor="w")

        # Pestaña 4: Respaldos
        f4 = tk.Frame(notebook, bg="white")
        notebook.add(f4, text="Respaldos")
        info_backup = (
            "Solo el Administrador puede realizar respaldos.\n"
            "Vaya a Archivo > Respaldo BD.\n"
            "El sistema generará una copia segura de toda la información."
        )
        tk.Label(f4, text=info_backup, bg="white", justify="left", padx=20, pady=20).pack(anchor="w")