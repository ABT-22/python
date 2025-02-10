import sqlite3
import tkinter as tk
from tkinter import messagebox

# Crear base de datos y tabla
conn = sqlite3.connect("tareas.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    completada INTEGER DEFAULT 0
)
""")
conn.commit()
conn.close()

# Funciones
def agregar_tarea():
    descripcion = entrada_tarea.get()
    if descripcion:
        conn = sqlite3.connect("tareas.db")
        c = conn.cursor()
        c.execute("INSERT INTO tareas (descripcion) VALUES (?)", (descripcion,))
        conn.commit()
        conn.close()
        entrada_tarea.delete(0, tk.END)
        actualizar_lista()
    else:
        messagebox.showwarning("Advertencia", "La tarea no puede estar vacía.")

def eliminar_tarea():
    try:
        seleccion = lista_tareas.curselection()[0]
        tarea_id = lista_tareas.get(seleccion).split(" - ")[0]
        conn = sqlite3.connect("tareas.db")
        c = conn.cursor()
        c.execute("DELETE FROM tareas WHERE id=?", (tarea_id,))
        conn.commit()
        conn.close()
        actualizar_lista()
    except IndexError:
        messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar.")

def marcar_completada():
    try:
        seleccion = lista_tareas.curselection()[0]
        tarea_id = lista_tareas.get(seleccion).split(" - ")[0]
        conn = sqlite3.connect("tareas.db")
        c = conn.cursor()
        c.execute("UPDATE tareas SET completada=1 WHERE id=?", (tarea_id,))
        conn.commit()
        conn.close()
        actualizar_lista()
    except IndexError:
        messagebox.showwarning("Advertencia", "Selecciona una tarea para completar.")

def actualizar_lista():
    lista_tareas.delete(0, tk.END)
    conn = sqlite3.connect("tareas.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tareas")
    for fila in c.fetchall():
        estado = "✔" if fila[2] else "✘"
        lista_tareas.insert(tk.END, f"{fila[0]} - {fila[1]} ({estado})")
    conn.close()

# Interfaz gráfica
root = tk.Tk()
root.title("Gestor de Tareas")

entrada_tarea = tk.Entry(root, width=40)
entrada_tarea.pack(pady=5)

btn_agregar = tk.Button(root, text="Agregar Tarea", command=agregar_tarea)
btn_agregar.pack()

lista_tareas = tk.Listbox(root, width=50, height=10)
lista_tareas.pack(pady=5)

btn_completar = tk.Button(root, text="Marcar como Completada", command=marcar_completada)
btn_completar.pack()

btn_eliminar = tk.Button(root, text="Eliminar Tarea", command=eliminar_tarea)
btn_eliminar.pack()

actualizar_lista()

root.mainloop()