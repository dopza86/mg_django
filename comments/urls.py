from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"comments", views.CommentViewSet)
router.register(r"text", views.TextViewSet)

urlpatterns = router.urls
