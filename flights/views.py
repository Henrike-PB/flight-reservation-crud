from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from .models import Flight, Airplane, Client, Reservation
from .serializers import FlightSerializer, AirplaneSerializer, ClientSerializer, ReservationSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    '''
    CRUD de Aviões
    - GET (listar/detalhar): qualquer pessoa, mesmo sem login
    - POST/PUT/PATCH/DELETE: apenas administradores
    '''

    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]


class FlightViewSet(viewsets.ModelViewSet):
    '''
    CRUD de Voos
    - GET (listar/detalhar): qualquer pessoa, mesmo sem login
    - POST/PUT/PATCH/DELETE: apenas administradores
    '''

    queryset = Flight.objects.select_related('airplane').all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]


class ClientViewSet(viewsets.ModelViewSet):
    '''
    CRUD de Clientes
    - Apenas usuários autenticados podem acessar
    - Usuários comuns só veem e editam o próprio perfil
    - Administradores veem todos os clientes
    '''

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(user=user)


class ReservationViewSet(viewsets.ModelViewSet):
    '''
    CRUD de Reservas
    - Apenas usuários autenticados podem acessar
    - Usuários comuns só veem as próprias reservas
    - Administradores veem todas as reservas
    '''
    
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.select_related('client', 'flight', 'flight__airplane').all()
        return Reservation.objects.select_related('client', 'flight', 'flight__airplane').filter(client__user=user)
