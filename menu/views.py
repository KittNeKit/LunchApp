import datetime

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from menu.models import Menu, Restaurant
from menu.serializers import MenuSerializer


class MenuViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Menu.objects.select_related("restaurant")
    serializer_class = MenuSerializer

    def get_queryset(self):
        current_day = datetime.datetime.now().strftime("%A")
        queryset = self.queryset.filter(day_of_the_week=current_day)
        return queryset

    @action(detail=True, methods=["post"])
    def vote_for_menu(self, request, pk=None):
        if not request.user.votes:
            restaurant = Restaurant.objects.get(
                pk=Menu.objects.get(pk=pk).restaurant.pk
            )
            restaurant.votes += 1
            request.user.votes = True
            request.user.save()
            restaurant.save()
            return Response(
                {"success": "You are vote for menu of the day."}, status.HTTP_200_OK
            )
        return Response({"error": "You already vote today."}, status.HTTP_403_FORBIDDEN)
