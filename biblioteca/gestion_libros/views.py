from django.shortcuts import render, redirect

# Create your views here.

from .models import Libro, Usuario, Prestamo
from django.http import HttpResponse

def registrar_libro(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        titulo = request.POST['titulo']
        autor = request.POST['autor']
        genero = request.POST['genero']
        fecha_publicacion = request.POST['fecha_publicacion']
        libro = Libro(codigo=codigo, titulo=titulo, autor=autor, genero=genero, fecha_publicacion=fecha_publicacion)
        libro.save()
        return redirect('listar_libros')  # Redirige a la vista de listar libros
    return render(request, 'registrar_libro.html')

def listar_libros(request):
    libros = Libro.objects.all()
    return render(request, 'listar_libros.html', {'libros': libros})
