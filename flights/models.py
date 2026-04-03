from django.db import models


'''
Modelos para o aplicativo de voos. Inclui as classes Airplane e Flight, que representam os aviões e os voos, respectivamente.
'''

'''
Nesta classe, estamos definindo o modelo Airplane, que tem os campos model (modelo do avião) e capacity (capacidade de passageiros).
O campo model é único para garantir que não haja dois aviões com o mesmo modelo.
'''
class Airplane(models.Model):
    model = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return self.model

'''
Nesta classe, estamos definindo o modelo Flight, que tem os campos:

flight_number (número do voo), origin (origem), destination (destino),
departure_time (hora de saída), arrival_time (hora de chegada)  e airplane (avião). 

O campo flight_number é único para garantir que não haja dois voos com o mesmo número.
'''
class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.flight_number}: {self.origin} -> {self.destination}"

'''
Aqui teremos a classe Client, que representa os clientes que fazem reservas de voos.
Ela tem os campos name (nome), telephone (telefone) e email (e-mail).
O campo email é único para garantir que não haja dois clientes com o mesmo e-mail.
'''  
class Client(models.Model):
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
'''
Por fim, temos a classe Reservation, que representa as reservas feitas pelos clientes.
Ela tem os campos client (cliente que fez a reserva), flight (voo reservado) e reservation_date (data da reserva).
'''
class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.CharField(max_length=5)
    reservation_date = models.DateTimeField(auto_now_add=True)

    '''
    A classe Meta é usada para definir restrições e opções adicionais para o modelo. 
    Neste caso, estamos definindo uma restrição de unicidade para garantir que não haja duas reservas com o mesmo voo e assento.
    Isso é importante para evitar que dois clientes reservem o mesmo assento no mesmo voo.
    '''
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['flight', 'seat'], name='unique_seat_per_flight')
        ]

    def __str__(self):
        return f"Reservation for {self.client.name} on flight {self.flight.flight_number}"