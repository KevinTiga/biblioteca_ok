from django.db import models

# Create your models here.
class Libro(models.Model):
    codigo = models.CharField(primary_key=True, max_length=50)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    fecha_publicacion = models.DateField()

    def __str__(self):
        return self.titulo

class Usuario(models.Model):
    cedula = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    codigof = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cedulaf = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigof.titulo} - {self.cedulaf.nombre}"
