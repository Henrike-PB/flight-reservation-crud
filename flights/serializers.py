from rest_framework import serializers
from .models import Flight, Airplane, Client, Reservation

'''
Aqui estamos definindo os serializers para os modelos Flight, Airplane, Client e Reservation.

Para cada modelo, criamos uma classe de serializer que herda de serializers.ModelSerializer e especificamos o modelo e os campos a serem incluídos na serialização.
No caso, estamos incluindo todos os campos de cada modelo usando fields = '__all__'.
'''

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    ''''
    Aqui, estamos definindo os campos flight e client como read_only=True para indicar que esses campos não podem ser modificados diretamente através do serializer.
    '''
    flight = FlightSerializer(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'

