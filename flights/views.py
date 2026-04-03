from django.shortcuts import render
from rest_framework import viewsets
from .models import Flight, Airplane, Client, Reservation
from .serializers import FlightSerializer, AirplaneSerializer, ClientSerializer, ReservationSerializer

'''
Neste arquivo, estamos definindo as views para os modelos Flight, Airplane, Client e Reservation usando viewsets do Django REST Framework.
Cada viewset é uma classe que herda de viewsets.ModelViewSet e especifica o queryset e o serializer_class para cada modelo.
O queryset define os objetos que serão retornados pela viewset, enquanto o serializer_class define a classe de serializer que será usada para serializar os dados.
'''

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


