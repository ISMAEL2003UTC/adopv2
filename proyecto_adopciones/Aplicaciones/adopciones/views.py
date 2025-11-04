
from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from django.contrib import messages

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


def editar_adopciones(request,id):
    adopciones= Adopcion.objects.get(id=id)
    mascotas=Mascota.objects.all()
    personas=Persona.objects.all()
    return render(request,'adopciones/editAdopciones.html',{'adopciones':adopciones,'mascotas':mascotas,'personas':personas})

def procesar_info_adopciones(request):
    if request.method == 'POST':
        id_adopcion = request.POST.get('id')
        personas_id = request.POST.get('personas')
        mascotas_id = request.POST.get('mascotas')
        fecha_adopcion = request.POST.get('fecha_adopcion')
        observaciones = request.POST.get('observaciones')

        adopcion = Adopcion.objects.get(id=id_adopcion)
        persona = Persona.objects.get(id_persona=personas_id)
        mascota = Mascota.objects.get(id=mascotas_id)

        # Verificar si esa persona ya adoptó esa misma mascota (excepto esta adopción)
        if Adopcion.objects.filter(id_persona=persona, id_mascota=mascota).exclude(id=adopcion.id).exists():
            messages.error(request, 'Esta persona ya adoptó esta mascota.')
            return redirect(f'/editar-adopciones/{adopcion.id}')

        # Verificar si la mascota ya fue adoptada por otra persona (excepto esta adopción)
        if Adopcion.objects.filter(id_mascota=mascota).exclude(id=adopcion.id).exists():
            messages.error(request, 'Esta mascota ya fue adoptada por otra persona.')
            return redirect(f'/editar-adopciones/{adopcion.id}')

        # Actualizar datos si pasa las validaciones
        adopcion.id_persona = persona
        adopcion.id_mascota = mascota
        adopcion.fecha_adopcion = fecha_adopcion
        adopcion.observaciones = observaciones
        adopcion.save()

        # Cambiar estado de la mascota si es necesario
        mascota.estado = 'Adoptada'
        mascota.save()

        messages.success(request, 'Adopción actualizada correctamente.')
        return redirect('/listar-adopciones')

