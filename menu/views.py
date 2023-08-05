import datetime

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from menu.models import Menu
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
    def vote_for_menu(self):
        pass
