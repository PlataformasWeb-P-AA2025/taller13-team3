"""
    Manejo de urls para la aplicación
    departamentos
"""
from django.urls import path, include
from departamentos import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'edificios', views.EdificioViewSet)
router.register(r'departamentos', views.DepartamentoViewSet)

urlpatterns = [
    path('', views.index, name='index'),

    # Edificios
    path('edificio/<int:id>', views.obtener_edificio, name='obtener_edificio'),
    path('crear/edificio', views.crear_edificio, name='crear_edificio'),
    path('editar/edificio/<int:id>', views.editar_edificio, name='editar_edificio'),
    path('eliminar/edificio/<int:id>', views.eliminar_edificio, name='eliminar_edificio'),

    # Departamentos
    path('crear/departamento', views.crear_departamento, name='crear_departamento'),
    path('editar/departamento/<int:id>', views.editar_departamento, name='editar_departamento'),
    path('crear/departamento/edificio/<int:id>',
         views.crear_departamento_edificio,
         name='crear_departamento_edificio'),

    # Autenticación
    path('saliendo/logout/', views.logout_view, name="logout_view"),
    path('entrando/login/', views.ingreso, name="login"),

    # API REST
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
