from django.urls import path, include
from . import views

app_name = "Teacher"
urlpatterns = [
    path('read/', views.read, name='read'),
    path('create/', views.create, name='create'),
    path('update/<slug:id>/', views.update, name='update'),
    path('delete/<slug:id>/', views.delete, name='delete'),
    path('check/', views.permission, name='permission'),
    path('<slug:id>/', views.readDetail, name='read-detail'),
]
