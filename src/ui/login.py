import tkinter as tk
from tkinter import messagebox
from src.logic.auth import AuthService

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login - AutoPy")
        self.geometry("350x350")
        self.resizable(False, False)
        self.logged_user = None
        
        # --- CORRECCIÓN: Quitamos transient para que no se oculte con la raiz ---
        # self.transient(parent)  <-- ELIMINADO
        # self.grab_set()         <-- ELIMINADO
        
        # Centrar ventana
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        self.init_ui()
        
        # Protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def init_ui(self):
        lbl_title = tk.Label(self, text="Iniciar Sesión", font=("Arial", 16, "bold"))
        lbl_title.pack(pady=20)
        
        tk.Label(self, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(self)
        self.entry_user.pack(pady=5)
        self.entry_user.focus() 
        
        tk.Label(self, text="Contraseña:").pack(pady=5)
        self.entry_pass = tk.Entry(self, show="*") 
        self.entry_pass.pack(pady=5)
        
        btn_login = tk.Button(self, text="Ingresar", command=self.perform_login, 
                              bg="#007bff", fg="white", width=20)
        btn_login.pack(pady=20)

    def perform_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        # Validación simple de campos vacíos
        if not user or not pwd:
            messagebox.showwarning("Atención", "Ingrese usuario y contraseña")
            return

        # Verificamos en BD
        logged_user = AuthService.login(user, pwd)
        
        if logged_user:
            self.logged_user = logged_user
            self.destroy() # Cerramos Login para dar paso al Main
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            
    def on_close(self):
        # Si cierran la ventana sin loguearse
        self.destroy()