
from django.urls import path

from proyecto_adopciones import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('persona/', views.persona, name='persona'),
    path('mascota/', views.mascota, name='mascota'),
    path('persona/editarPersona/<int:id_persona>/', views.editarPersona, name='editarPersona'),
    path('nuevaPersona/', views.nuevaPersona, name='nuevaPersona'),
    path('guardarPersona/', views.guardarPersona, name='guardarPersona'),
    path('persona/eliminarPersona/<int:id_persona>/', views.eliminarPersona, name='eliminarPersona'),


    #adopciones
    path('listar-adopciones',views.listar_adopciones),
    path('crear-adopciones',views.crear_adopciones),
    path('guardar-adopciones',views.guardar_adopciones),
    path('eliminar-adopciones/<id>',views.eliminar_adopciones),
    #path('editar-adopciones/<id>',views.editar_adopciones),
    #path('procesar-info-adopciones',views.procesar_info_adopciones),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
