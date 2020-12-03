from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.FollowRelationViewSet)
app_name = "follow_relation"

urlpatterns = router.urls
