import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from src.logic.auth import AuthService

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Acceso - AutoPy")
        self.geometry("450x650") # Un poco más alta y ancha para elegancia
        self.resizable(False, False)
        self.logged_user = None
        
        # --- PALETA DE COLORES (BRANDING DARK) ---
        self.color_bg = "#000000"       # Negro puro (Funde el logo)
        self.color_accent = "#D60000"   # Rojo del logo (Branding)
        self.color_input_bg = "#1A1A1A" # Gris oscuro elegante
        self.color_input_fg = "#FFFFFF" # Texto blanco
        self.color_placeholder = "#666666"
        
        self.configure(bg=self.color_bg)
        
        # Centrar en pantalla
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        self.init_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def init_ui(self):
        # Frame central con padding para que respire el diseño
        container = tk.Frame(self, bg=self.color_bg)
        container.pack(expand=True, fill="both", padx=50, pady=40)

        # --- 1. LOGO (Branding) ---
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            img_path = os.path.join(base_dir, "assets", "logo.jpg")
            
            pil_img = Image.open(img_path)
            # Redimensionamos un poco más grande para impacto visual
            pil_img = pil_img.resize((280, 280), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(pil_img)
            
            lbl_logo = tk.Label(container, image=self.logo_img, bg=self.color_bg, bd=0)
            lbl_logo.pack(pady=(0, 20))
        except:
            # Fallback texto estilizado
            tk.Label(container, text="AUTOPY", font=("Segoe UI", 30, "bold"), 
                     bg=self.color_bg, fg=self.color_accent).pack(pady=40)

        # --- 2. CAMPOS DE TEXTO ---
        # Usuario
        lbl_user = tk.Label(container, text="USUARIO", font=("Segoe UI", 9, "bold"), 
                            bg=self.color_bg, fg=self.color_placeholder)
        lbl_user.pack(anchor="w", pady=(0, 5))
        
        self.entry_user = tk.Entry(container, font=("Segoe UI", 11), 
                                   bg=self.color_input_bg, fg=self.color_input_fg,
                                   insertbackground='white', relief="flat")
        self.entry_user.pack(fill="x", ipady=10, pady=(0, 20))
        self.entry_user.focus()

        # Contraseña
        lbl_pass = tk.Label(container, text="CONTRASEÑA", font=("Segoe UI", 9, "bold"), 
                            bg=self.color_bg, fg=self.color_placeholder)
        lbl_pass.pack(anchor="w", pady=(0, 5))
        
        self.entry_pass = tk.Entry(container, font=("Segoe UI", 11), 
                                   bg=self.color_input_bg, fg=self.color_input_fg,
                                   insertbackground='white', relief="flat", show="•")
        self.entry_pass.pack(fill="x", ipady=10, pady=(0, 30))

        # --- 3. BOTÓN DE ACCIÓN (Call to Action) ---
        self.btn_login = tk.Button(container, text="INICIAR SESIÓN", font=("Segoe UI", 11, "bold"),
                              bg=self.color_accent, fg="white", 
                              activebackground="#ff3333", activeforeground="white",
                              relief="flat", cursor="hand2", borderwidth=0,
                              command=self.perform_login)
        self.btn_login.pack(fill="x", ipady=12) # Botón alto y moderno

        # --- 4. FOOTER ---
        tk.Label(container, text="Sistema de Gestión v1.0", font=("Segoe UI", 8), 
                 bg=self.color_bg, fg="#444444").pack(side="bottom", pady=10)
        
        # Permitir entrar con tecla ENTER
        self.bind('<Return>', lambda event: self.perform_login())

    def perform_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        if not user or not pwd:
            messagebox.showwarning("Datos incompletos", "Por favor ingrese usuario y contraseña.")
            return

        logged_user = AuthService.login(user, pwd)
        
        if logged_user:
            self.logged_user = logged_user
            self.destroy()
        else:
            # Mensaje de error más amigable
            messagebox.showerror("Error de Acceso", "Credenciales inválidas.\nVerifique su usuario y contraseña.")
            self.entry_pass.delete(0, tk.END) # Limpiar contraseña para reintentar
            
    def on_close(self):
        self.destroy()