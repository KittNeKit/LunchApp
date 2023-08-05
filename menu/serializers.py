from rest_framework import serializers

from menu.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("name", "votes")
        read_only_fields = ("votes",)


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("id", "menu", "restaurant")
        read_only_fields = ("menu", "restaurant")


class MenuRestaurantSerializer(MenuSerializer):
    class Meta:
        model = Menu
        fields = ("menu", "restaurant", "day_of_the_week")
