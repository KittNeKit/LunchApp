from rest_framework import routers

from menu.views import MenuViewSet

router = routers.DefaultRouter()
router.register("", MenuViewSet)

urlpatterns = [] + router.urls

app_name = "menu"
