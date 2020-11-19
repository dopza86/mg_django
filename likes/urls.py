from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.LikeViewSet)
app_name = "likes"

urlpatterns = router.urls
