
from datetime import datetime
from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Count



from .models import Persona, Mascota, Adopcion

# Create your views here.
# renderizando de todos los listados ######################################################################
def persona(request):
    listadoPersona = Persona.objects.all()
    return render(request, 'persona.html', {'personas': listadoPersona})
def mascota(request):
    listadoMascota = Mascota.objects.all()
    return render(request, 'mascota.html', {'mascotas': listadoMascota})
def adopcion(request):
    listadoAdopcion = Adopcion.objects.all()
    return render(request, 'adopcion.html', {'adopciones': listadoAdopcion})

#formularios para agregar nuevos datos ################################################################
def nuevaAdopcion(request):
    return render(request, 'nuevaAdopcion.html')
def nuevaPersona(request):
    return render(request, 'nuevaPersona.html') 
def nuevaMascota(request):
    return render(request, 'nuevaMascota.html')

# apartado para guardar en la bdd ##################################################################
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Persona

def guardarPersona(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        imagen = request.FILES.get('imagen')  # Evita MultiValueDictKeyError

        if not nombre or not apellido or not email or not direccion or not imagen:
            messages.error(request, "Por favor, complete todos los campos obligatorios y seleccione una imagen.")
            return redirect('nuevaPersona')

        Persona.objects.create(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
            direccion=direccion,
            imagen=imagen
        )

        messages.success(request, "Persona registrada correctamente.")
        return redirect('persona')
    else:
        return redirect('nuevaPersona')

from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Persona

def editarPersona(request, id_persona):
    persona = Persona.objects.get(id_persona=id_persona)

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        imagen = request.FILES.get('imagen')  # Opcional

        if not nombre or not apellido or not email or not direccion:
            messages.error(request, "Por favor, complete todos los campos obligatorios.")
            return redirect(reverse('editarPersona', kwargs={'id_persona': id_persona}))
        persona.nombre = nombre
        persona.apellido = apellido
        persona.telefono = telefono
        persona.email = email
        persona.direccion = direccion
        if imagen:
            persona.imagen = imagen  
        persona.save()
        messages.success(request, "Persona actualizada correctamente.")
        return redirect('persona')
    return render(request, 'editarPersona.html', {'persona': persona})


#funciones para eliminar registros #########################################################################3
    
def eliminarPersona(request, id_persona):
    personaEliminar = Persona.objects.get(id_persona=id_persona)
    personaEliminar.delete()
    return redirect('persona')

def listar_adopciones(request):
    adopciones = Adopcion.objects.all()
    return render(request,'adopciones/indexAdopciones.html',{'adopciones':adopciones})


def crear_adopciones(request):
    mascotas = Mascota.objects.all()
    personas = Persona.objects.all()
    return render(request,'adopciones/createAdopciones.html',{'mascotas':mascotas,'personas':personas})

"""def guardar_adopciones(request):
    personas_id = request.POST.get('personas')
    mascotas_id = request.POST.get('mascotas')
    fecha_adopcion = request.POST.get('fecha_adopcion')
    observaciones = request.POST.get('observaciones')
    

    persona = Persona.objects.get(id_persona=personas_id)
    mascota = Mascota.objects.get(id=mascotas_id)
    adopcion = Adopcion.objects.create(
        id_persona=persona,
        id_mascota=mascota,
        fecha_adopcion=fecha_adopcion,
        observaciones=observaciones
    )
    

    messages.success(request, 'Adopción creada correctamente')
    return redirect('/listar-adopciones')
"""
def guardar_adopciones(request):
    personas_id = request.POST.get('personas')
    mascotas_id = request.POST.get('mascotas')
    fecha_adopcion = request.POST.get('fecha_adopcion')
    observaciones = request.POST.get('observaciones')

   
    imagen = request.FILES.get('imagen')

    persona = Persona.objects.get(id_persona=personas_id)
    mascota = Mascota.objects.get(id_mascota=mascotas_id)

    
    if Adopcion.objects.filter(id_persona=persona, id_mascota=mascota).exists():
        messages.error(request, 'Esta persona ya adoptó esta mascota.')
        return redirect('/crear-adopciones')

    
    if Adopcion.objects.filter(id_mascota=mascota).exists():
        messages.error(request, 'Esta mascota ya fue adoptada por otra persona.')
        return redirect('/crear-adopciones')

    
    Adopcion.objects.create(
        id_persona=persona,
        id_mascota=mascota,
        fecha_adopcion=fecha_adopcion,
        observaciones=observaciones,
        imagen=imagen  
    )

    
    mascota.estado = 'Adoptada'
    mascota.save()

    messages.success(request, 'Adopción registrada correctamente.')
    return redirect('/listar-adopciones')

def eliminar_adopciones(request, id):
    adopcion = Adopcion.objects.get(id_adopcion=id)
    nombre = adopcion.id_mascota.nombre
    adopcion.delete()
    messages.success(request, f'Adopción de mascota {nombre} eliminada correctamente')
    return redirect('/listar-adopciones')



def editar_adopciones(request, id):
    adopciones = Adopcion.objects.get(id_adopcion=id)
    mascotas = Mascota.objects.all()
    personas = Persona.objects.all()
    return render(request, 'adopciones/editAdopciones.html', {
        'adopciones': adopciones,
        'mascotas': mascotas,
        'personas': personas
    })

def procesar_info_adopciones(request):
    if request.method == "POST":

        id_adopcion = request.POST.get("id")
        adopcion = get_object_or_404(Adopcion, id_adopcion=id_adopcion)

        persona = adopcion.id_persona
        mascota = adopcion.id_mascota

        persona.nombre = request.POST.get("nombre")
        persona.apellido = request.POST.get("apellido")
        persona.save()

        mascota.nombre = request.POST.get("mascotas")
        if request.FILES.get("foto_mascota"):
            mascota.foto = request.FILES["foto_mascota"]
        mascota.save()

        adopcion.fecha_adopcion = request.POST.get("fecha_adopcion")
        adopcion.observaciones = request.POST.get("observaciones")
        if request.FILES.get("imagen"):
            adopcion.imagen = request.FILES["imagen"]
        adopcion.save()

        messages.success(request, "Adopción actualizada correctamente.")
        return redirect('/listar-adopciones')



def reporte_estadistico_adopciones(request):

    especies = (
        Mascota.objects
        .values("especie")
        .annotate(total=Count("adopcion"))
        .order_by("-total")
    )

    razas = (
        Mascota.objects
        .values("raza")
        .annotate(total=Count("adopcion"))
        .order_by("-total")
    )

    edades = (
        Mascota.objects
        .values("edad")
        .annotate(total=Count("adopcion"))
        .order_by("-total")
    )

    fecha_generacion = datetime.now().strftime('%d/%m/%Y %H:%M')

    return render(request, "adopciones/reporteAdopciones.html", {
        "especies": especies,
        "razas": razas,
        "edades": edades,
        "fecha_generacion": fecha_generacion
    })

def guardarMascota(request):
    nombre = request.POST["nombre"]
    descripcion = request.POST["descripcion"]
    especie = request.POST["especie"]
    collar = request.POST["collar"]
    raza = request.POST["raza"]
    edad = request.POST["edad"]
    sexo = request.POST["sexo"]
    color = request.POST["color"]
    estado = request.POST["estado"]
    foto = request.FILES.get("foto")
    if Mascota.objects.filter(collar=collar).exists():
        messages.error(request, f"El collar '{collar}' ya está registrado en otra mascota.")
        return redirect('nuevaMascota')

    Mascota.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        especie=especie,
        collar=collar,
        raza=raza,
        edad=edad,
        sexo=sexo,
        color=color,
        estado=estado,
        foto=foto
    )

    messages.success(request, "Mascota registrada exitosamente.")
    return redirect("/mascota")


def editarMascota(request, id_mascota):
    mascotaEditar = Mascota.objects.get(id_mascota=id_mascota)
    return render(request, "editarMascota.html", {'mascotaEditar': mascotaEditar})


def actualizarMascota(request, id_mascota):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        descripcion = request.POST["descripcion"]
        especie = request.POST["especie"]
        collar = request.POST["collar"]
        raza = request.POST["raza"]
        edad = request.POST["edad"]
        sexo = request.POST["sexo"]
        color = request.POST["color"]
        estado = request.POST["estado"]

        mascota = Mascota.objects.get(id_mascota=id_mascota)
        if Mascota.objects.filter(collar=collar).exclude(id_mascota=id_mascota).exists():
            messages.error(request, f"El collar '{collar}' ya está registrado en otra mascota.")
            return redirect(f"/editarMascota/{id_mascota}")
        mascota.nombre = nombre
        mascota.descripcion = descripcion
        mascota.especie = especie
        mascota.collar = collar
        mascota.raza = raza
        mascota.edad = edad
        mascota.sexo = sexo
        mascota.color = color
        mascota.estado = estado

        if request.FILES.get("foto"):
            mascota.foto = request.FILES["foto"]

        mascota.save()
        messages.success(request, "Mascota actualizada exitosamente.")
        return redirect("/mascota")


def eliminarMascota(request, id_mascota):
    mascotaEliminar = Mascota.objects.get(id_mascota=id_mascota)
    mascotaEliminar.delete()
    messages.success(request, "Mascota eliminada exitosamente.")
    return redirect('/mascota')

### REPORTES #######################################################################
def reporte_adopciones_persona(request):
    adopciones_por_persona = Adopcion.objects.values(
        'id_persona__id_persona',
        'id_persona__nombre',
        'id_persona__apellido'
    ).annotate(total_adopciones=Count('id_adopcion')).order_by('-total_adopciones')

    context = {
        'adopciones_por_persona': adopciones_por_persona
    }
    return render(request, 'adopciones/reporte_adopciones_persona.html', context)
