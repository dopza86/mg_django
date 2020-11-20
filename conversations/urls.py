from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.ConversationViewSet)
app_name = "consversations"

urlpatterns = router.urls
