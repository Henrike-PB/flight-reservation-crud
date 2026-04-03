from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, AirplaneViewSet, ClientViewSet, ReservationViewSet

'''
Neste arquivo, estamos definindo as URLs para as views dos modelos Flight, Airplane, Client e Reservation usando um router do Django REST Framework.
O DefaultRouter é uma classe que automaticamente gera as URLs para as operações CRUD (Create, Read, Update, Delete) para cada viewset registrado.
'''

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'airplanes', AirplaneViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]