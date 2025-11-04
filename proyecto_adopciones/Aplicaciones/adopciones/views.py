from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from django.contrib import messages

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
def guardarPersona(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        imagen = request.FILES['imagen']

        Persona.objects.create(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
            direccion=direccion,
            imagen=imagen
        )
        return redirect('persona')
def editarPersona(request, id_persona):
    persona = Persona.objects.get(id_persona=id_persona)

    if request.method == 'POST':
        persona.nombre = request.POST['nombre']
        persona.apellido = request.POST['apellido']
        persona.telefono = request.POST.get('telefono')
        persona.email = request.POST.get('email')
        persona.direccion = request.POST.get('direccion')
        persona.imagen = request.FILES['imagen']
        if 'imagen' in request.FILES:
            persona.imagen = request.FILES['imagen']
        persona.save()
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

    persona = Persona.objects.get(id_persona=personas_id)
    mascota = Mascota.objects.get(id=mascotas_id)

    #  Verificar si la persona ya adoptó esa mascota
    if Adopcion.objects.filter(id_persona=persona, id_mascota=mascota).exists():
        messages.error(request, 'Esta persona ya adoptó esta mascota.')
        return redirect('/crear-adopciones')

    # Verificar si la mascota ya fue adoptada por alguien más
    if Adopcion.objects.filter(id_mascota=mascota).exists():
        messages.error(request, 'Esta mascota ya fue adoptada por otra persona.')
        return redirect('/crear-adopciones')

    #  Crear la adopción
    adopcion = Adopcion.objects.create(
        id_persona=persona,
        id_mascota=mascota,
        fecha_adopcion=fecha_adopcion,
        observaciones=observaciones
    )

    # Cambiar estado de la mascota
    mascota.estado = 'Adoptada'
    mascota.save()

    messages.success(request, 'Adopción registrada correctamente.')
    return redirect('/listar-adopciones')

def eliminar_adopciones(request,id):
    adopcion = Adopcion.objects.get(id=id)
    nombre = adopcion.id_mascota.nombre
    adopcion.delete()
    messages.success(request, f'Adopcion de mascota  {nombre} eliminado correctamente')
    return redirect('/listar-adopciones')
