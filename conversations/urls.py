from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"conversation", views.ConversationModelViewSet)
router.register(r"message", views.MessageModelViewSet)
# app_name = "consversations"

urlpatterns = router.urls