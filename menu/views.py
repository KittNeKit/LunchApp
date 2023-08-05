import datetime

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from menu.models import Menu, Restaurant
from menu.permissions import IsRestaurantOrIfUserReadOnly
from menu.serializers import (
    MenuSerializer,
    RestaurantSerializer,
    MenuRestaurantSerializer,
)


@extend_schema_view(
    list=extend_schema(
        description=(
            "All menu in the LunchApp endpoint "
            "(User can see all menu of the current day of the week, "
            "Restaurants users can see all of owns menu)."
        )
    ),
    retrieve=extend_schema(description="Specific menu endpoint."),
    create=extend_schema(description="Creating a new menu endpoint."),
)
class MenuViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Menu.objects.select_related("restaurant")
    serializer_class = MenuSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.type_of_user == "Employee":
            current_day = datetime.datetime.now().strftime("%A")
            return self.queryset.filter(day_of_the_week=current_day)
        return self.queryset.filter(restaurant__owner=self.request.user.id)

    def get_serializer_class(self):
        if self.request.user.type_of_user == "Employee":
            return self.serializer_class
        return MenuRestaurantSerializer

    def create(self, request, *args, **kwargs):
        restaurant = request.data.get("restaurant")
        try:
            restaurant = Restaurant.objects.get(pk=restaurant)
            if restaurant.owner == request.user:
                return super().create(request, *args, **kwargs)
            else:
                return Response(
                    {"error": "You can only "
                              "create menus for your own restaurants."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        """Function to vote for menu, User can vote only once"""
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


@api_view(["Get"])
def get_most_voted_menu(request):
    """View for most voted restaurant"""
    restaurant = Restaurant.objects.all().order_by("-votes").first()
    serializer = RestaurantSerializer(restaurant, many=False)
    return Response(serializer.data, status=200)


@extend_schema_view(
    list=extend_schema(
        description=(
            "All restaurants in the LunchApp endpoint "
            "(User can see all restaurants, "
            "Restaurants users can see all of owns restaurants)."
        )
    ),
    retrieve=extend_schema(description="Specific restaurants endpoint."),
    create=extend_schema(description="Creating a new restaurants endpoint."),
)
class RestaurantViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsRestaurantOrIfUserReadOnly)

    def get_queryset(self):
        if self.request.user.type_of_user == "Restaurant":
            return self.queryset.filter(owner_id=self.request.user.id)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.id)
