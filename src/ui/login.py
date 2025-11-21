import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from src.logic.auth import AuthService

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Acceso - AutoPy")
    
        self.geometry("360x540") 
        self.resizable(False, False)
        self.logged_user = None
        
        self.color_bg = "#000000"       
        self.color_accent = "#D60000"   
        self.color_input_bg = "#1A1A1A" 
        self.color_input_fg = "#FFFFFF" 
        self.color_placeholder = "#666666"
        
        self.configure(bg=self.color_bg)
        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        self.init_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def init_ui(self):
        
        container = tk.Frame(self, bg=self.color_bg)
        container.pack(expand=True, fill="both", padx=40, pady=20)

        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            img_path = os.path.join(base_dir, "assets", "logo.jpg")
            
            pil_img = Image.open(img_path)
            
            pil_img = pil_img.resize((220, 220), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(pil_img)
            
            lbl_logo = tk.Label(container, image=self.logo_img, bg=self.color_bg, bd=0)
            lbl_logo.pack(pady=(40, 20))
        except:
            tk.Label(container, text="AUTOPY", font=("Segoe UI", 30, "bold"), 
                     bg=self.color_bg, fg=self.color_accent).pack(pady=(50, 30))

        tk.Label(container, text="USUARIO", font=("Segoe UI", 9, "bold"), 
                 bg=self.color_bg, fg=self.color_placeholder).pack(anchor="w", pady=(0, 5))
        
        self.entry_user = tk.Entry(container, font=("Segoe UI", 11), 
                                   bg=self.color_input_bg, fg=self.color_input_fg,
                                   insertbackground='white', relief="flat")
        self.entry_user.pack(fill="x", ipady=8, pady=(0, 15))
        self.entry_user.focus()

        tk.Label(container, text="CONTRASEÑA", font=("Segoe UI", 9, "bold"), 
                 bg=self.color_bg, fg=self.color_placeholder).pack(anchor="w", pady=(0, 5))
        
        self.entry_pass = tk.Entry(container, font=("Segoe UI", 11), 
                                   bg=self.color_input_bg, fg=self.color_input_fg,
                                   insertbackground='white', relief="flat", show="•")
        self.entry_pass.pack(fill="x", ipady=8, pady=(0, 30))

        self.btn_login = tk.Button(container, text="INICIAR SESIÓN", font=("Segoe UI", 10, "bold"),
                              bg=self.color_accent, fg="white", 
                              activebackground="#ff3333", activeforeground="white",
                              relief="flat", cursor="hand2", borderwidth=0,
                              command=self.perform_login)
        self.btn_login.pack(fill="x", ipady=10)

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
            messagebox.showerror("Error de Acceso", "Credenciales inválidas.")
            self.entry_pass.delete(0, tk.END)
            
    def on_close(self):
        self.destroy()