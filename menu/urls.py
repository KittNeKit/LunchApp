from django.urls import path
from rest_framework import routers

from menu.views import MenuViewSet, RestaurantViewSet, get_most_voted_menu

router = routers.DefaultRouter()
router.register("vote", MenuViewSet)
router.register("restaurant", RestaurantViewSet)

urlpatterns = [
    path("most-voted/", get_most_voted_menu),
] + router.urls

app_name = "menu"
