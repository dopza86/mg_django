from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.CommentViewSet)
app_name = "comments"

urlpatterns = router.urls
