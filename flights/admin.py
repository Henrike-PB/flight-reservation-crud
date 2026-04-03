from django.contrib import admin
from .models import Airplane, Flight, Client, Reservation

'''
Aqui estamos registrando os modelos Airplane, Flight, Client e Reservation no admin do Django para que possamos gerenciá-los através da interface administrativa.
Cada classe de admin personalizada (AirplaneAdmin, FlightAdmin, ClientAdmin e ReservationAdmin)
'''

'''
Na classe AirplaneAdmin, estamos configurando a exibição dos campos model e capacity na lista de aviões e permitindo a busca pelo campo model.
'''
@admin.register(Airplane) # usamos esse decorador para registrar o modelo Airplane no admin do Django
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('model', 'capacity')
    search_fields = ('model',)


'''
Nessa classe FlightAdmin, estamos configurando a exibição dos campos flight_number, origin, destination, departure_time, arrival_time e airplane na lista de voos e permitindo a busca pelos campos flight_number, origin e destination.
'''
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'origin', 'destination', 'departure_time', 'arrival_time', 'airplane')
    search_fields = ('flight_number', 'origin', 'destination')

'''
Na classe ClientAdmin, estamos configurando a exibição dos campos name, telephone e email na lista de clientes e permitindo a busca pelos campos name e email.
'''
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'telephone', 'email')
    search_fields = ('name', 'email')

'''
E na classe ReservationAdmin, estamos configurando a exibição dos campos client, flight, seat e reservation_date na lista de reservas e permitindo a busca pelos campos client e flight.
'''
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('client', 'flight', 'seat', 'reservation_date')
    search_fields = ('client', 'flight')


