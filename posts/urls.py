from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register("", views.PostViewSet)
router.register(r"post", views.PostViewSet)
router.register(r"photo", views.PhotoViewSet)
# app_name = "posts"

urlpatterns = router.urls
