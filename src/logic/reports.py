import pandas as pd
import sqlite3
from tkinter import filedialog, messagebox
from src.database.db import get_connection
import os

class ReportService:
    
    @staticmethod
    def export_simple_vehicles():
        """
        REPORTE SENCILLO: Lista todos los vehículos y su estado.
        """
        conn = get_connection()
        try:
            # 1. Consulta SQL
            query = """
                SELECT id, model, plate_number, chassis_number, daily_rate, 
                CASE WHEN is_available = 1 THEN 'Disponible' ELSE 'Rentado' END as Estado
                FROM vehicles
            """
            # 2. Pandas lee el SQL y lo convierte en DataFrame
            df = pd.read_sql_query(query, conn)
            
            if df.empty:
                messagebox.showwarning("Atención", "No hay vehículos para reportar.")
                return

            # 3. Guardar archivo
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Guardar Reporte de Vehículos",
                initialfile="Reporte_Vehiculos_Sencillo.xlsx"
            )
            
            if file_path:
                df.to_excel(file_path, index=False, sheet_name="Vehículos")
                messagebox.showinfo("Éxito", f"Reporte generado en:\n{file_path}")
                os.startfile(file_path) # Abre el Excel automáticamente
                
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al generar reporte: {e}")
        finally:
            conn.close()

    @staticmethod
    def export_master_detail():
        """
        REPORTE MAESTRO-DETALLE:
        Hoja 1: Resumen de Clientes (Maestro)
        Hoja 2: Detalle de todas las Rentas (Detalle)
        """
        conn = get_connection()
        try:
            # Consulta Maestro (Clientes con conteo de rentas)
            query_master = """
                SELECT c.id, c.full_name, c.document_number, count(r.id) as total_rentas
                FROM customers c
                LEFT JOIN rentals r ON c.id = r.customer_id
                GROUP BY c.id
            """
            
            # Consulta Detalle (Rentas completa)
            query_detail = """
                SELECT r.id as Renta_ID, r.rental_date, r.return_date, 
                       c.full_name as Cliente, v.model as Vehiculo, r.total_amount
                FROM rentals r
                JOIN customers c ON r.customer_id = c.id
                JOIN vehicles v ON r.vehicle_id = v.id
            """
            
            df_master = pd.read_sql_query(query_master, conn)
            df_detail = pd.read_sql_query(query_detail, conn)
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                title="Guardar Reporte Maestro-Detalle",
                initialfile="Reporte_Maestro_Detalle.xlsx"
            )
            
            if file_path:
                # Se utilizo ExcelWriter para crear múltiples hojas
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df_master.to_excel(writer, sheet_name="Maestro Clientes", index=False)
                    df_detail.to_excel(writer, sheet_name="Detalle Rentas", index=False)
                
                messagebox.showinfo("Éxito", "Reporte Maestro-Detalle generado.")
                os.startfile(file_path)

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    @staticmethod
    def export_parameterized(start_date, end_date):
        """
        REPORTE PARAMETRIZADO: Rentas dentro de un rango de fechas.
        """
        conn = get_connection()
        try:
            query = """
                SELECT r.id, r.rental_date, c.full_name, v.model, r.total_amount
                FROM rentals r
                JOIN customers c ON r.customer_id = c.id
                JOIN vehicles v ON r.vehicle_id = v.id
                WHERE r.rental_date BETWEEN ? AND ?
            """
            # Pandas params funciona contra las inyeccion SQL
            df = pd.read_sql_query(query, conn, params=(start_date, end_date))
            
            if df.empty:
                messagebox.showinfo("Info", "No se encontraron rentas en esas fechas.")
                return

            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                title=f"Reporte Rentas {start_date} a {end_date}",
                initialfile=f"Rentas_{start_date}_{end_date}.xlsx"
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Éxito", "Reporte por parámetros generado.")
                os.startfile(file_path)
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()