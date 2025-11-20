import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from src.logic.auth import AuthService

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Acceso - AutoPy")
        self.geometry("400x600")
        self.resizable(False, False)
        self.logged_user = None
        
        # --- PALETA DE COLORES (Basada en tu Logo) ---
        self.color_bg = "#000000"       # Negro puro (Fondo del logo)
        self.color_primary = "#D60000"  # Rojo deportivo (Texto AUTOPY)
        self.color_text = "#FFFFFF"     # Blanco (Texto secundario)
        self.color_input_bg = "#333333" # Gris oscuro para cajas de texto
        self.color_input_fg = "#FFFFFF" # Texto blanco al escribir
        
        self.font_title = ("Segoe UI", 18, "bold")
        self.font_text = ("Segoe UI", 10)
        
        self.configure(bg=self.color_bg)
        
        # Centrar ventana
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        self.init_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def init_ui(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=self.color_bg)
        main_frame.pack(expand=True, fill="both", padx=40, pady=20)

        # --- 1. LOGO INTEGRADO ---
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            # Buscamos logo.jpg específicamente
            img_path = os.path.join(base_dir, "assets", "logo.jpg")
            
            # Cargar y ajustar tamaño (más grande para que luzca)
            pil_img = Image.open(img_path)
            # Mantenemos proporción
            pil_img = pil_img.resize((250, 250), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(pil_img)
            
            # Label sin bordes para que se funda con el fondo negro
            lbl_logo = tk.Label(main_frame, image=self.logo_img, bg=self.color_bg, borderwidth=0)
            lbl_logo.pack(pady=(0, 0)) 
        except Exception as e:
            # Fallback si no encuentra la imagen
            print(f"Error cargando imagen: {e}")
            tk.Label(main_frame, text="AUTOPY", font=("Arial", 30, "bold"), 
                     bg=self.color_bg, fg=self.color_primary).pack(pady=40)

        # --- 2. FORMULARIO ---
        # Usuario
        tk.Label(main_frame, text="USUARIO", font=("Segoe UI", 8, "bold"), 
                 bg=self.color_bg, fg=self.color_primary).pack(anchor="w", pady=(0, 5))
        
        self.entry_user = tk.Entry(main_frame, font=self.font_text, 
                                   bg=self.color_input_bg, fg=self.color_input_fg,
                                   insertbackground='white', # Cursor blanco
                                   relief="flat")
        self.entry_user.pack(fill="x", ipady=8, pady=(0, 20))
        self.entry_user.focus()

        # Contraseña
        tk.Label(main_frame, text="CONTRASEÑA", font=("Segoe UI", 8, "bold"), 
                 bg=self.color_bg, fg=self.color_primary).pack(anchor="w", pady=(0, 5))
        
        self.entry_pass = tk.Entry(main_frame, font=self.font_text, 
                                   bg=self.color_input_bg, fg=self.color_input_fg,
                                   insertbackground='white', # Cursor blanco
                                   relief="flat", show="•")
        self.entry_pass.pack(fill="x", ipady=8, pady=(0, 30))

        # --- 3. BOTÓN DE ACCIÓN ---
        # Botón rojo intenso con texto blanco
        self.btn_login = tk.Button(main_frame, text="INGRESAR AL SISTEMA", font=("Segoe UI", 10, "bold"),
                              bg=self.color_primary, fg="white", 
                              activebackground="#ff3333", activeforeground="white", # Efecto al hacer click
                              relief="flat", cursor="hand2",
                              command=self.perform_login)
        self.btn_login.pack(fill="x", ipady=10)

        # Footer discreto
        tk.Label(main_frame, text="© 2025 AutoPy Rental Services", font=("Segoe UI", 7), 
                 bg=self.color_bg, fg="#555555").pack(side="bottom", pady=10)
        
        self.bind('<Return>', lambda event: self.perform_login())

    def perform_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        if not user or not pwd:
            messagebox.showwarning("Datos incompletos", "Por favor ingrese sus credenciales.")
            return

        logged_user = AuthService.login(user, pwd)
        
        if logged_user:
            self.logged_user = logged_user
            self.destroy()
        else:
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")
            
    def on_close(self):
        self.destroy()