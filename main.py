import tkinter as tk
from src.database.db import init_db
from src.ui.login import LoginWindow
from src.ui.main_window import MainWindow

def main():
    print("--- PASO 1: Iniciando Base de Datos... ---")
    try:
        init_db()
        print("✅ BD Iniciada correctamente.")
    except Exception as e:
        print(f"❌ ERROR CRÍTICO EN BD: {e}")
        return

    print("--- PASO 2: Creando Ventana Raíz... ---")
    root = tk.Tk()
    root.withdraw() 

    print("--- PASO 3: Abriendo Login... ---")
    login_app = LoginWindow(root)
    
    # Esto es para forzar que el Login se muestre al frente
    login_app.deiconify()
    login_app.lift()
    login_app.focus_force()
    
    print("--- ESPERANDO USUARIO EN LOGIN... ---")
    root.wait_window(login_app) 

    print("--- PASO 4: Login Cerrado. Verificando usuario... ---")
    if hasattr(login_app, 'logged_user') and login_app.logged_user:
        user = login_app.logged_user
        print(f"✅ Usuario logueado: {user['user_name']}")
        
        print("--- PASO 5: Abriendo Ventana Principal... ---")
        main_app = MainWindow(root, user)
        
        root.wait_window(main_app)
        print("--- Fin de ejecución ---")
    else:
        print("⚠️ El usuario cerró el login sin ingresar.")
        root.destroy()

if __name__ == "__main__":
    main()