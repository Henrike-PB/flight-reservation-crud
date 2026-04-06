from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

'''
Aqui em models.py, estamos definindo os modelos de dados para o sistema de reserva de voos.
Temos quatro modelos principais: Airplane, Flight, Client e Reservation.
'''


class Airplane(models.Model):
    '''
    Representa um avião cadastrado no sistema.
    - model: identificação única do avião (ex: "Boeing 737-800").
    - capacity: número máximo de passageiros (deve ser >= 1).
    '''

    model = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="A capacidade deve ser de pelo menos 1 passageiro.")]
    )

    def __str__(self):
        return f"{self.model} ({self.capacity} lugares)"


class Flight(models.Model):
    '''
    Representa um voo registrado no sistema.
    - flight_number: código único do voo (ex: "AD1234").
    - origin / destination: cidades de origem e destino.
    - departure_time / arrival_time: data e horário de partida e chegada.
    - airplane: avião associado a este voo (FK -> Airplane).
    '''

    flight_number = models.CharField(max_length=10, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')

    def __str__(self):
        return f"{self.flight_number}: {self.origin} → {self.destination}"


class Client(models.Model):
    '''
    Representa um cliente que pode fazer reservas.
    - user: vínculo 1:1 com o sistema de autenticação do Django.
    - name: nome completo do cliente.
    - telephone: telefone de contato.
    - email: e-mail único para identificação.
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    '''
    Representa uma reserva de assento em um voo.
    - client: cliente que fez a reserva (FK -> Client).
    - flight: voo reservado (FK -> Flight).
    - seat: número/código do assento (ex: "12A").
    - reservation_date: data/hora em que a reserva foi criada (automática).

    Restrições:
    - Não pode haver duas reservas com o mesmo assento no mesmo voo (UniqueConstraint).
    '''

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reservations')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reservations')
    seat = models.CharField(max_length=5)
    reservation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['flight', 'seat'], name='unique_seat_per_flight')
        ]

    def __str__(self):
        return f"Reserva: {self.client.name} - Voo {self.flight.flight_number} (Assento {self.seat})"