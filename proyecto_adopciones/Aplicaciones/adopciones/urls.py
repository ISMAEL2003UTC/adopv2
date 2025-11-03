
from django.urls import path
from .import views

urlpatterns = [
    path('persona/', views.persona, name='persona'),
    path('mascota/', views.mascota, name='mascota'),
    path('adopcion/', views.adopcion, name='adopcion'),
    path('nuevaAdopcion/', views.nuevaAdopcion, name='nuevaAdopcion'),
    path('persona/editarPersona/<int:id_persona>/', views.editarPersona, name='editarPersona'),
    path('nuevaPersona/', views.nuevaPersona, name='nuevaPersona'),


]

