import os
import sys
import django
import tkinter as tk
from tkinter import ttk, messagebox
from django.contrib.auth import authenticate

# Agregar el proyecto al path
sys.path.append("C:/Users/hp/Music/proyecto pueba/biblioteca_ok/biblioteca")

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca.settings')
django.setup()

from gestion_libros.models import Libro  # Importar el modelo Libro

def ventana_registrar_libro():
    def guardar_libro():
        codigo = entry_codigo.get()
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        genero = entry_genero.get()
        fecha_publicacion = entry_fecha_publicacion.get()

        if not (codigo and titulo and autor and genero and fecha_publicacion):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Crear y guardar un nuevo libro en la base de datos
            nuevo_libro = Libro(
                codigo=codigo,
                titulo=titulo,
                autor=autor,
                genero=genero,
                fecha_publicacion=fecha_publicacion
            )
            nuevo_libro.save()
            messagebox.showinfo("Éxito", "Libro registrado con éxito")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el libro: {e}")

    ventana = tk.Toplevel()
    ventana.title("Registrar Libro")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Código:").grid(row=0, column=0, padx=10, pady=5)
    entry_codigo = tk.Entry(ventana)
    entry_codigo.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Título:").grid(row=1, column=0, padx=10, pady=5)
    entry_titulo = tk.Entry(ventana)
    entry_titulo.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Autor:").grid(row=2, column=0, padx=10, pady=5)
    entry_autor = tk.Entry(ventana)
    entry_autor.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Género:").grid(row=3, column=0, padx=10, pady=5)
    entry_genero = tk.Entry(ventana)
    entry_genero.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Fecha Publicación (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
    entry_fecha_publicacion = tk.Entry(ventana)
    entry_fecha_publicacion.grid(row=4, column=1, padx=10, pady=5)

    tk.Button(ventana, text="Guardar", command=guardar_libro).grid(row=5, column=0, columnspan=2, pady=20)

def ventana_listar_libros():
    def eliminar_libros():
        seleccionados = tree.selection()
        if not seleccionados:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún libro")
            return

        try:
            for seleccionado in seleccionados:
                valores = tree.item(seleccionado, 'values')
                codigo = valores[0]
                Libro.objects.filter(codigo=codigo).delete()
                tree.delete(seleccionado)
            messagebox.showinfo("Éxito", "Libro(s) eliminado(s) con éxito")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el/los libro(s): {e}")

    def volver_atras():
        ventana.destroy()

    ventana = tk.Toplevel()
    ventana.title("Listar Libros")
    ventana.geometry("600x400")

    tree = ttk.Treeview(ventana, columns=("Código", "Título", "Autor", "Género", "Fecha Publicación"), show="headings")
    tree.heading("Código", text="Código")
    tree.heading("Título", text="Título")
    tree.heading("Autor", text="Autor")
    tree.heading("Género", text="Género")
    tree.heading("Fecha Publicación", text="Fecha Publicación")

    tree.column("Código", width=80)
    tree.column("Título", width=150)
    tree.column("Autor", width=100)
    tree.column("Género", width=80)
    tree.column("Fecha Publicación", width=120)
    tree.pack(fill=tk.BOTH, expand=True)

    #Consultar los libros en la base de datos
    libros = Libro.objects.all()
    for libro in libros:
        tree.insert("", tk.END, values=(libro.codigo, libro.titulo, libro.autor, libro.genero, libro.fecha_publicacion))

    tk.Button(ventana, text="Eliminar Seleccionados", command=eliminar_libros).pack(pady=10)
    tk.Button(ventana, text="Atrás", command=volver_atras).pack(pady=10)

def ventana_principal():
    def cerrar_sesion():
        root.destroy()
        login()

    root = tk.Tk()
    root.title("Biblioteca")
    root.geometry("400x300")

    tk.Button(root, text="Registrar Libro", command=ventana_registrar_libro, width=20).pack(pady=20)
    tk.Button(root, text="Listar Libros", command=ventana_listar_libros, width=20).pack(pady=20)
    tk.Button(root, text="Cerrar Sesión", command=cerrar_sesion, width=20).pack(pady=20)

    root.mainloop()

def login():
    def autenticar_usuario():
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        user = authenticate(username=username, password=password)
        if user is not None:
            messagebox.showinfo("Éxito", f"¡Bienvenido {user.username}!")
            ventana.destroy()
            ventana_principal()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    ventana = tk.Tk()
    ventana.title("Login")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Usuario:").pack(pady=5)
    entry_username = tk.Entry(ventana)
    entry_username.pack(pady=5)

    tk.Label(ventana, text="Contraseña:").pack(pady=5)
    entry_password = tk.Entry(ventana, show="*")
    entry_password.pack(pady=5)

    tk.Button(ventana, text="Iniciar Sesión", command=autenticar_usuario).pack(pady=20)

    ventana.mainloop()

if __name__ == "__main__":
    login()
