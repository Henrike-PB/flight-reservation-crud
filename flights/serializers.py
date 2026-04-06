from rest_framework import serializers
from django.utils import timezone
from .models import Flight, Airplane, Client, Reservation


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    # Aqui definimos um campo somente-leitura para exibir o nome do avião nas respostas
    airplane_detail = AirplaneSerializer(source='airplane', read_only=True)

    def validate(self, data):
        '''
        Validações de regra de negócio para criação e edição de voos:
        1. Origem e destino não podem ser iguais.
        2. Data de partida não pode estar no passado.
        3. Data de chegada deve ser posterior à de partida.
        '''

        instance = self.instance
        origin = data.get('origin', getattr(instance, 'origin', None))
        destination = data.get('destination', getattr(instance, 'destination', None))
        departure = data.get('departure_time', getattr(instance, 'departure_time', None))
        arrival = data.get('arrival_time', getattr(instance, 'arrival_time', None))

        if origin and destination and origin.strip().lower() == destination.strip().lower():
            raise serializers.ValidationError(
                {"destination": "A origem e o destino não podem ser iguais."}
            )

        if departure and departure < timezone.now():
            raise serializers.ValidationError(
                {"departure_time": "A data de partida não pode ser no passado."}
            )

        if departure and arrival and departure >= arrival:
            raise serializers.ValidationError(
                {"arrival_time": "A data de chegada deve ser posterior à data de partida."}
            )

        return data

    class Meta:
        model = Flight
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    '''
    Serializer para Reservas.

    Na leitura (GET): exibe os dados completos do voo e do cliente.
    Na escrita (POST/PUT): aceita os IDs de flight e client normalmente.

    Isso é feito porque estamos usando campos separados para leitura e escrita:
    - flight_detail / client_detail: somente leitura, dados expandidos.
    - flight / client: somente escrita, irao receber o ID (PrimaryKeyRelatedField).
    '''

    # Aqui definimos campos de leitura (retornam os dados completos nos GETs)
    flight_detail = FlightSerializer(source='flight', read_only=True)
    client_detail = ClientSerializer(source='client', read_only=True)

    def validate(self, data):
        '''
        Validações de regra de negócio para reservas:
        1. O número do assento deve ser um inteiro positivo.
        2. O assento não pode exceder a capacidade do avião.
        3. O voo não pode já ter lotado (total de reservas < capacidade).
        '''

        flight = data.get('flight', getattr(self.instance, 'flight', None))
        seat = data.get('seat', getattr(self.instance, 'seat', None))

        if flight and seat:
            # nesse trecho, tentamos converter o número do assento para inteiro para validar que é um número válido
            try:
                seat_number = int(seat)
            except (ValueError, TypeError):
                raise serializers.ValidationError(
                    {"seat": "O assento deve ser um número inteiro (ex: 1, 2, 3...)."}
                )

            if seat_number < 1:
                raise serializers.ValidationError(
                    {"seat": "O número do assento deve ser maior que zero."}
                )

            # validando que o assento não excede a capacidade do avião
            capacity = flight.airplane.capacity
            if seat_number > capacity:
                raise serializers.ValidationError(
                    {"seat": f"Este avião tem apenas {capacity} assentos. Assento {seat_number} é inválido."}
                )

            # verifica  que o voo não está lotado
            reservations_count = flight.reservations.count()

            if self.instance:
                reservations_count = flight.reservations.exclude(pk=self.instance.pk).count()

            if reservations_count >= capacity:
                raise serializers.ValidationError(
                    {"flight": f"Este voo está lotado ({capacity}/{capacity} assentos ocupados)."}
                )

        return data

    class Meta:
        model = Reservation
        fields = [
            'id', 'client', 'flight', 'seat', 'reservation_date',
            'flight_detail', 'client_detail',
        ]
        read_only_fields = ['reservation_date']
