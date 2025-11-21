import shutil
import os
import datetime
from tkinter import filedialog, messagebox
from src.database.db import DB_PATH 

class BackupService:
    @staticmethod
    def create_backup():
        """
        Genera una copia del archivo .sqlite3 en la carpeta que elija el usuario.
        """
    
        if not os.path.exists(DB_PATH):
            messagebox.showerror("Error", "No se encuentra el archivo de base de datos.")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        default_name = f"respaldo_autopy_{timestamp}.db"

        target_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Archivos de Base de Datos", "*.db"), ("Todos", "*.*")],
            initialfile=default_name,
            title="Guardar Respaldo de Base de Datos"
        )

        if target_path:
            try:
               
                shutil.copy2(DB_PATH, target_path)
                messagebox.showinfo("Respaldo Exitoso", f"Copia de seguridad guardada en:\n{target_path}")
            except Exception as e:
                messagebox.showerror("Error de Respaldo", f"No se pudo copiar el archivo:\n{e}")

    @staticmethod
    def restore_backup():
        """
        Restaura una base de datos desde un archivo seleccionado.
        ADVERTENCIA: Esto sobrescribe la BD actual.
        """
        
        confirm = messagebox.askyesno(
            "¡ADVERTENCIA DE SEGURIDAD!",
            "Restaurar una base de datos BORRARÁ todos los datos actuales y los reemplazará por los del respaldo.\n\n"
            "¿Está completamente seguro de continuar?"
        )
        if not confirm: return

        source_path = filedialog.askopenfilename(
            title="Seleccionar archivo de respaldo para restaurar",
            filetypes=[("Archivos de Base de Datos", "*.db;*.sqlite3")]
        )

        if source_path:
            try:
               
                shutil.copy2(source_path, DB_PATH)
                messagebox.showinfo("Restauración Exitosa", "La base de datos ha sido restaurada.\nEl sistema se cerrará para aplicar cambios.")
                exit() 
            except Exception as e:
                messagebox.showerror("Error Crítico", f"Fallo al restaurar:\n{e}")  