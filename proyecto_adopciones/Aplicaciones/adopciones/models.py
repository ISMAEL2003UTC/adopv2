from django.db import models

# Create your models here.

class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='personas/', default='personas/default.png')


    class Meta:
        db_table = 'persona'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Mascota(models.Model):
    id_mascota = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    collar = models.CharField(max_length=50, unique=True, blank=True, null=True)
    especie = models.CharField(max_length=50, blank=True, null=True)
    raza = models.CharField(max_length=100, blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    sexo = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    foto=models.FileField(upload_to='mascota', null=True , blank=True)
    estado = models.CharField(max_length=50, default='Disponible')

    class Meta:
        db_table = 'mascota'  

    def _str_(self):
        return f"{self.nombre} ({self.especie})"

class Adopcion(models.Model):
    id_adopcion = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='id_persona')
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, db_column='id_mascota')
    fecha_adopcion = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    imagen = models.ImageField(
        upload_to='adopciones/',
        blank=True,
        null=True,
        default='adopciones/default.png'
    )
    class Meta:
        db_table = 'adopcion'
        unique_together = ('id_persona', 'id_mascota')  

    def __str__(self):
        return f"{self.id_persona} adoptó a {self.id_mascota}"
