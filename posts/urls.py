from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.PostViewSet)
app_name = "posts"

urlpatterns = router.urls
