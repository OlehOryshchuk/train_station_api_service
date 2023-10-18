from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (
    Station,
    Route,
    Trip,
    Crew,
    TrainType,
    Train,
    Order,
    Ticket,
)


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = [
            "id",
            "name",
            "cargo_num",
            "seats_in_cargo",
            "train_type",
            "capacity",
        ]


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
        ]


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )
    destination = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )


class TrainListSerializer(TrainSerializer):
    train_type_name = serializers.CharField(
        read_only=True, source="train_type.name"
    )

    class Meta:
        model = Train
        fields = [
            "id",
            "name",
            "cargo_num",
            "seats_in_cargo",
            "train_type_name",
            "image",
        ]


class TrainDetailSerialize(TrainSerializer):
    train_type = TrainTypeSerializer(read_only=True)

    class Meta:
        model = Train
        fields = [
            "id",
            "name",
            "cargo_num",
            "seats_in_cargo",
            "train_type",
            "image",
        ]


class TrainImageSerializer(TrainSerializer):
    class Meta:
        model = Train
        fields = ["id", "image"]


class TripListSerializer(TripSerializer):
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    route = serializers.StringRelatedField(read_only=True)
    train_name = serializers.CharField(
        sread_only=True, source="train.name"
    )
    train_image = serializers.ImageField(
        source="train.image", read_only=True,
    )
    train_capacity = serializers.SlugRelatedField(
        read_only=True, slug_field="capacity"
    )
    # TODO: when i will create TripViewSet i need to create field
    #  tickets_available using F(train.capacity) - COUNT(tickets)

    class Meta:
        model = Trip
        fields = [
            "crew",
            "route",
            "train_name",
            "departure_time",
            "arrival_time",
            "train_capacity",
        ]
