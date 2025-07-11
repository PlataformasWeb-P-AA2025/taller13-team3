from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group

# ejemplo de uso django-rest_framework
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from departamentos.serializers import UserSerializer, GroupSerializer, \
    EdificioSerializer, DepartamentoSerializer

from departamentos.models import *
from departamentos.forms import *

def index(request):
    edificios = Edificio.objects.all()
    informacion_template = {'edificios': edificios, 'numero_edificios': len(edificios)}
    return render(request, 'index.html', informacion_template)


def ingreso(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.data.get("username")
            raw_password = form.data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect(index)
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Has salido del sistema")
    return redirect(index)


def obtener_edificio(request, id):
    edificio = Edificio.objects.get(pk=id)
    return render(request, 'obtener_edificio.html', {'edificio': edificio})

@login_required(login_url='/entrando/login/')
@permission_required('departamentos.add_edificio', login_url="/entrando/login/")
def crear_edificio(request):
    if request.method == 'POST':
        formulario = EdificioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = EdificioForm()
    return render(request, 'crearEdificio.html', {'formulario': formulario})

@login_required(login_url='/entrando/login/')
def editar_edificio(request, id):
    edificio = Edificio.objects.get(pk=id)
    if request.method == 'POST':
        formulario = EdificioForm(request.POST, instance=edificio)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = EdificioForm(instance=edificio)
    return render(request, 'editarEdificio.html', {'formulario': formulario})

def eliminar_edificio(request, id):
    edificio = Edificio.objects.get(pk=id)
    edificio.delete()
    return redirect(index)


def crear_departamento(request):
    if request.method == 'POST':
        formulario = DepartamentoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = DepartamentoForm()
    return render(request, 'crearDepartamento.html', {'formulario': formulario})

def editar_departamento(request, id):
    departamento = Departamento.objects.get(pk=id)
    if request.method == 'POST':
        formulario = DepartamentoForm(request.POST, instance=departamento)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = DepartamentoForm(instance=departamento)
    return render(request, 'crearDepartamento.html', {'formulario': formulario})

def crear_departamento_edificio(request, id):
    edificio = Edificio.objects.get(pk=id)
    if request.method == 'POST':
        formulario = DepartamentoEdificioForm(edificio, request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = DepartamentoEdificioForm(edificio)
    return render(request, 'crearDepartamentoEdificio.html', {'formulario': formulario, 'edificio': edificio})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class EdificioViewSet(viewsets.ModelViewSet):
    queryset = Edificio.objects.all()
    serializer_class = EdificioSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
