from django.urls import path

from arrays import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:d>', views.data, name='data'),
]