from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'category',CategoryView)
router.register(r'custom-user',CustomUserView)
router.register(r'environment',EnvironmentView)
router.register(r'equipment',EquipmentView)
router.register(r'notification',NotificationView)
router.register(r'tasks/status',TaskStatusView)
router.register(r'tasks/images',TaskStatusImageView)
router.register(r'tasks',TaskView)

urlpatterns = router.urls